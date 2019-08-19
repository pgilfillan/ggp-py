from src.core.propnet_arch.propnet import PropNet
from src.core.propnet_arch.util import parse_gdl
from src.core.propnet_arch.node import props_split

f = open('games/proptest2/proptest2.gdl', 'r')
description = f.read()
out = parse_gdl(description)
print("Out is:")
for o in out:
    print("Term:", o[0], "Conditions:", o[1])
