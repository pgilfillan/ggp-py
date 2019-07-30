from src.core.propnet_arch.propnet import PropNet

f = open('games/proptest/proptest.gdl', 'r')
description = f.read()
prop = PropNet(description)
