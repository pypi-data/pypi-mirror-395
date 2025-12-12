#!/usr/bin/env python

import time
import os.path as op

from pkg_resources import parse_version as pv

from setuptools import setup, __version__ as setuptools_version
from setuptools.command.build_py import build_py

have_pep621_support = pv(setuptools_version) >= pv('61.0.0')

version = '1.8.0'


class NotInAGitRepos(Exception):
    pass


def git_infos():
    '''Query git about sha1 of last commit and check if there are local \
       modifications.'''

    from subprocess import Popen, PIPE
    import re

    def q(c):
        return Popen(c, stdout=PIPE).communicate()[0]

    if not op.exists('.git'):
        raise NotInAGitRepos()

    sha1 = q(['git', 'log', '--pretty=oneline', '-n1']).split()[0]
    sha1 = re.sub(br'[^0-9a-f]', '', sha1)
    sha1 = str(sha1.decode('ascii'))
    sstatus = q(['git', 'status', '--porcelain', '-uno'])
    local_modifications = bool(sstatus.strip())
    return sha1, local_modifications


def make_info_module(packname, version, outfile):
    '''Put version and revision information into file src/setup_info.py.'''

    sha1, local_modifications = None, None
    combi = '%s_%s' % (packname, version)
    try:
        sha1, local_modifications = git_infos()
        combi += '_%s' % sha1
        if local_modifications:
            combi += '_modified'

    except (OSError, NotInAGitRepos):
        pass

    datestr = time.strftime('%Y-%m-%d_%H:%M:%S')
    combi += '_%s' % datestr

    module_code = '''# This module is automatically created from setup.py
git_sha1 = %s
local_modifications = %s
version = %s
long_version = %s  # noqa
installed_date = %s
''' % tuple([repr(x) for x in (
        sha1, local_modifications, version, combi, datestr)])

    with open(outfile, 'w') as f:
        f.write(module_code)


class CustomBuildPyCommand(build_py):

    def run(self):
        outfile = self.get_module_outfile(
            self.build_lib, ['grond'], 'setup_info')
        dir_ = op.dirname(outfile)
        self.mkpath(dir_)
        make_info_module('grond', version, outfile)
        build_py.run(self)


if not have_pep621_support:
    metadata = dict(
        name='grond',
        description='A probabilistic earthquake source inversion framework. '
                    'Designed and crafted in Mordor.',
        url='https://pyrocko.org/grond/',
        python_requires='>=3.10, <4',
        version=version,
        author='The Grond Developers',
        author_email='info@pyrocko.org',
        entry_points={
            'console_scripts': [
                'grond = grond.apps.grond:main',
            ]
        },
        install_requires=['pyrocko>=2025.01.21'],
        license='GPLv3',
        classifiers=[
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: Implementation :: CPython',
            'Operating System :: POSIX',
            'Operating System :: MacOS',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Physics',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: Software Development :: Libraries :: Application '
            'Frameworks',
            ],
        keywords=[
            'seismology, waveform analysis, earthquake modelling, geophysics,'
            ' geophysical inversion'],
    )

else:
    metadata = {}


setup(
    cmdclass={
        'build_py': CustomBuildPyCommand,
    },
    name='grond',
    version=version,
    packages=[
        'grond',
        'grond.apps',
        'grond.targets',
        'grond.targets.waveform',
        'grond.targets.waveform_phase_ratio',
        'grond.targets.waveform_oac',
        'grond.targets.satellite',
        'grond.targets.gnss_campaign',
        'grond.targets.phase_pick',
        'grond.problems',
        'grond.problems.cmt',
        'grond.problems.locate',
        'grond.problems.double_dc',
        'grond.problems.rectangular',
        'grond.problems.volume_point',
        'grond.problems.vlvd',
        'grond.problems.singleforce',
        'grond.problems.double_sf',
        'grond.problems.simple_landslide',
        'grond.optimisers',
        'grond.optimisers.highscore',
        'grond.analysers',
        'grond.analysers.noise_analyser',
        'grond.analysers.target_balancing',
        'grond.report',
        'grond.plot',
        'grond.clustering',
    ],
    package_dir={'grond': 'src'},
    include_package_data=False,
    package_data={
        'grond': [
            'report/app/*.html',
            'report/app/favicon.png',
            'report/app/templates/*.html',
            'report/app/css/*.css',
            'report/app/js/*.js',

            'data/snippets/*.gronf',
            'data/snippets/*.md',
            'data/examples/*/*.*',
            'data/examples/*/*/*.*',
            'data/examples/*/*/grondown',
            ]},
    **metadata)
