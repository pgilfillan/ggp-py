from src.core.propnet_arch.propnet import PropNet
from test_parser import parse_gdl

f = open('games/proptest/proptest.gdl', 'r')
description = f.read()
#prop = PropNet(description)
parse_gdl(description)