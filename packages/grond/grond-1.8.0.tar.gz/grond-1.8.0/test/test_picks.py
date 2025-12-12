from __future__ import absolute_import


from .common import grond, run_in_project, get_playground_dir, chdir  # noqa

from grond import config


def test_picks_for_time_windows():

    def main(env, rundir_path):

        conf = env.get_config()

        mod_conf = conf.clone()

        mod_conf.target_groups[0].only_use_stations_with_picks = True
        mod_conf.target_groups[1].only_use_stations_with_picks = True

        mod_conf.target_groups[0].misfit_config.pick_synthetic_traveltime =\
            '{stored:any_P}'
        mod_conf.target_groups[0].misfit_config.pick_phasename = 'P'
        mod_conf.target_groups[1].misfit_config.pick_synthetic_traveltime =\
            '{stored:any_P}'
        mod_conf.target_groups[1].misfit_config.pick_phasename = 'P'

        mod_conf.dataset_config.picks_paths =\
            ['data/events/${event_name}/picks/picks_${event_name}.txt']

        mod_conf.optimiser_config.sampler_phases[0].niterations = 100
        mod_conf.optimiser_config.sampler_phases[1].niterations = 100
        mod_conf.optimiser_config.nbootstrap = 10

        mod_conf.set_basepath(conf.get_basepath())

        modconfig_path = 'config/mod_config.gronf'
        config.write_config(mod_conf, modconfig_path)

        grond('go', modconfig_path, '--force')

    run_in_project(
        main,
        project_dir_source='example_regional_cmt_full',
        project_dir='example_regional_cmt_full_picks',
        event_name='gfz2018pmjk',
        config_path='config/regional_cmt.gronf')
