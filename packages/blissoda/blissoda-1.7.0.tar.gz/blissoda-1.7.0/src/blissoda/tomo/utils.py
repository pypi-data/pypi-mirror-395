import logging
from enum import IntEnum
from typing import Tuple

import numpy as np

from blissoda.bliss_globals import current_session
from blissoda.import_utils import unavailable_class
from blissoda.import_utils import unavailable_function
from blissoda.import_utils import unavailable_module

try:
    from bliss.physics import units
    from flint.viewers.custom_image.client import ImageView
    from tomo.globals import get_active_tomo_config
except ImportError as ex:
    units = unavailable_module(ex)
    get_active_tomo_config = unavailable_function(ex)
    ImageView = unavailable_class(ex)


logger = logging.getLogger(__name__)


def get_estimate_cor_metadata() -> tuple:
    """Return (pixel_size_mm, detector_width, translation_y_mm) for CoR estimation."""
    config = current_session.config

    tomo_config = get_active_tomo_config()
    tomo_detector = tomo_config.detectors.active_detector
    lima_detector = tomo_config.detectors.get_detector(
        tomo_config.detectors.active_detector
    )

    pixel_size_mm = tomo_detector.sample_pixel_size / 1000  # default mm

    detector_width = lima_detector.image.fullsize[0]

    translation_y_motor = tomo_config.sample_stage.y_axis.name

    translation_y_motor_config = config.get(translation_y_motor)
    translation_y_value = float(translation_y_motor_config.position)
    translation_y_unit = translation_y_motor_config.unit
    try:  # FIX ME: handle case where unit is not recognized
        translation_y_mm = (
            translation_y_value * units.ur(translation_y_unit).to("mm").magnitude
        )
    except Exception:
        translation_y_mm = translation_y_value

    return pixel_size_mm, detector_width, translation_y_mm


def get_reconstruction_metadata(scan) -> tuple:
    """Return (distance_m, energy_keV, pixel_size_m) from scan metadata."""

    technique_info = scan.scan_info["technique"]
    scan_info = technique_info["scan"]

    # Get distance in meters
    distance = float(scan_info["effective_propagation_distance"])
    distance_unit = scan_info.get("effective_propagation_distance@units", "m")
    distance_m = distance * units.ur(distance_unit).to("m").magnitude

    # Get energy in keV
    energy = float(scan_info["energy"])
    energy_unit = scan_info.get("energy@units", "keV")
    energy_keV = energy * units.ur(energy_unit).to("keV").magnitude

    # Get pixel size in meters
    pixel_size = scan_info["sample_pixel_size"]
    pixel_size_unit = scan_info["sample_pixel_size@units"]
    pixel_size_m = pixel_size * units.ur(pixel_size_unit).to("m").magnitude

    return distance_m, energy_keV, pixel_size_m


def calculate_CoR_estimate(
    pixel_size_mm: float,
    translation_y_mm: float,
    detector_width: int,
    offset_mm: float,
    flip: bool,
    orientation_factor: float = 1.0,
) -> float:
    """
    Estimate the center of rotation for tomographic reconstruction.
    """
    # The -0.5 accounts for pixel-center coordinate convention used by the reconstruction algorithm
    default_center = detector_width / 2 - 0.5

    # This tells us how many pixels the center of rotation has shifted
    pixel_shift = (translation_y_mm - offset_mm) / pixel_size_mm

    # Adjust the center of rotation based on the pixel shift and orientation factor
    center_of_rotation = default_center + (pixel_shift * orientation_factor)

    if flip:
        center_of_rotation *= -1

    return center_of_rotation


def calculate_relative_CoR_estimate(
    pixel_size_mm: float,
    translation_y_mm: float,
    offset_mm: float,
    flip: bool,
    orientation_factor: float = 1.0,
) -> float:
    """
    Estimate the relative center of rotation for tomographic reconstruction.
    """

    # This tells us how many pixels the center of rotation has shifted
    pixel_shift = (translation_y_mm - offset_mm) / pixel_size_mm

    # Adjust the center of rotation based on the pixel shift and orientation factor
    relative_center_of_rotation = pixel_shift * orientation_factor

    if flip:
        relative_center_of_rotation *= -1

    return relative_center_of_rotation


class ImageKey(IntEnum):
    PROJECTION = 0
    DARK_FIELD = 2
    FLAT_FIELD = 1
    INVALID = 3


def compute_axes(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute physical axes from sample config; fallback to pixel indices.

    Converts pixel_size (um) to axis units defined by cfg.sample_x_axis.unit
    and cfg.sample_y_axis.unit.

    Parameters
    ----------
    image : np.ndarray
        The image array (for shape information)

    Returns
    -------
    tuple of np.ndarray
        x_axis and y_axis arrays in physical units
    """

    tomo_config = get_active_tomo_config()
    pixel_size_um = tomo_config.detectors.active_detector.sample_pixel_size

    # Determine units for x and y axes
    unit_x = getattr(tomo_config.sample_x_axis, "unit", "mm")
    unit_y = getattr(tomo_config.sample_y_axis, "unit", "mm")

    # Conversion factors from micrometers to axis units
    conv = {"um": 1.0, "mm": 1e-3}
    if unit_x not in conv:
        logger.warning("Unknown unit '%s' for sample_x_axis, assuming 'mm'", unit_x)
    if unit_y not in conv:
        logger.warning("Unknown unit '%s' for sample_y_axis, assuming 'mm'", unit_y)

    # Convert pixel size to axis units
    ps_x = pixel_size_um * conv.get(unit_x, 0.001)
    ps_y = pixel_size_um * conv.get(unit_y, 0.001)

    rows, cols = image.shape[-2:]

    # Center positions are already in axis units
    cx = tomo_config.sample_x_axis.position
    cy = tomo_config.sample_y_axis.position

    half_w = (cols * ps_x) / 2
    half_h = (rows * ps_y) / 2

    x_axis = np.linspace(cx - half_w, cx + half_w, cols)
    y_axis = np.linspace(cy - half_h, cy + half_h, rows)

    return x_axis, y_axis


def apply_labels(widget: ImageView) -> None:
    """
    Apply axis labels from tomo config.

    Parameters
    ----------
    widget : ImageView
        The plot widget
    """
    tomo_config = get_active_tomo_config()
    widget.xlabel = tomo_config.sample_y.name
    widget.ylabel = tomo_config.sample_x.name
