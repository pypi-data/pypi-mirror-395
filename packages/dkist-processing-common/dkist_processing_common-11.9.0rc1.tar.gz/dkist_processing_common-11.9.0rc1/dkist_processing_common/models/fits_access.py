"""Abstraction layer for accessing fits data via class attributes."""

from __future__ import annotations

from enum import StrEnum
from enum import unique
from pathlib import Path

import numpy as np
from astropy.io import fits

HEADER_KEY_NOT_FOUND = "HEADER_KEY_NOT_FOUND"


@unique
class MetadataKey(StrEnum):
    """Controlled list of names for FITS metadata header keys."""

    ip_task_type = "IPTASK"  # in L0FitsAccess
    ip_start_time = "DKIST011"  # in L0FitsAccess
    ip_end_time = "DKIST012"  # in L0FitsAccess
    elevation = "ELEV_ANG"
    azimuth = "TAZIMUTH"
    table_angle = "TTBLANGL"
    gos_level3_status = "LVL3STAT"
    gos_level3_lamp_status = "LAMPSTAT"
    gos_polarizer_status = "LVL2STAT"
    gos_polarizer_angle = "POLANGLE"
    gos_retarder_status = "LVL1STAT"
    gos_retarder_angle = "RETANGLE"
    gos_level0_status = "LVL0STAT"
    time_obs = "DATE-BEG"
    ip_id = "IP_ID"
    instrument = "INSTRUME"
    wavelength = "LINEWAV"
    proposal_id = "PROP_ID"
    experiment_id = "EXPER_ID"
    num_dsps_repeats = "DSPSREPS"
    current_dsps_repeat = "DSPSNUM"
    fpa_exposure_time_ms = "XPOSURE"
    sensor_readout_exposure_time_ms = "TEXPOSUR"
    num_raw_frames_per_fpa = "NSUMEXP"
    camera_id = "CAM_ID"
    camera_name = "CAMERA"
    camera_bit_depth = "BITDEPTH"
    hardware_binning_x = "HWBIN1"
    hardware_binning_y = "HWBIN2"
    software_binning_x = "SWBIN1"
    software_binning_y = "SWBIN2"
    observing_program_execution_id = "OBSPR_ID"
    telescope_tracking_mode = "TELTRACK"
    coude_table_tracking_mode = "TTBLTRCK"
    telescope_scanning_mode = "TELSCAN"
    light_level = "LIGHTLVL"
    hls_version = "HLSVERS"


class FitsAccessBase:
    """
    Abstraction layer for accessing fits data via class attributes.

    Parameters
    ----------
    hdu
        The fits object
    name
        An optional name that can be associated with the object
    auto_squeeze
        A boolean indicating whether to 'squeeze' out dimensions of size 1
    """

    def __init__(
        self,
        hdu: fits.ImageHDU | fits.PrimaryHDU | fits.CompImageHDU,
        name: str | Path | None = None,
        auto_squeeze: bool = True,
    ):
        self._hdu = hdu
        self.name = name
        self.auto_squeeze = auto_squeeze

    def __repr__(self):
        return f"{self.__class__.__name__}(hdu={self._hdu!r}, name={self.name!r}, auto_squeeze={self.auto_squeeze})"

    @property
    def data(self) -> np.ndarray:
        """
        Return the data array from the associated FITS object, with axes of length 1 removed if the array has three dimensions and the unit axis is the zeroth one.

        This is intended solely to remove the dummy dimension that is in raw data from the summit.

        Setting `auto_squeeze = False` when initializing this object will never squeeze out any dimensions

        Returns
        -------
        data array
        """
        # This conditional is explicitly to catch summit data with a dummy first axis for WCS
        # purposes
        if self.auto_squeeze and len(self._hdu.data.shape) == 3 and self._hdu.data.shape[0] == 1:
            return np.squeeze(self._hdu.data)
        return self._hdu.data

    @data.setter
    def data(self, array: np.ndarray) -> None:
        """
        Set the data array using an input data array.

        Parameters
        ----------
        array
            The input array

        Returns
        -------
        None
        """
        # There is no shape magic stuff going on here right now because the tasks/services that care about
        # it will deal with it themselves (I think (tm)).
        self._hdu.data = array

    @property
    def header(self) -> fits.Header:
        """Return the header for this fits object."""
        return self._hdu.header

    @property
    def header_dict(self) -> dict:
        """Return the header as a dict for this fits object with the special card values (HISTORY, COMMENT) as strings."""
        result = {}
        for card, value in self.header.items():
            if not isinstance(value, (int, float, str, bool)):
                result[card] = str(value)
            else:
                result[card] = value
        return result

    @property
    def size(self) -> float:
        """Return the size in bytes of the data portion of this fits object."""
        return self._hdu.size

    @classmethod
    def from_header(cls, header: fits.Header | dict, name: str | None = None) -> FitsAccessBase:
        """
        Convert a header to a FitsAccessBase (or child) object.

        Parameters
        ----------
        header
            A single `astropy.io.fits.header.Header` HDU object.
        name
            A unique name for the fits access instance
        """
        if isinstance(header, dict):
            header = fits.Header(header)
        hdu = fits.PrimaryHDU()

        # We need to update the header after `PrimaryHDU` instantiation because some of the FITS controlled keys
        # (e.g., NAXIS, NAXISn) would otherwise be changed by checks that occur during instantiation.
        hdu.header.update(header)
        return cls(hdu=hdu, name=name)

    @classmethod
    def from_path(cls, path: str | Path) -> FitsAccessBase:
        """
        Load the file at given path into a FitsAccess object.

        Parameters
        ----------
        path
            Location of fits file on disk
        """
        hdul = fits.open(path)
        if hdul[0].data is not None:
            hdu = hdul[0]
        else:
            hdu = hdul[1]
        return cls(hdu=hdu, name=path)
