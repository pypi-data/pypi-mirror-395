from collections import OrderedDict

from trap import cli

HEADER = """.. _input_arguments:

Input arguments
===============

This section includes a list of arguments that can be passed to trap-run.
Equivalent information can be shown in the terminal by running `trap-run --help`.

The arguments can be modified in the configuration file (default: trap_config.toml) or
via the command line. The arguments supplied on the command line take precedence.

"""


def sanetize_help_info(help_info):
    return " ".join([line.strip() for line in help_info.split("\n")])


def write_argument_rst(file_path):

    # Get argument descriptions
    parser = cli.construct_argument_parser()
    arg_descriptions = OrderedDict()
    for argument in parser._actions:
        if argument.option_strings:  # Ignore positional arguments
            arg_name = ", ".join(argument.option_strings)  # e.g., "-h, --help"
            if argument.help is None:
                raise ValueError(f"No help found for argument {arg_name}")
            section_name = argument.container.title
            section = arg_descriptions.get(section_name, OrderedDict())
            section[arg_name] = sanetize_help_info(argument.help)
            arg_descriptions[section_name] = section

    # Write output to file
    with open(file_path, "w") as file:
        file.write(HEADER)
        for section_name, section_args in arg_descriptions.items():
            file.write(f"\n**{section_name}**\n")
            for arg, description in section_args.items():
                file.write(f" - **{arg}**: {description}\n")
    return file_path
