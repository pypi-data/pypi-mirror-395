from os import path, environ
from glob import glob
from ..utils import get_folder_path
from ..pipeline.config import generate_nabu_configfile, parse_nabu_config_file
from ..pipeline.fullfield.nabu_config import nabu_config as default_fullfield_config
from ..pipeline.helical.nabu_config import nabu_config as helical_fullfield_config
from .utils import parse_params_values
from .cli_configs import BootstrapConfig


def bootstrap():
    args = parse_params_values(BootstrapConfig, parser_description="Initialize a nabu configuration file")

    do_bootstrap = bool(args["bootstrap"])
    no_comments = bool(args["nocomments"])
    overwrite = bool(args["overwrite"])

    if do_bootstrap:
        print(
            "The --bootstrap option is now the default behavior of the nabu-config command. This option is therefore not needed anymore."
        )
    if path.isfile(args["output"]) and not (overwrite):
        rep = input("File %s already exists. Overwrite ? [y/N]" % args["output"])
        if rep.lower() != "y":
            print("Stopping")
            exit(0)

    opts_level = args["level"]

    prefilled_values = {}
    template_name = args["template"]
    if template_name != "":
        prefilled_values = get_config_template(template_name, if_not_found="print")
        if prefilled_values is None:
            exit(0)
        opts_level = "advanced"

    if args["dataset"] != "":
        prefilled_values["dataset"] = {}
        user_dataset = args["dataset"]
        if not path.isabs(user_dataset):
            user_dataset = path.abspath(user_dataset)
            print("Warning: using absolute dataset path %s" % user_dataset)
        if not path.exists(user_dataset):
            print("Error: cannot find the file or directory %s" % user_dataset)
            exit(1)
        prefilled_values["dataset"]["location"] = user_dataset

    if args["helical"]:
        my_config = helical_fullfield_config
    else:
        my_config = default_fullfield_config

    generate_nabu_configfile(
        args["output"],
        my_config,
        comments=not (no_comments),
        options_level=opts_level,
        prefilled_values=prefilled_values,
    )
    return 0


def get_config_template(template_name, if_not_found="raise"):
    def handle_not_found(msg):
        if if_not_found == "raise":
            raise FileNotFoundError(msg)
        elif if_not_found == "print":
            print(msg)

    templates_path = get_folder_path(path.join("resources", "templates"))

    custom_templates_path = environ.get("NABU_TEMPLATES_PATH", None)
    templates = glob(path.join(templates_path, "*.conf"))
    if custom_templates_path is not None:
        templates_custom = glob(path.join(custom_templates_path, "*.conf"))
        templates_custom += glob(path.join(custom_templates_path, "*.cfg"))
        templates = templates_custom + templates

    available_templates_names = [path.splitext(path.basename(fname))[0] for fname in templates]

    if template_name not in available_templates_names:
        handle_not_found("Unable to find template '%s'. Available are: %s" % (template_name, available_templates_names))
        return

    fname = templates[available_templates_names.index(template_name)]
    return parse_nabu_config_file(fname)
