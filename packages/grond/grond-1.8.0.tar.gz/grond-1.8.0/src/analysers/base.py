# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century
from pyrocko.guts import Object

from grond.meta import GrondError

guts_prefix = 'grond'


class Analyser(object):

    def analyse(self, problem, ds):
        pass


class AnalyserConfig(Object):

    def get_analyser(self):
        return Analyser


class AnalyserResult(Object):

    class NoResults(GrondError):
        pass

    pass


__all__ = '''
    Analyser
    AnalyserConfig
'''.split()
