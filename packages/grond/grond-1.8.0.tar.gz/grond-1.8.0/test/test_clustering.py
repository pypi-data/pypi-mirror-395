# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
from .common import grond, run_in_project


def test_clustering():

    def main(env, rundir_path):
        grond('cluster', 'dbscan', rundir_path)

    run_in_project(
        main,
        project_dir_source='example_regional_cmt_full',
        project_dir='example_regional_cmt_full_clustering',
        event_name='gfz2018pmjk',
        config_path='config/regional_cmt_ampspec.gronf')
