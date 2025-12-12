# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
from pyrocko import gf
import grond
from grond.toy import scenario, ToyProblem
from . import common
from .common import chdir


def test_optimise_toy(dump=False, reference=None):
    source, targets = scenario('wellposed', 'noisefree')

    p = ToyProblem(
        name='toy_problem',
        ranges={
            'north': gf.Range(start=-10., stop=10.),
            'east': gf.Range(start=-10., stop=10.),
            'depth': gf.Range(start=0., stop=10.)},
        base_source=source,
        targets=targets)

    optimiser = grond.HighScoreOptimiser(
        nbootstrap=10,
        sampler_phases=[
            grond.UniformSamplerPhase(niterations=1000),
            grond.DirectedSamplerPhase(niterations=5000)])

    playground_dir = common.get_playground_dir()
    with chdir(playground_dir):
        rundir = 'toy'
        optimiser.init_bootstraps(p)
        p.dump_problem_info(rundir)
        optimiser.optimise(p, rundir=rundir)
