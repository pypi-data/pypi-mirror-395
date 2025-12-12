# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
import logging

import numpy as num

from pyrocko.guts import Float, Tuple, String, Int, List
from pyrocko import gf, util
from pyrocko.plot import beachball

from ..base import MisfitTarget, TargetGroup, MisfitResult
from grond.meta import has_get_plot_classes, GrondError, nslcs_to_patterns

guts_prefix = 'grond'
logger = logging.getLogger('grond.targets.phase_pick.target')


def log_exclude(target, reason):
    logger.debug('Excluding potential target %s: %s' % (
        target.string_id(), reason))


class PhasePickTargetGroup(TargetGroup):

    '''
    Generate targets to fit phase arrival times.
    '''

    distance_min = Float.T(optional=True)
    distance_max = Float.T(optional=True)
    distance_3d_min = Float.T(optional=True)
    distance_3d_max = Float.T(optional=True)
    depth_min = Float.T(optional=True)
    depth_max = Float.T(optional=True)
    store_id = gf.StringID.T(optional=True)
    include = List.T(
        String.T(),
        optional=True,
        help='If not None, list of stations/components to include according '
             'to their STA, NET.STA, NET.STA.LOC, or NET.STA.LOC.CHA codes.')
    exclude = List.T(
        String.T(),
        help='Stations/components to be excluded according to their STA, '
             'NET.STA, NET.STA.LOC, or NET.STA.LOC.CHA codes.')
    limit = Int.T(optional=True)

    pick_synthetic_traveltime = gf.Timing.T(
        help='Synthetic phase arrival definition.')
    pick_phasename = String.T(
        help='Name of phase in pick file.')

    weight_traveltime = Float.T(default=1.0)
    weight_polarity = Float.T(default=1.0)

    def get_targets(self, ds, event, default_path='none'):
        logger.debug('Selecting phase pick targets...')
        origin = event
        targets = []

        stations = ds.get_stations()
        if len(stations) == 0:
            logger.warning(
                'No stations found to create waveform target group.')

        for st in stations:
            nslc = st.nsl() + ('',)
            target = PhasePickTarget(
                codes=nslc[:3],
                lat=st.lat,
                lon=st.lon,
                north_shift=st.north_shift,
                east_shift=st.east_shift,
                depth=st.depth,
                store_id=self.store_id,
                manual_weight=self.weight,
                normalisation_family=self.normalisation_family,
                path=self.path or default_path,
                pick_synthetic_traveltime=self.pick_synthetic_traveltime,
                pick_phasename=self.pick_phasename,
                weight_polarity=self.weight_polarity,
                weight_traveltime=self.weight_traveltime)

            if util.match_nslc(
                    nslcs_to_patterns(self.exclude), nslc):
                log_exclude(target, 'excluded by target group')
                continue

            if self.include is not None and not util.match_nslc(
                    nslcs_to_patterns(self.include), nslc):
                log_exclude(target, 'excluded by target group')
                continue

            if self.distance_min is not None and \
               target.distance_to(origin) < self.distance_min:
                log_exclude(target, 'distance < distance_min')
                continue

            if self.distance_max is not None and \
               target.distance_to(origin) > self.distance_max:
                log_exclude(target, 'distance > distance_max')
                continue

            if self.distance_3d_min is not None and \
               target.distance_3d_to(origin) < self.distance_3d_min:
                log_exclude(target, 'distance_3d < distance_3d_min')
                continue

            if self.distance_3d_max is not None and \
               target.distance_3d_to(origin) > self.distance_3d_max:
                log_exclude(target, 'distance_3d > distance_3d_max')
                continue

            if self.depth_min is not None and \
               target.depth < self.depth_min:
                log_exclude(target, 'depth < depth_min')
                continue

            if self.depth_max is not None and \
               target.depth > self.depth_max:
                log_exclude(target, 'depth > depth_max')
                continue

            marker = ds.get_pick(
                event.name,
                target.codes[:3],
                target.pick_phasename)

            if not marker:
                log_exclude(target, 'no pick available')
                continue

            target.set_dataset(ds)
            targets.append(target)

        return targets

    def is_gf_store_appropriate(self, store, depth_range):
        ok = TargetGroup.is_gf_store_appropriate(
            self, store, depth_range)
        ok &= self._is_gf_store_appropriate_check_extent(
            store, depth_range)
        return ok


