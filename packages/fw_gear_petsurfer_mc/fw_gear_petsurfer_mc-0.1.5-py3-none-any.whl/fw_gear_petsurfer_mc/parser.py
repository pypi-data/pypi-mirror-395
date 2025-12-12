"""Parser module to parse gear config.json."""

import os
from datetime import datetime
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
):
    """Gets the project ID from context and the included session IDs and pattern for nifti filtering

    Returns:
        destination, in_dir, in_file, analysis_label
    """
    # updating analysis label
    now = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    analysis_label = f'{gear_context.manifest.get("name")} - {now}'
    destination = gear_context.get_destination_container()
    # destination = gear_context.get_destination_parent()

    # get input directory
    in_dir = os.path.dirname(
        gear_context.get_input("input-file").get("location")["path"]
    )

    in_file = gear_context.get_input("input-file").get("location")["name"]
    template_creation = gear_context.config.get("template_creation")
    frame_pattern = gear_context.config.get("frame_pattern")
    frame_number = gear_context.config.get("ref_frame")

    return (
        destination,
        Path(in_dir),
        Path(in_file),
        analysis_label,
        template_creation,
        frame_pattern,
        frame_number,
    )
