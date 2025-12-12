# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
import numpy as num
import logging

from pyrocko import gf, util
from pyrocko.guts import String, Float, Dict, StringChoice

from grond.meta import Forbidden, expand_template, Parameter, \
    has_get_plot_classes

from ..base import Problem, ProblemConfig

guts_prefix = 'grond'
logger = logging.getLogger('grond.problems.double_sf.problem')
km = 1e3
as_km = dict(scale_factor=km, scale_unit='km')


class DoubleSFProblemConfig(ProblemConfig):

    ranges = Dict.T(String.T(), gf.Range.T())
    distance_min = Float.T(default=0.0)
    force_directions = StringChoice.T(
        choices=('off', 'unidirectional', 'counterdirectional'),
        default='off')

    def get_problem(self, event, target_groups, targets):
        if event.depth is None:
            event.depth = 0.

        source = gf.SFSource.from_pyrocko_event(event)
        source.stf = gf.HalfSinusoidSTF(duration=event.duration or 0.0)

        base_source = gf.CombiSFSource(
            name=source.name,
            subsources=[
                source.clone(name=''),
                source.clone(name='')])

        source.lat, source.lon = event.effective_latlon

        subs = dict(
            event_name=event.name,
            event_time=util.time_to_str(event.time))

        problem = DoubleSFProblem(
            name=expand_template(self.name_template, subs),
            base_source=base_source,
            target_groups=target_groups,
            targets=targets,
            ranges=self.ranges,
            distance_min=self.distance_min,
            norm_exponent=self.norm_exponent,
            force_directions=self.force_directions)

        return problem


@has_get_plot_classes
class DoubleSFProblem(Problem):

    problem_parameters = [
        Parameter('time1', 's', label='Time'),
        Parameter('north_shift1', 'm', label='Northing', **as_km),
        Parameter('east_shift1', 'm', label='Easting', **as_km),
        Parameter('depth1', 'm', label='Depth', **as_km),
        Parameter('time2', 's', label='Time'),
        Parameter('north_shift2', 'm', label='Northing', **as_km),
        Parameter('east_shift2', 'm', label='Easting', **as_km),
        Parameter('depth2', 'm', label='Depth', **as_km),
        Parameter('fn1', 'N', label='$F_{n1}$'),
        Parameter('fe1', 'N', label='$F_{e1}$'),
        Parameter('fd1', 'N', label='$F_{d1}$'),
        Parameter('fn2', 'N', label='$F_{n2}$'),
        Parameter('fe2', 'N', label='$F_{e2}$'),
        Parameter('fd2', 'N', label='$F_{d2}$'),
        Parameter('duration1', 's', label='Duration 1'),
        Parameter('duration2', 's', label='Duration 2')]

    dependants = [
        Parameter('force1', 'N', label='$||F_1||$'),
        Parameter('force2', 'N', label='$||F_2||$')]

    distance_min = Float.T(default=0.0)
    force_directions = String.T()

    def __init__(self, **kwargs):
        Problem.__init__(self, **kwargs)
        self.deps_cache = {}

    def get_source(self, x):
        d = self.get_parameter_dict(x)

        sources = []

        for i, subsource in enumerate(self.base_source.subsources):
            p = {}

            for k in subsource.keys():
                key = '%s%d' % (k, i+1)
                if key in d:
                    p[k] = float(
                        self.ranges[key].make_relative(subsource[k], d[key]))

            sources.append(self.base_source.subsources[i].clone(**p))

        sources[0].stf = gf.HalfSinusoidSTF(duration=float(d.duration1))
        sources[1].stf = gf.HalfSinusoidSTF(duration=float(d.duration2))

        return self.base_source.clone(subsources=sources)

    def make_dependant(self, xs, pname):
        cache = self.deps_cache
        if xs.ndim == 1:
            return self.make_dependant(xs[num.newaxis, :], pname)[0]

        if pname not in self.dependant_names:
            raise KeyError(pname)

        y = num.zeros(xs.shape[0])
        for i, x in enumerate(xs):
            k = tuple(x.tolist())
            if k not in cache:
                source = self.get_source(x)
                cache[k] = source

            source = cache[k]

            y[i] = getattr(source.subsources[int(pname[-1]) - 1], pname[:-1])

        return y

    def pack(self, source):
        arr = self.get_parameter_array(source)
        subsrcs = source.subsources
        for ip, p in enumerate(self.parameters):
            # if p.name == 'time':
            #     arr[ip] -= self.base_source.time
            if p.name == 'duration1':
                arr[ip] = subsrcs[0].stf.duration if subsrcs[0].stf else 0.0
            if p.name == 'duration2':
                arr[ip] = subsrcs[1].stf.duration if subsrcs[1].stf else 0.0
        return arr

    def preconstrain(self, x):
        source = self.get_source(x)
        if any(self.distance_min > source.distance_to(t)
               for t in self.waveform_targets + self.phase_pick_targets):
            raise Forbidden()

        if self.force_directions == 'unidirectional':
            force1 = source.subsources[0].force
            force2 = source.subsources[1].force

            ratio = force2 / force1

            idx_fn2 = self.get_parameter_index('fn2')
            idx_fe2 = self.get_parameter_index('fe2')
            idx_fd2 = self.get_parameter_index('fd2')

            x[idx_fn2] = source.subsources[0].fn * ratio
            x[idx_fe2] = source.subsources[0].fe * ratio
            x[idx_fd2] = source.subsources[0].fd * ratio

        elif self.force_directions == 'counterdirectional':
            force1 = source.subsources[0].force
            force2 = source.subsources[1].force

            ratio = force2 / force1

            idx_fn2 = self.get_parameter_index('fn2')
            idx_fe2 = self.get_parameter_index('fe2')
            idx_fd2 = self.get_parameter_index('fd2')

            x[idx_fn2] = -source.subsources[0].fn * ratio
            x[idx_fe2] = -source.subsources[0].fe * ratio
            x[idx_fd2] = -source.subsources[0].fd * ratio

        return x

    def get_dependant_bounds(self):
        range_start = num.min([
            (self.ranges['f{}1'.format(f)].start,
             self.ranges['f{}2'.format(f)].start) for f in 'n e d'.split()],
            axis=0)

        range_stop = num.max([
            (self.ranges['f{}1'.format(f)].stop,
             self.ranges['f{}2'.format(f)].stop) for f in 'n e d'.split()],
            axis=0)

        force_range = (
            -num.linalg.norm(range_start),
            num.linalg.norm(range_stop))

        out = [force_range, force_range]

        return out

    @classmethod
    def get_plot_classes(cls):
        from . import plot
        plots = super(DoubleSFProblem, cls).get_plot_classes()
        plots.extend([
            plot.DoubleSFForcePlot,
            plot.DoubleSFDecompositionPlot])
        return plots


__all__ = '''
    DoubleSFProblem
    DoubleSFProblemConfig
'''.split()
