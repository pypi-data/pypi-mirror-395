# https://pyrocko.org/grond - GPLv3
#
# The Grond Developers, 21st Century

def light(color, factor=0.5):
    return tuple(1-(1-c)*factor for c in color)


def dark(color, factor=0.5):
    return tuple(c*factor for c in color)
