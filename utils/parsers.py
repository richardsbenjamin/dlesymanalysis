from __future__ import annotations

from argparse import ArgumentParser

from dlesymanalysis._typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dlesymanalysis._typing import Namespace


BASIC_PARSER_ARGS = {
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

CALC_EXTREME_DAYS_ARGS = {
    **BASIC_PARSER_ARGS,
    "ocean-quantiles-path": {
        "type": str,
        "required": True,
        "help": "Zarr path to where the ocean quantiles are saved."
    },
    "atmos-quantiles-path": {
        "type": str,
        "required": True,
        "help": "Zarr path to where the atmos quantiles are saved."
    },
}

FIG_VAR_DISTS_ARGS = {
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
    "singles-path": {
        "type": str,
        "required": True,
        "help": "Zarr path to where to get the ERA5 single levels."
    },
    "fig-save-path": {
        "type": str,
        "required": True,
        "help": "Zarr path to where to save the figure."
    },
}


def get_arg_parser(description: str, args_dict: dict) -> Namespace:
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

def get_calc_avgs_parser() -> Namespace:
    return get_arg_parser(
        description="Calculate the global annual averages.",
        args_dict=BASIC_PARSER_ARGS,
    )

def get_calc_extreme_days_parser_args() -> Namespace:
    return get_arg_parser(
        description="Calculate the number extreme days for all variables and locations",
        args_dict=CALC_EXTREME_DAYS_ARGS,
    )

def get_calc_percentiles_parser() -> Namespace:
    return get_arg_parser(
        description="Calculate the percentiles for each location for each data of year.",
        args_dict=BASIC_PARSER_ARGS,
    )

def get_fig_var_dists_parser() -> Namespace:
    return get_arg_parser(
        description="Generate figure of histograms of first and last decades.",
        args_dict=FIG_VAR_DISTS_ARGS,
    )

def get_spatial_lin_regress_parser() -> Namespace:
    return get_arg_parser(
        description="Calculate drift for each spatial location.",
        args_dict=BASIC_PARSER_ARGS,
    )

def get_stats_calc_parse_args() -> Namespace:
    return get_arg_parser(
        description="Calculate basic stats for each variable.",
        args_dict=BASIC_PARSER_ARGS,
    )


