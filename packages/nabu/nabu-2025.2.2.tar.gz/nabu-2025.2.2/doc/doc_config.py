#!/usr/bin/env python

from nabu.resources.nabu_config import nabu_config


def generate(file_):
    def write(content):
        print(content, file=file_)
    for section, values in nabu_config.items():
        if section == "about":
            continue
        write("## %s\n" % section)
        for key, val in values.items():
            if val["type"] == "unsupported":
                continue
            write(val["help"] + "\n")
            write(
                "```ini\n%s = %s\n```"
                % (key, val["default"])
            )



if __name__ == "__main__":

    import sys, os
    print(os.path.abspath(__file__))
    exit(0)

    fname = "/tmp/test.md"
    with open(fname, "w") as f:
        generate(f)
