from src.core.propnet_arch.propnet import PropNet

f = open('games/proptest/proptest.pl', 'r')
description = f.read()
prop = PropNet(description)