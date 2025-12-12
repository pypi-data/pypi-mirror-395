from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from physicsx.component_host._component import resolve_component
from physicsx.component_host._entrypoint import resolve_entrypoint
from physicsx.component_host._execute import execute


def main(argv: Sequence[str] | None = None) -> int:
    """Run a PhysicsX component by its component name.

    Args:
        argv: Command-line arguments. If None, uses sys.argv.

    Returns:
        Exit code from the component execution.
    """
    parser = argparse.ArgumentParser(
        prog="physicsx-component-host",
        description="Run a PhysicsX component by its component name",
    )
    parser.add_argument(
        "--component-name",
        required=True,
        dest="component_name",
        help="Component name to identify and load the component",
    )
    parser.add_argument(
        "--input-file-path",
        required=True,
        dest="input_file_path",
        help="Path to input JSON file",
    )
    parser.add_argument(
        "--output-file-path",
        required=True,
        dest="output_file_path",
        help="Path to output JSON file",
    )

    args = parser.parse_args(argv)

    function = resolve_entrypoint(args.component_name).load()
    component = resolve_component(function)

    exit_code = execute(
        component=component,
        input_file_path=args.input_file_path,
        output_file_path=args.output_file_path,
        stderr=sys.stderr,
    )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
