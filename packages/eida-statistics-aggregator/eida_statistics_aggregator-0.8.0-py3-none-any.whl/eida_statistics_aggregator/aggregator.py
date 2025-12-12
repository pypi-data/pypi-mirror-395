"""
Aggregate and submit metadata
"""

import gzip
import logging
import sys
from pathlib import Path
from importlib.metadata import version

import click
import requests

from eida_statistics_aggregator.stat_collection import StatCollection

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
logger = logging.getLogger()


def proj_version():
    return version("eida_statistics_aggregator")


@click.command()
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(exists=True, dir_okay=True, resolve_path=True),
    help="File name prefix to write the statistics to. The full output file will be prefix_START_END.json.gz",
    default="/tmp",
)
@click.option(
    "--token",
    help="Your EIDA token to the statistics webservice. Can be set by TOKEN environment variable",
    default="",
    envvar="TOKEN",
)
@click.option("--send-to", help="EIDA statistics webservice to post the result.")
@click.option("--version", is_flag=True)
@click.argument("files", type=click.Path(exists=True), nargs=-1)
def cli(files, output_directory, token, send_to, version):
    """
    Command line interface
    """
    if version:
        print(proj_version())
        sys.exit(0)
    statistics = StatCollection()
    for f in files:
        statistics.parse(f)

    logger.info(
        "Generated %s aggregations from %s events. Aggregation score is %s",
        statistics.nbaggs(),
        statistics.nbevents,
        round(statistics.nbevents / statistics.nbaggs(), 1),
    )
    # get start and end of statistics
    # sort statistics_dict by key, get first and last entry
    sorted_list = statistics.get_days()
    output_file = f"{output_directory}/{sorted_list[0]}_{sorted_list[-1]}.json.gz"
    logger.debug("Statistics will be stored to Gzipped file %s", output_file)

    payload = gzip.compress(statistics.to_json().encode("utf-8"))
    with Path.open(output_file, "wb") as dumpfile:
        dumpfile.write(payload)
        logger.info("Statistics stored to %s", output_file)

    if send_to is not None and token is not None:
        logger.info("Posting stat file %s to %s", output_file, send_to)
        headers = {
            "Authentication": "Bearer " + token,
            "Content-Type": "application/json",
        }
        r = requests.post(
            send_to, data=statistics.to_json(), headers=headers, timeout=600
        )
        logger.info(r.text)
