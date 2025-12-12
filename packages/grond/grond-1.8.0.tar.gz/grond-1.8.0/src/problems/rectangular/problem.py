# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
import logging

from pyrocko import gf, util
from pyrocko.guts import String, Dict, Int, Float

from grond.meta import expand_template, Parameter, has_get_plot_classes

from ..base import Problem, ProblemConfig

guts_prefix = 'grond'
logger = logging.getLogger('grond.problems.rectangular.problem')
km = 1e3
as_km = dict(scale_factor=km, scale_unit='km')


class RectangularProblemConfig(ProblemConfig):

    ranges = Dict.T(String.T(), gf.Range.T())
    decimation_factor = Int.T(default=1)
    distance_min = Float.T(default=0.0)

    def get_problem(self, event, target_groups, targets):
        self.check_deprecations()

        if self.decimation_factor != 1:
            logger.warning(
                'Decimation factor for rectangular source set to %i. Results '
                'may be inaccurate.' % self.decimation_factor)

        base_source = gf.RectangularSource.from_pyrocko_event(
            event,
            anchor='top',
            decimation_factor=self.decimation_factor)

        subs = dict(
            event_name=event.name,
            event_time=util.time_to_str(event.time))

        problem = RectangularProblem(
            name=expand_template(self.name_template, subs),
            base_source=base_source,
            target_groups=target_groups,
            targets=targets,
            ranges=self.ranges,
            norm_exponent=self.norm_exponent,
            distance_min=self.distance_min)

        return problem


@has_get_plot_classes
class RectangularProblem(Problem):
    distance_min = Float.T(default=0.0)

    problem_parameters = [
        Parameter('east_shift', 'm', label='Easting', **as_km),
        Parameter('north_shift', 'm', label='Northing', **as_km),
        Parameter('depth', 'm', label='Depth', **as_km),
        Parameter('length', 'm', label='Length', optional=False, **as_km),
        Parameter('width', 'm', label='Width', optional=False, **as_km),
        Parameter('slip', 'm', label='Slip', optional=False),
        Parameter('strike', 'deg', label='Strike'),
        Parameter('dip', 'deg', label='Dip'),
        Parameter('rake', 'deg', label='Rake')
    ]

    problem_waveform_parameters = [
        Parameter('nucleation_x', 'offset', label='Nucleation X'),
        Parameter('nucleation_y', 'offset', label='Nucleation Y'),
        Parameter('time', 's', label='Time'),
        Parameter('velocity', 'm/s', label='Rupture Velocity')
    ]

    dependants = []

    def pack(self, source):
        arr = self.get_parameter_array(source)
        for ip, p in enumerate(self.parameters):
            if p.name == 'time':
                arr[ip] -= self.base_source.time
        return arr

    def get_source(self, x):
        d = self.get_parameter_dict(x)
        p = {}
        for k in self.base_source.keys():
            if k in d:
                p[k] = float(
                    self.ranges[k].make_relative(self.base_source[k], d[k]))

        source = self.base_source.clone(**p)

        return source

    def preconstrain(self, x):
        if self.distance_min != 0.0:
            raise ValueError(
                'RectangularProblem currently cannot handle '
                'distance_min != 0.0.')
        return x

    @classmethod
    def get_plot_classes(cls):
        plots = super(RectangularProblem, cls).get_plot_classes()
        return plots


__all__ = '''
    RectangularProblem
    RectangularProblemConfig
'''.split()
