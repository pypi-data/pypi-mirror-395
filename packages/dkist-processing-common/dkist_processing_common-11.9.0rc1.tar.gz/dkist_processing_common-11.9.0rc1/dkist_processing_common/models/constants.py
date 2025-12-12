"""
Components of the Constant model.

Contains names of database entries and Base class for an object that simplifies
accessing the database (tab completion, etc.)
"""

from enum import StrEnum
from enum import unique
from string import ascii_uppercase

from sqids import Sqids

from dkist_processing_common._util.constants import ConstantsDb


@unique
class BudName(StrEnum):
    """Controlled list of names for constant stems (buds)."""

    instrument = "INSTRUMENT"
    num_cs_steps = "NUM_CS_STEPS"
    num_modstates = "NUM_MODSTATES"
    retarder_name = "RETARDER_NAME"
    proposal_id = "PROPOSAL_ID"
    contributing_proposal_ids = "CONTRIBUTING_PROPOSAL_IDS"
    experiment_id = "EXPERIMENT_ID"
    contributing_experiment_ids = "CONTRIBUTING_EXPERIMENT_IDS"
    obs_ip_start_time = "OBS_IP_START_TIME"
    average_cadence = "AVERAGE_CADENCE"
    maximum_cadence = "MAXIMUM_CADENCE"
    minimum_cadence = "MINIMUM_CADENCE"
    variance_cadence = "VARIANCE_CADENCE"
    num_dsps_repeats = "NUM_DSPS_REPEATS"
    dark_exposure_times = "DARK_EXPOSURE_TIMES"
    dark_readout_exp_times = "DARK_READOUT_EXP_TIMES"
    wavelength = "WAVELENGTH"
    camera_id = "CAMERA_ID"
    camera_name = "CAMERA_NAME"
    camera_bit_depth = "CAMERA_BIT_DEPTH"
    hardware_binning_x = "HARDWARE_BINNING_X"
    hardware_binning_y = "HARDWARE_BINNING_Y"
    software_binning_x = "SOFTWARE_BINNING_X"
    software_binning_y = "SOFTWARE_BINNING_Y"
    hls_version = "HLS_VERSION"
    # Multi-task buds start here:
    dark_observing_program_execution_ids = "DARK_OBSERVING_PROGRAM_EXECUTION_IDS"
    solar_gain_observing_program_execution_ids = "SOLAR_GAIN_OBSERVING_PROGRAM_EXECUTION_IDS"
    polcal_observing_program_execution_ids = "POLCAL_OBSERVING_PROGRAM_EXECUTION_IDS"
    dark_date_begin = "DARK_DATE_BEGIN"
    solar_gain_date_begin = "SOLAR_GAIN_DATE_BEGIN"
    polcal_date_begin = "POLCAL_DATE_BEGIN"
    dark_date_end = "DARK_DATE_END"
    solar_gain_date_end = "SOLAR_GAIN_DATE_END"
    polcal_date_end = "POLCAL_DATE_END"
    solar_gain_num_raw_frames_per_fpa = "SOLAR_GAIN_NUM_RAW_FRAMES_PER_FPA"
    polcal_num_raw_frames_per_fpa = "POLCAL_NUM_RAW_FRAMES_PER_FPA"
    solar_gain_telescope_tracking_mode = "SOLAR_GAIN_TELESCOPE_TRACKING_MODE"
    polcal_telescope_tracking_mode = "POLCAL_TELESCOPE_TRACKING_MODE"
    solar_gain_coude_table_tracking_mode = "SOLAR_GAIN_COUDE_TABLE_TRACKING_MODE"
    polcal_coude_table_tracking_mode = "POLCAL_COUDE_TABLE_TRACKING_MODE"
    solar_gain_telescope_scanning_mode = "SOLAR_GAIN_TELESCOPE_SCANNING_MODE"
    polcal_telescope_scanning_mode = "POLCAL_TELESCOPE_SCANNING_MODE"
    dark_average_light_level = "DARK_AVERAGE_LIGHT_LEVEL"
    solar_gain_average_light_level = "SOLAR_GAIN_AVERAGE_LIGHT_LEVEL"
    polcal_average_light_level = "POLCAL_AVERAGE_LIGHT_LEVEL"
    dark_average_telescope_elevation = "DARK_AVERAGE_TELESCOPE_ELEVATION"
    solar_gain_average_telescope_elevation = "SOLAR_GAIN_AVERAGE_TELESCOPE_ELEVATION"
    polcal_average_telescope_elevation = "POLCAL_AVERAGE_TELESCOPE_ELEVATION"
    dark_average_coude_table_angle = "DARK_AVERAGE_COUDE_TABLE_ANGLE"
    solar_gain_average_coude_table_angle = "SOLAR_GAIN_AVERAGE_COUDE_TABLE_ANGLE"
    polcal_average_coude_table_angle = "POLCAL_AVERAGE_COUDE_TABLE_ANGLE"
    dark_average_telescope_azimuth = "DARK_AVERAGE_TELESCOPE_AZIMUTH"
    solar_gain_average_telescope_azimuth = "SOLAR_GAIN_AVERAGE_TELESCOPE_AZIMUTH"
    polcal_average_telescope_azimuth = "POLCAL_AVERAGE_TELESCOPE_AZIMUTH"
    dark_gos_level3_status = "DARK_GOS_LEVEL3_STATUS"
    solar_gain_gos_level3_status = "SOLAR_GAIN_GOS_LEVEL3_STATUS"
    dark_gos_level3_lamp_status = "DARK_GOS_LEVEL3_LAMP_STATUS"
    solar_gain_gos_level3_lamp_status = "SOLAR_GAIN_GOS_LEVEL3_LAMP_STATUS"
    dark_gos_polarizer_status = "DARK_GOS_POLARIZER_STATUS"
    solar_gain_gos_polarizer_status = "SOLAR_GAIN_GOS_POLARIZER_STATUS"
    dark_gos_polarizer_angle = "DARK_GOS_POLARIZER_ANGLE"
    solar_gain_gos_polarizer_angle = "SOLAR_GAIN_GOS_POLARIZER_ANGLE"
    dark_gos_retarder_status = "DARK_GOS_RETARDER_STATUS"
    solar_gain_gos_retarder_status = "SOLAR_GAIN_GOS_RETARDER_STATUS"
    dark_gos_retarder_angle = "DARK_GOS_RETARDER_ANGLE"
    solar_gain_gos_retarder_angle = "SOLAR_GAIN_GOS_RETARDER_ANGLE"
    dark_gos_level0_status = "DARK_GOS_LEVEL0_STATUS"
    solar_gain_gos_level0_status = "SOLAR_GAIN_GOS_LEVEL0_STATUS"


