import re


def parse_gdl(description):
    description = description.strip()
    for line in description.splitlines():
        line = line.strip()
        print("Line:", line)
        if re.search(r'<=', line):
            search = re.search(r'\(<= ([a-z]+) (.*)\)', line)
            if search is not None:
                print(search.groups())
        else:
            search = re.search(r'\(([a-z]+) (.*)\)', line)
            if search is not None:
                print(search.groups())
