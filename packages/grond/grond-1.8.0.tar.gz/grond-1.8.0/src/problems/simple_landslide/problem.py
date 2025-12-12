# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
import numpy as num
import logging

from pyrocko import gf, util
from pyrocko.guts import String, Float, Dict

from grond.meta import Forbidden, expand_template, Parameter, \
    has_get_plot_classes

from ..base import Problem, ProblemConfig

guts_prefix = 'grond'
logger = logging.getLogger('grond.problems.simple_landslide.problem')
km = 1e3
as_km = dict(scale_factor=km, scale_unit='km')


class SimpleLandslideProblemConfig(ProblemConfig):

    ranges = Dict.T(String.T(), gf.Range.T())
    distance_min = Float.T(default=0.0)

    def get_problem(self, event, target_groups, targets):
        if event.depth is None:
            event.depth = 0.

        base_source = gf.SimpleLandslideSource.from_pyrocko_event(
            event,
            anchor_stf='centroid')

        subs = dict(
            event_name=event.name,
            event_time=util.time_to_str(event.time))

        problem = SimpleLandslideProblem(
            name=expand_template(self.name_template, subs),
            base_source=base_source,
            target_groups=target_groups,
            targets=targets,
            ranges=self.ranges,
            distance_min=self.distance_min,
            norm_exponent=self.norm_exponent)

        return problem


@has_get_plot_classes
class SimpleLandslideProblem(Problem):

    problem_parameters = [
        Parameter('time', 's', label='Time'),
        Parameter('north_shift', 'm', label='Northing', **as_km),
        Parameter('east_shift', 'm', label='Easting', **as_km),
        Parameter('depth', 'm', label='Depth', **as_km),
        Parameter('impulse_n', 'Ns', label='$p_{n}$'),
        Parameter('impulse_e', 'Ns', label='$p_{e}$'),
        Parameter('impulse_d', 'Ns', label='$p_{d}$'),
        Parameter('azimuth', 'deg', label='Azimuth'),
        Parameter('duration_acc_v', 's', label='T_{av}'),
        Parameter('duration_acc_h', 's', label='T_{ah}'),
        Parameter('duration_dec_v', 's', label='T_{dv}'),
        Parameter('duration_dec_h', 's', label='T_{dh}'),
    ]

    dependants = []

    distance_min = Float.T(default=0.0)

    def __init__(self, **kwargs):
        Problem.__init__(self, **kwargs)
        self.deps_cache = {}
        self.problem_parameters = self.problem_parameters

    def get_source(self, x):
        d = self.get_parameter_dict(x)
        p = {}
        for k in self.base_source.keys():
            if k in d:
                p[k] = float(
                    self.ranges[k].make_relative(self.base_source[k], d[k]))

        stf_v = gf.SimpleLandslideSTF(
            duration_acceleration=d['duration_acc_v'],
            duration_deceleration=d['duration_dec_v'])
        stf_h = gf.SimpleLandslideSTF(
            duration_acceleration=d['duration_acc_h'],
            duration_deceleration=d['duration_dec_h'])

        return self.base_source.clone(**p, stf_v=stf_v, stf_h=stf_h)

    def make_dependant(self, xs, pname):
        pass

    def pack(self, source):
        x = num.array([
            source.time - self.base_source.time,
            source.north_shift,
            source.east_shift,
            source.depth,
            source.impulse_n,
            source.impulse_e,
            source.impulse_d,
            source.stf_v.duration_acceleration,
            source.stf_h.duration_acceleration,
            source.stf_v.duration_deceleration,
            source.stf_h.duration_deceleration], dtype=float)

        return x

    def preconstrain(self, x):
        source = self.get_source(x)
        if any(self.distance_min > source.distance_to(t)
               for t in self.waveform_targets + self.phase_pick_targets):
            raise Forbidden()
        return x

    @classmethod
    def get_plot_classes(cls):
        from ..singleforce import plot
        plots = super(SimpleLandslideProblem, cls).get_plot_classes()
        plots.extend([plot.SFLocationPlot, plot.SFForcePlot])
        return plots


__all__ = '''
    SimpleLandslideProblem
    SimpleLandslideProblemConfig
'''.split()
