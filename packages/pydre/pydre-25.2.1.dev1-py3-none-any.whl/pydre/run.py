from loguru import logger
from pydre import project
import sys
import argparse
from typing import List, Optional


def parse_arguments(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Set up argparse based parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--projectfile", type=str, help="the project file path", required=True
    )
    parser.add_argument(
        "-d", "--datafiles", type=str, help="the data file path", nargs="+"
    )
    parser.add_argument(
        "-o",
        "--outputfile",
        type=str,
        help="the name of the output file",
        default="out.csv",
    )
    parser.add_argument(
        "-l",
        "--warninglevel",
        type=str,
        default="WARNING",
        help="Loggging error level. DEBUG, INFO, WARNING, ERROR, and CRITICAL are allowed.",
    )
    return parser.parse_args(args)


def setup_logging(level: str) -> str:
    """Set up logging with the specified level."""
    logger.remove()
    level = level.upper()
    accepted_levels = ["DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
    if level in accepted_levels:
        logger.add(sys.stderr, level=level)
        return level
    else:
        logger.add(sys.stderr, level="WARNING")
        logger.warning("Command line log level (-l) invalid. Defaulting to WARNING")
        return "WARNING"


def run_project(
    projectfile: str,
    datafiles: Optional[List[str]],
    outputfile: Optional[str],
    num_threads: int = 12,
) -> project.Project:
    """Create, process and save a project."""
    p = project.Project(projectfile, datafiles, outputfile)
    p.processDatafiles(numThreads=num_threads)
    p.saveResults()
    return p


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the application."""
    try:
        parsed_args = parse_arguments(args)
        setup_logging(parsed_args.warninglevel)
        run_project(
            parsed_args.projectfile, parsed_args.datafiles, parsed_args.outputfile
        )
        return 0
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        return 1


def pydre():
    sys.exit(main())


if __name__ == "__main__":
    pydre()
