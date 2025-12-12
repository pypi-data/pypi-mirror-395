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
logger = logging.getLogger('grond.problems.locate.problem')
km = 1e3
as_km = dict(scale_factor=km, scale_unit='km')


class LocateProblemConfig(ProblemConfig):

    ranges = Dict.T(String.T(), gf.Range.T())
    distance_min = Float.T(default=0.0)

    def get_problem(self, event, target_groups, targets):
        self.check_deprecations()

        if event.depth is None:
            event.depth = 0.

        base_source = gf.Source.from_pyrocko_event(event)

        subs = dict(
            event_name=event.name,
            event_time=util.time_to_str(event.time))

        problem = LocateProblem(
            name=expand_template(self.name_template, subs),
            base_source=base_source,
            target_groups=target_groups,
            targets=targets,
            ranges=self.ranges,
            distance_min=self.distance_min,
            norm_exponent=self.norm_exponent)

        return problem


@has_get_plot_classes
class LocateProblem(Problem):

    problem_parameters = [
        Parameter('time', 's', label='Time'),
        Parameter('north_shift', 'm', label='Northing', **as_km),
        Parameter('east_shift', 'm', label='Easting', **as_km),
        Parameter('depth', 'm', label='Depth', **as_km)]

    dependants = []

    distance_min = Float.T(default=0.0)

    def __init__(self, **kwargs):
        Problem.__init__(self, **kwargs)

    def get_source(self, x):
        d = self.get_parameter_dict(x)

        p = {}
        for k in self.base_source.keys():
            if k in d:
                p[k] = float(
                    self.ranges[k].make_relative(self.base_source[k], d[k]))

        return self.base_source.clone(**p)

    def pack(self, source):
        return num.array([
            source.time - self.base_source.time,
            source.north_shift,
            source.east_shift,
            source.depth])

    def preconstrain(self, x):
        source = self.get_source(x)
        for t in self.waveform_targets + self.phase_pick_targets:
            if (self.distance_min > num.asarray(t.distance_to(source))).any():
                raise Forbidden()

        return x

    @classmethod
    def get_plot_classes(cls):
        from .. import plot
        plots = super(LocateProblem, cls).get_plot_classes()
        plots.extend([plot.LocationPlot])
        return plots


__all__ = '''
    LocateProblem
    LocateProblemConfig
'''.split()
