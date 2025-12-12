from argparse import ArgumentParser


def parse_params_values(Params, parser_description=None, program_version=None, user_args=None):
    parser = ArgumentParser(description=parser_description)
    for param_name, vals in Params.items():
        if param_name[0] != "-":
            # It would be better to use "required" and not to pop it.
            # required is an accepted keyword for argparse
            optional = not (vals.pop("mandatory", False))
            if optional:
                param_name = "--" + param_name
            aliases = vals.pop("aliases", tuple())
            if optional:
                aliases = tuple(["--" + alias for alias in aliases])
        else:
            aliases = ()
        parser.add_argument(param_name, *aliases, **vals)
    if program_version is not None:
        parser.add_argument("--version", "-V", action="version", version=program_version)

    args = parser.parse_args(args=user_args)

    args_dict = args.__dict__
    return args_dict


def parse_sections(sections):
    sections = sections.lower()
    if sections == "all":
        return None
    sections = sections.replace(" ", "").split(",")
    return sections
