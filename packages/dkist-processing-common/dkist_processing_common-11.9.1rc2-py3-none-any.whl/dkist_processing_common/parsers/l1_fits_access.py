"""By-frame 214 L1 only header keywords that are not instrument specific."""

from astropy.io import fits

from dkist_processing_common.models.fits_access import HEADER_KEY_NOT_FOUND
from dkist_processing_common.models.fits_access import FitsAccessBase
from dkist_processing_common.models.fits_access import MetadataKey

NOT_A_FLOAT = -999


class L1FitsAccess(FitsAccessBase):
    """
    Class defining a fits access object for processed L1 data.

    Parameters
    ----------
    hdu
        The input fits hdu
    name
        An optional name to be associated with the hdu
    auto_squeeze
        A boolean indicating whether to 'squeeze' out dimensions of size 1
    """

    def __init__(
        self,
        hdu: fits.ImageHDU | fits.PrimaryHDU | fits.CompImageHDU,
        name: str | None = None,
        auto_squeeze: bool = False,  # Because L1 data should always have the right form, right?
    ):
        super().__init__(hdu=hdu, name=name, auto_squeeze=auto_squeeze)

        self.elevation: float = self.header[MetadataKey.elevation]
        self.azimuth: float = self.header[MetadataKey.azimuth]
        self.table_angle: float = self.header[MetadataKey.table_angle]
        self.gos_level3_status: str = self.header[MetadataKey.gos_level3_status]
        self.gos_level3_lamp_status: str = self.header[MetadataKey.gos_level3_lamp_status]
        self.gos_polarizer_status: str = self.header[MetadataKey.gos_polarizer_status]
        self.gos_retarder_status: str = self.header[MetadataKey.gos_retarder_status]
        self.gos_level0_status: str = self.header[MetadataKey.gos_level0_status]
        self.time_obs: str = self.header[MetadataKey.time_obs]
        self.ip_id: str = self.header[MetadataKey.ip_id]
        self.instrument: str = self.header[MetadataKey.instrument]
        self.wavelength: float = self.header[MetadataKey.wavelength]
        self.proposal_id: str = self.header[MetadataKey.proposal_id]
        self.experiment_id: str = self.header[MetadataKey.experiment_id]
        self.num_dsps_repeats: int = self.header[MetadataKey.num_dsps_repeats]
        self.current_dsps_repeat: int = self.header[MetadataKey.current_dsps_repeat]
        self.fpa_exposure_time_ms: float = self.header[MetadataKey.fpa_exposure_time_ms]
        self.sensor_readout_exposure_time_ms: float = self.header[
            MetadataKey.sensor_readout_exposure_time_ms
        ]
        self.num_raw_frames_per_fpa: int = self.header[MetadataKey.num_raw_frames_per_fpa]
        self.camera_id: str = self.header[MetadataKey.camera_id]
        self.camera_name: str = self.header[MetadataKey.camera_name]
        self.camera_bit_depth: int = self.header[MetadataKey.camera_bit_depth]
        self.hardware_binning_x: int = self.header[MetadataKey.hardware_binning_x]
        self.hardware_binning_y: int = self.header[MetadataKey.hardware_binning_y]
        self.software_binning_x: int = self.header[MetadataKey.software_binning_x]
        self.software_binning_y: int = self.header[MetadataKey.software_binning_y]
        self.observing_program_execution_id: str = self.header[
            MetadataKey.observing_program_execution_id
        ]
        self.telescope_tracking_mode: str = self.header.get(
            MetadataKey.telescope_tracking_mode, HEADER_KEY_NOT_FOUND
        )
        self.coude_table_tracking_mode: str = self.header.get(
            MetadataKey.coude_table_tracking_mode, HEADER_KEY_NOT_FOUND
        )
        self.telescope_scanning_mode: str = self.header.get(
            MetadataKey.telescope_scanning_mode, HEADER_KEY_NOT_FOUND
        )
        self.light_level: float = self.header[MetadataKey.light_level]
        self.hls_version: str = self.header[MetadataKey.hls_version]

    @property
    def gos_polarizer_angle(self) -> float:
        """Convert the polarizer angle to a float if possible before returning."""
        try:
            return float(self.header[MetadataKey.gos_polarizer_angle])
        except ValueError:
            return NOT_A_FLOAT  # The angle is only used if the polarizer is in the beam

    @property
    def gos_retarder_angle(self) -> float:
        """Convert the retarder angle to a float if possible before returning."""
        try:
            return float(self.header[MetadataKey.gos_retarder_angle])
        except ValueError:
            return NOT_A_FLOAT  # The angle is only used if the retarder is in the beam
