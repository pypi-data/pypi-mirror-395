"""Util module."""

import logging
import typing as t
from pathlib import Path

# import pytz

AnyPath = t.Union[str, Path]

log = logging.getLogger(__name__)


def get_or_create_acquisition(session, label, update=True, **kwargs):
    """Get the Acquisition container if it exists, else create a new Acquisition container.

    Args:
        session (flywheel.Session): A Flywheel Session.
        label (str): The Acquisition label.
        update (bool): If true, update container with key/value passed as kwargs.
        kwargs (dict): Any key/value properties of Acquisition you would like to update.

    Returns:
        (flywheel.Acquisition): A Flywheel Acquisition container.
    """

    if not label:
        raise ValueError(f"label is required (currently {label})")

    acquisition = session.acquisitions.find_first(f"label={label}")
    if not acquisition:
        acquisition = session.add_acquisition(label=label)

    if update and kwargs:
        acquisition.update(**kwargs)

    if acquisition:
        acquisition = acquisition.reload()

    return acquisition


def get_acq_labels(ses: str) -> list:
    """Get acq labels for a give session."""

    acq_labels = []
    for label in ses.acquisitions.iter():
        acq_labels.append(label.get("label"))

    return acq_labels
