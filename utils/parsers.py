from argparse import ArgumentParser


CALC_AVGS_PARSER_ARGS = {
    "ocean-store": {
        "type": str,
        "required": True,
        "help": "Zarr path to the DLESyM ocean output."
    },
    "atmos-store": {
        "type": str,
        "required": True,
        "help": "Zarr path to the DLESyM atmos output."
    },
    "ocean-output": {
        "type": str,
        "required": True,
        "help": "Zarr path to where to save the ocean averages."
    },
    "atmos-output": {
        "type": str,
        "required": True,
        "help": "Zarr path to where to save the atmos averages."
    },
}


def get_arg_parser(description: str, args_dict: dict) -> ArgumentParser:
    arg_parser = ArgumentParser(description=description)
    for arg, arg_params in args_dict.items():
        arg_parser.add_argument(
            f'--{arg}',
            type=arg_params["type"],
            required=arg_params["required"],
            help=arg_params["help"],
        )
    run_args = arg_parser.parse_args()
    return run_args

def get_calc_avgs_parser() -> ArgumentParser:
    return get_arg_parser(
        description="Calculate the global annual averages.",
        args_dict=CALC_AVGS_PARSER_ARGS,
    )


