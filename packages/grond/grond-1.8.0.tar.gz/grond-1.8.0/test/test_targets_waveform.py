# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
import pytest

from pyrocko import gf

from .common import grond, run_in_project  # noqa
from grond import PhaseMissError


def test_phase_hole():

    def main(env, rundir_path):

        conf = env.get_config()

        mod_conf = conf.clone()

        mod_conf.target_groups[0].misfit_config.tmin = gf.Timing('{cake:p}')
        mod_conf.set_basepath(conf.get_basepath())

        event_name = env.get_current_event_name()
        event = mod_conf.get_dataset(event_name).get_event()

        problem = mod_conf.get_problem(event)
        x = problem.preconstrain(problem.get_reference_model())

        with pytest.raises(PhaseMissError):
            problem.evaluate(x)

    run_in_project(
        main,
        project_dir_source='example_regional_cmt_full',
        project_dir='example_regional_cmt_full_phase_hole',
        event_name='gfz2018pmjk',
        config_path='config/regional_cmt_ampspec.gronf')