class PhasePickResult(MisfitResult):
    tobs = Float.T(optional=True)
    tsyn = Float.T(optional=True)
    polarity_obs = Float.T(optional=True)
    polarity_syn = Float.T(optional=True)
    azimuth = Float.T(optional=True)
    takeoff_angle = Float.T(optional=True)


@has_get_plot_classes
class PhasePickTarget(gf.Location, MisfitTarget):

    '''
    Target to fit phase arrival times.
    '''

    codes = Tuple.T(
        3, String.T(),
        help='network, station, location codes.')

    store_id = gf.StringID.T(
        help='ID of Green\'s function store (only used for earth model).')

    pick_synthetic_traveltime = gf.Timing.T(
        help='Synthetic phase arrival definition.')

    pick_phasename = String.T(
        help='Name of phase in pick file.')

    can_bootstrap_weights = True

    weight_traveltime = Float.T(default=1.0)
    weight_polarity = Float.T(default=1.0)

    def __init__(self, **kwargs):
        gf.Location.__init__(self, **kwargs)
        MisfitTarget.__init__(self, **kwargs)
        self._tobs_cache = {}

    @property
    def nmisfits(self):
        return 2

    @classmethod
    def get_plot_classes(cls):
        from . import plot
        plots = super(PhasePickTarget, cls).get_plot_classes()
        plots.extend(plot.get_plot_classes())
        return plots

    def string_id(self):
        return '.'.join(x for x in (self.path,) + self.codes)

    def set_dataset(self, ds):
        MisfitTarget.set_dataset(self, ds)
        self._obs_cache = {}

    def get_plain_targets(self, engine, source):
        return self.prepare_modelling(engine, source, None)

    def prepare_modelling(self, engine, source, targets):
        return []

    def get_times_polarities(self, engine, source):
        tsyn = None

        k = source.name
        if k not in self._obs_cache:
            ds = self.get_dataset()
            tobs = None
            marker = ds.get_pick(
                source.name,
                self.codes[:3],
                self.pick_phasename)

            if marker:
                polarity_obs = marker.get_polarity()
                if polarity_obs not in (1, -1, None):
                    raise GrondError(
                        'Polarity of pick %s.%s.%s.%s must be 1 or -1 or None'
                        % marker.one_nslc())
                self._obs_cache[k] = marker.tmin, polarity_obs
            else:
                self._obs_cache[k] = None

        tobs, polarity_obs = self._obs_cache[k]

        store = engine.get_store(self.store_id)

        use_polarities = self.weight_polarity > 0. and polarity_obs is not None
        use_traveltimes = self.weight_traveltime > 0. and tobs is not None

        if use_polarities:
            traveltime, takeoff_angle = store.t(
                self.pick_synthetic_traveltime, source, self,
                attributes=['takeoff_angle'])
        else:
            traveltime = store.t(
                self.pick_synthetic_traveltime, source, self)
            takeoff_angle = None

        if use_traveltimes:
            tsyn = source.time + traveltime
        else:
            tsyn = None

        if use_polarities:
            mt = source.pyrocko_moment_tensor()
            azimuth = source.azibazi_to(self)[0]
            amp = beachball.amplitudes(mt, [azimuth], [takeoff_angle])[0]
            polarity_syn = -1.0 if amp < 0. else 1.0
        else:
            polarity_syn = None
            azimuth = None

        return tobs, tsyn, polarity_obs, polarity_syn, azimuth, takeoff_angle

    def finalize_modelling(
            self, engine, source, modelling_targets, modelling_results):

        ds = self.get_dataset()  # noqa

        tobs, tsyn, polarity_obs, polarity_syn, azimuth, takeoff_angle = \
            self.get_times_polarities(engine, source)

        misfits = num.full((2, 2), num.nan)
        misfits[:, 1] = 1.0

        if self.weight_traveltime > 0. and None not in (tobs, tsyn):
            misfits[0, 0] = self.weight_traveltime * abs(tobs - tsyn)

        if self.weight_polarity > 0. \
                and None not in (polarity_obs, polarity_syn):
            misfits[1, 0] = self.weight_polarity \
                 * 0.5 * abs(polarity_obs - polarity_syn)

        result = PhasePickResult(
            tobs=tobs,
            tsyn=tsyn,
            polarity_obs=polarity_obs,
            polarity_syn=polarity_syn,
            azimuth=azimuth,
            takeoff_angle=takeoff_angle,
            misfits=misfits)

        return result


__all__ = '''
    PhasePickTargetGroup
    PhasePickTarget
    PhasePickResult
'''.split()
