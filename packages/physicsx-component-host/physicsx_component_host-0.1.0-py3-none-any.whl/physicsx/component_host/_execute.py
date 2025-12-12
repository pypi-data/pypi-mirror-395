"""Core PXC-002 process execution logic."""

from __future__ import annotations

import json
import traceback
from pathlib import Path
from typing import TextIO

from physicsx.component_host._component import Component


def execute(
    component: Component,
    input_file_path: str,
    output_file_path: str,
    stderr: TextIO,
) -> int:
    """Execute a component by reading JSON input from a file and writing output to a file.

    Args:
        component: The component to execute.
        input_file_path: Path to the input JSON file.
        output_file_path: Path to the output JSON file.
        stderr: Error stream to write error messages to.

    Returns:
        Exit code: 0 on success, 1 on any error.
    """
    try:
        input_text = Path(input_file_path).read_text()
        input_dict = json.loads(input_text)
        validated_input = component.input_type.model_validate(input_dict)
        output = component.function(validated_input)
        output_json = output.model_dump_json()
        Path(output_file_path).write_text(output_json + "\n")
        return 0
    except Exception:
        stderr.write(traceback.format_exc())
        stderr.flush()
        return 1
