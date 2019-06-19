import re


def gdl_to_prolog(file):

    i = 0
    output = ""
    f = open(file)
    for line in f.readlines():
        print("line:", line)
        i+=1
        if i == 3:
            return output

        if re.match(r'^\s*$', line):
            continue
        elif re.match(r'\(<=', line):
            pass
        else:
            groups = re.search(r'([a-z]+)', line)
            print(groups)
            print(groups.group(0), groups.group(1))