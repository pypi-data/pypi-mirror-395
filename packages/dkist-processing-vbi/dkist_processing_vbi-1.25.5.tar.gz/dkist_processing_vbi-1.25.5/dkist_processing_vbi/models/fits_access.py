"""VBI control of FITS key names and values."""

from enum import StrEnum


class VbiMetadataKey(StrEnum):
    """Controlled list of names for FITS metadata header keys."""

    spatial_step_pattern = "VBISTPAT"
    number_of_spatial_steps = "VBINSTP"
    current_spatial_step = "VBISTP"
    number_of_exp_per_mosaic_step = "VBINFRAM"
    current_mosaic_step_exp = "VBICFRAM"