class ConstantsBase:
    """
    Aggregate (from the constant buds flower pot) in a single property on task classes.

    It also provides some default constants, but is intended to be subclassed by instruments.

    To subclass:

    1. Create the actual subclass. All you need to do is add more @properties for the constants you want

    2. Update the instrument class's `constants_model_class` property to return the new subclass. For example::

         class NewConstants(ConstantsBase):
            @property
            def something(self):
                return 7

         class InstrumentWorkflowTask(WorkflowTaskBase):
            @property
            def constants_model_class:
                return NewConstants

            ...

    Parameters
    ----------
    recipe_run_id
        The recipe_run_id
    task_name
        The task_name
    """

    def __init__(self, recipe_run_id: int, task_name: str):
        self._db_dict = ConstantsDb(recipe_run_id=recipe_run_id, task_name=task_name)
        self._recipe_run_id = recipe_run_id

    # These management functions are all underscored because we want tab-complete to *only* show the available
    #  constants
    def _update(self, d: dict):
        self._db_dict.update(d)

    def _purge(self):
        self._db_dict.purge()

    def _close(self):
        self._db_dict.close()

    def _rollback(self):
        self._db_dict.rollback()

    @property
    def dataset_id(self) -> str:
        """Define the dataset id constant."""
        return Sqids(min_length=6, alphabet=ascii_uppercase).encode([self._recipe_run_id])

    @property
    def stokes_params(self) -> list[str]:
        """Return the list of stokes parameter names."""
        return ["I", "Q", "U", "V"]

    @property
    def instrument(self) -> str:
        """Get the instrument name."""
        return self._db_dict[BudName.instrument]

    @property
    def num_cs_steps(self) -> int:
        """Get the number of calibration sequence steps."""
        return self._db_dict[BudName.num_cs_steps]

    @property
    def num_modstates(self) -> int:
        """Get the number of modulation states."""
        return self._db_dict[BudName.num_modstates]

    @property
    def retarder_name(self) -> str:
        """Get the retarder name."""
        return self._db_dict[BudName.retarder_name]

    @property
    def proposal_id(self) -> str:
        """Get the proposal ID constant."""
        return self._db_dict[BudName.proposal_id]

    @property
    def contributing_proposal_ids(self) -> list[str]:
        """Return the list of contributing proposal IDs."""
        proposal_ids = self._db_dict[BudName.contributing_proposal_ids]
        return list(proposal_ids)

    @property
    def experiment_id(self) -> str:
        """Get the experiment ID constant."""
        return self._db_dict[BudName.experiment_id]

    @property
    def contributing_experiment_ids(self) -> list[str]:
        """Return the list of contributing experiment IDs."""
        experiment_ids = self._db_dict[BudName.contributing_experiment_ids]
        return list(experiment_ids)

    @property
    def obs_ip_start_time(self) -> str:
        """Return the start time of the observe IP."""
        return self._db_dict[BudName.obs_ip_start_time]

    @property
    def average_cadence(self) -> float:
        """Get the average cadence constant."""
        return self._db_dict[BudName.average_cadence]

    @property
    def maximum_cadence(self) -> float:
        """Get the maximum cadence constant constant."""
        return self._db_dict[BudName.maximum_cadence]

    @property
    def minimum_cadence(self) -> float:
        """Get the minimum cadence constant constant."""
        return self._db_dict[BudName.minimum_cadence]

    @property
    def variance_cadence(self) -> float:
        """Get the variance of the cadence constant."""
        return self._db_dict[BudName.variance_cadence]

    @property
    def num_dsps_repeats(self) -> int:
        """Get the number of dsps repeats."""
        return self._db_dict[BudName.num_dsps_repeats]

    @property
    def dark_exposure_times(self) -> list[float]:
        """Get a list of exposure times used in the dark calibration."""
        exposure_times = self._db_dict[BudName.dark_exposure_times]
        return list(exposure_times)

    @property
    def dark_readout_exp_times(self) -> list[float]:
        """Get a list of readout exp times for all dark frames."""
        readout_times = self._db_dict[BudName.dark_readout_exp_times]
        return list(readout_times)

    @property
    def wavelength(self) -> float:
        """Wavelength."""
        return self._db_dict[BudName.wavelength]

    @property
    def camera_id(self) -> str:
        """Return the camera ID constant."""
        return self._db_dict[BudName.camera_id]

    @property
    def camera_name(self) -> str:
        """Return the camera name for humans constant."""
        return self._db_dict[BudName.camera_name]

    @property
    def camera_bit_depth(self) -> int:
        """Return the camera bit depth constant."""
        return self._db_dict[BudName.camera_bit_depth]

    @property
    def hardware_binning_x(self) -> int:
        """Return the x-direction hardware binning constant."""
        return self._db_dict[BudName.hardware_binning_x]

    @property
    def hardware_binning_y(self) -> int:
        """Return the y-direction hardware binning constant."""
        return self._db_dict[BudName.hardware_binning_y]

    @property
    def software_binning_x(self) -> int:
        """Return the x-direction software binning constant."""
        return self._db_dict[BudName.software_binning_x]

    @property
    def software_binning_y(self) -> int:
        """Return the y-direction software binning constant."""
        return self._db_dict[BudName.software_binning_y]

    @property
    def hls_version(self) -> str:
        """Return the High-Level Software version."""
        return self._db_dict[BudName.hls_version]

    # Multi-task constants start here:

    @property
    def dark_observing_program_execution_ids(self) -> list[str]:
        """Return the observing program execution ids constant for the dark task."""
        observing_programs = self._db_dict[BudName.dark_observing_program_execution_ids]
        return list(observing_programs)

    @property
    def solar_gain_observing_program_execution_ids(self) -> list[str]:
        """Return the observing program execution ids constant for the solar_gain task."""
        observing_programs = self._db_dict[BudName.solar_gain_observing_program_execution_ids]
        return list(observing_programs)

    @property
    def polcal_observing_program_execution_ids(self) -> list[str]:
        """Return the observing program execution ids constant."""
        observing_programs = self._db_dict[BudName.polcal_observing_program_execution_ids]
        return list(observing_programs)

    @property
    def dark_date_begin(self) -> str:
        """Return the date begin header constant for the dark task."""
        return self._db_dict[BudName.dark_date_begin]

    @property
    def solar_gain_date_begin(self) -> str:
        """Return the date begin header constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_date_begin]

    @property
    def polcal_date_begin(self) -> str:
        """Return the time obs header constant for the polcal task."""
        return self._db_dict[BudName.polcal_date_begin]

    @property
    def dark_date_end(self) -> str:
        """Return the date end constant for the dark task."""
        return self._db_dict[BudName.dark_date_end]

    @property
    def solar_gain_date_end(self) -> str:
        """Return the date end constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_date_end]

    @property
    def polcal_date_end(self) -> str:
        """Return the date end constant for the polcal task."""
        return self._db_dict[BudName.polcal_date_end]

    @property
    def solar_gain_num_raw_frames_per_fpa(self) -> int:
        """Return the number of raw frames per fpa constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_num_raw_frames_per_fpa]

    @property
    def polcal_num_raw_frames_per_fpa(self) -> int:
        """Return the num raw frames per fpa constant for the polcal task."""
        return self._db_dict[BudName.polcal_num_raw_frames_per_fpa]

    @property
    def solar_gain_telescope_tracking_mode(self) -> str:
        """Return the telescope tracking mode constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_telescope_tracking_mode]

    @property
    def polcal_telescope_tracking_mode(self) -> str:
        """Return the telescope tracking mode constant for the polcal task."""
        return self._db_dict[BudName.polcal_telescope_tracking_mode]

    @property
    def solar_gain_coude_table_tracking_mode(self) -> str:
        """Return the coude table tracking mode constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_coude_table_tracking_mode]

    @property
    def polcal_coude_table_tracking_mode(self) -> str:
        """Return the coude table tracking mode constant for the polcal task."""
        return self._db_dict[BudName.polcal_coude_table_tracking_mode]

    @property
    def solar_gain_telescope_scanning_mode(self) -> str:
        """Return the telescope scanning mode constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_telescope_scanning_mode]

    @property
    def polcal_telescope_scanning_mode(self) -> str:
        """Return the telescope scanning mode constant for the polcal task."""
        return self._db_dict[BudName.polcal_telescope_scanning_mode]

    @property
    def dark_average_light_level(self) -> float:
        """Return the average light level constant for the dark task."""
        return self._db_dict[BudName.dark_average_light_level]

    @property
    def solar_gain_average_light_level(self) -> float:
        """Return the average light level constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_average_light_level]

    @property
    def polcal_average_light_level(self) -> float:
        """Return the average light level constant for the polcal task."""
        return self._db_dict[BudName.polcal_average_light_level]

    @property
    def dark_average_telescope_elevation(self) -> float:
        """Return the average telescope elevation constant for the dark task."""
        return self._db_dict[BudName.dark_average_telescope_elevation]

    @property
    def solar_gain_average_telescope_elevation(self) -> float:
        """Return the average telescope elevation constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_average_telescope_elevation]

    @property
    def polcal_average_telescope_elevation(self) -> float:
        """Return the average telescope elevation constant for the polcal task."""
        return self._db_dict[BudName.polcal_average_telescope_elevation]

    @property
    def dark_average_coude_table_angle(self) -> float:
        """Return the average coude table angle constant for the dark task."""
        return self._db_dict[BudName.dark_average_coude_table_angle]

    @property
    def solar_gain_average_coude_table_angle(self) -> float:
        """Return the average coude table angle constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_average_coude_table_angle]

    @property
    def polcal_average_coude_table_angle(self) -> float:
        """Return the average coude table angle constant for the polcal task."""
        return self._db_dict[BudName.polcal_average_coude_table_angle]

    @property
    def dark_average_telescope_azimuth(self) -> float:
        """Return the average telescope azimuth constant for the dark task."""
        return self._db_dict[BudName.dark_average_telescope_azimuth]

    @property
    def solar_gain_average_telescope_azimuth(self) -> float:
        """Return the average telescope azimuth constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_average_telescope_azimuth]

    @property
    def polcal_average_telescope_azimuth(self) -> float:
        """Return the average telescope azimuth constant for the polcal task."""
        return self._db_dict[BudName.polcal_average_telescope_azimuth]

    @property
    def dark_gos_level3_status(self) -> str:
        """Return the gos level3 status constant for the dark task."""
        return self._db_dict[BudName.dark_gos_level3_status]

    @property
    def solar_gain_gos_level3_status(self) -> str:
        """Return the gos level3 status constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_gos_level3_status]

    @property
    def dark_gos_level3_lamp_status(self) -> str:
        """Return the gos level3 lamp status constant for the dark task."""
        return self._db_dict[BudName.dark_gos_level3_lamp_status]

    @property
    def solar_gain_gos_level3_lamp_status(self) -> str:
        """Return the gos level3 lamp status constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_gos_level3_lamp_status]

    @property
    def dark_gos_polarizer_status(self) -> str:
        """Return the gos polarizer status constant for the dark task."""
        return self._db_dict[BudName.dark_gos_polarizer_status]

    @property
    def solar_gain_gos_polarizer_status(self) -> str:
        """Return the gos polarizer status constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_gos_polarizer_status]

    @property
    def dark_gos_polarizer_angle(self) -> float:
        """Return the gos polarizer angle constant for the dark task."""
        return self._db_dict[BudName.dark_gos_polarizer_angle]

    @property
    def solar_gain_gos_polarizer_angle(self) -> float:
        """Return the gos polarizer angle constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_gos_polarizer_angle]

    @property
    def dark_gos_retarder_status(self) -> str:
        """Return the gos retarder status constant for the dark task."""
        return self._db_dict[BudName.dark_gos_retarder_status]

    @property
    def solar_gain_gos_retarder_status(self) -> str:
        """Return the gos retarder status constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_gos_retarder_status]

    @property
    def dark_gos_retarder_angle(self) -> float:
        """Return the gos retarder angle constant for the dark task."""
        return self._db_dict[BudName.dark_gos_retarder_angle]

    @property
    def solar_gain_gos_retarder_angle(self) -> float:
        """Return the gos retarder angle constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_gos_retarder_angle]

    @property
    def dark_gos_level0_status(self) -> str:
        """Return the gos level0 status constant for the dark task."""
        return self._db_dict[BudName.dark_gos_level0_status]

    @property
    def solar_gain_gos_level0_status(self) -> str:
        """Return the gos level0 status constant for the solar gain task."""
        return self._db_dict[BudName.solar_gain_gos_level0_status]
