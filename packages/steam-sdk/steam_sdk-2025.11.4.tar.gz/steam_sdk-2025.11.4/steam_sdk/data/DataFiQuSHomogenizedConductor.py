from pydantic import BaseModel, Field
from typing import List, Literal, Optional, Union


# ============= GEOMETRY ============= #
# -- Input/Output settings -- #
class HomogenizedConductorIOsettingsLoad(BaseModel):
    """
    Level 3: Class for Input/Output settings for the cable geometry
    """

    load_from_yaml: Optional[bool] = Field(
        default=False,
        description="True to load the geometry from a YAML file, false to generate the geometry.",
    )
    filename: Optional[str] = Field(
        default=None,
        description="Name of the YAML file from which to load the geometry.",
    )

class HomogenizedConductorIOsettingsSave(BaseModel):
    """
    Level 3: Class for Input/Output settings for the cable geometry
    """

    save_to_yaml: Optional[bool] = Field(
        default=False,
        description="True to save the geometry to a YAML-file, false to not save the geometry.",
    )
    filename: Optional[str] = Field(
        default=None,
        description="Name of the output geometry YAML file.",
    )

class HomogenizedConductorGeometryIOsettings(BaseModel):
    """
    Level 2: Class for Input/Output settings for the cable geometry
    """

    load: HomogenizedConductorIOsettingsLoad = (
        HomogenizedConductorIOsettingsLoad()
    )
    save: HomogenizedConductorIOsettingsSave = (
        HomogenizedConductorIOsettingsSave()
    )

class Rectangle(BaseModel):
    """
    Level 2: Class for Input/Output settings for the cable geometry
    """
    center_position: Optional[List[float]] = Field(
        default=[], description="Center position in two dimensional plane (x, y)."
    )    
    width: Optional[float] = Field(
        default=None, description="Width of the region (m)."
    )
    height: Optional[float] = Field(
        default=None, description="Height of the region (m)."
    )

class Circle(BaseModel):
    """
    Level 2: Class for Input/Output settings for the cable geometry
    """
    center_position: Optional[List[float]] = Field(
        default=None, description="Center position in two dimensional plane (x, y)."
    )    
    radius: Optional[float] = Field(
        default=None, description="Radius of the circle (m)."
    )

# -- Strand geometry parameters -- #
class HomogenizedConductorGeometry(BaseModel):
    """
    Level 2: Class for strand geometry parameters
    """
    cables_definition: Optional[List[Rectangle]] = Field(default=None, description="List of cable shapes")
    excitation_coils: Optional[List[Rectangle]] = Field(default=None, description="List of excitation coils")
    air: Circle = Circle()
    air_form: Literal['circle'] = Field(
        default='circle', 
        description="Type of model geometry which will be generated. Supported options are only circle for now"
    )
    io_settings: HomogenizedConductorGeometryIOsettings = HomogenizedConductorGeometryIOsettings()

# ============= MESH ============= #

# -- Strand mesh settings -- #
class HomogenizedConductorMesh(BaseModel):
    """
    Level 2: Class for FiQuS ConductorAC
    """

    scaling_global: Optional[float] = Field(
        default=1, description="Global scaling factor for mesh size."
    )
    air_boundary_mesh_size_ratio: Optional[float] = Field(
        default=1, description="Ratio within the air region from boundary to inner elements."
    )
    cable_mesh_size_ratio: Optional[float] = Field(
        default=1, description="Scaling factor within the cable regions."
    )


# ============= SOLVE ============= #
# -- General parameters -- #
class HomogenizedConductorSolveGeneralparameters(BaseModel):
    """
    Level 3: Class for general parameters
    """
    superconductor_linear: Optional[bool] = Field(default=False, description="For debugging: replace LTS by normal conductor.")

    noOfMPITasks: Optional[Union[bool, int]] = Field(
        default=False,
        title="No. of tasks for MPI parallel run of GetDP",
        description=(
            "If integer, GetDP will be run in parallel using MPI. This is only valid"
            " if MPI is installed on the system and an MPI-enabled GetDP is used." 
            " If False, GetDP will be run in serial without invoking mpiexec."
        ),
    )
    rho_cables: Optional[float] = Field(
        default=1,
        description='Resistance for cables when modelled as linear conductors (no current sharing with power law) [Ohm*m].'
    )
    strand_transposition_length: Optional[float] = Field(
        default=0.1,
        description='Transposition length of the strands in the Rutherford cable (m).'
    )
    n_strands: Optional[int] = Field(
        default=36,
        description='Number of strands in the cable (-).'
    )
    strand_filling_factor: Optional[float] = Field(
        default=0.8617,
        description='Filling factor of the strands in the rectangular cable envelope (-).'
    )


# -- Initial conditions -- #
class HomogenizedConductorSolveInitialconditions(BaseModel):
    """
    Level 3: Class for initial conditions
    """

    init_from_pos_file: bool = Field(
        default=False, description="This field is used to initialize the solution from a non-zero field solution stored in a .pos file."
    )
    pos_file_to_init_from: Optional[str] = Field(
        default=None,
        description="Name of .pos file for magnetic field (A/m) from which the solution should be initialized."
        " Should be in the Geometry_xxx/Mesh_xxx/ folder in which the Solution_xxx will be saved.",
    )


# -- Source parameters -- #
class SolveExcitationCoils(BaseModel):
    """
    Level 5: Class for superimposed DC field or current parameters for the sine source
    """
    enable: Optional[bool] = Field(default=False, description='Solve with excitation coils acting as sources.')


class SolveSineSourceSuperimposedDC(BaseModel):
    """
    Level 5: Class for superimposed DC field or current parameters for the sine source
    """
    field_magnitude: Optional[float] = Field(default=0.0, description="DC field magnitude (T) (direction along y-axis). Solution must be initialized with a non-zero field solution stored in a .pos file if non-zero DC field is used.")
    current_magnitude: Optional[float] = Field(default=0.0, description="DC current magnitude (A). Solution must be initialized with a non-zero field solution stored in a .pos file if non-zero DC current is used.")


class SolveSineSource(BaseModel):
    """
    Level 4: Class for Sine source parameters
    """
    frequency: Optional[float] = Field(default=None, description="Frequency of the sine source (Hz).")
    field_amplitude: Optional[float] = Field(default=None, description="Amplitude of the sine field (T).")
    current_amplitude: Optional[float] = Field(default=None, description="Amplitude of the sine current (A).")
    superimposed_DC: SolveSineSourceSuperimposedDC = SolveSineSourceSuperimposedDC()


class SolvePiecewiseSource(BaseModel):
    """
    Level 4: Class for piecewise (linear) source parameters
    """
    source_csv_file: Optional[str] = Field(default=None, description="File name for the from_file source type defining the time evolution of current and field (in-phase). Multipliers are used for each of them. The file should contain two columns: 'time' (s) and 'value' (field/current (T/A)), with these headers. If this field is set, times, applied_fields_relative and transport_currents_relative are ignored.")
    times: Optional[List[float]] = Field(default=None, description="Time instants (s) defining the piecewise linear sources. Used only if source_csv_file is not set. Can be scaled by time_multiplier.")
    applied_fields_relative: Optional[List[float]] = Field(default=None, description="Applied fields relative to multiplier applied_field_multiplier at the time instants 'times'. Used only if source_csv_file is not set.")
    transport_currents_relative: Optional[List[float]] = Field(default=None, description="Transport currents relative to multiplier transport_current_multiplier at the time instants 'times'. Used only if source_csv_file is not set.")
    time_multiplier: Optional[float] = Field(default=None, description="Multiplier for the time values in times (scales the time values). Also used for the time values in the source_csv_file.")
    applied_field_multiplier: Optional[float] = Field(default=None, description="Multiplier for the applied fields in applied_fields_relative. Also used for the values in the source_csv_file.")
    transport_current_multiplier: Optional[float] = Field(default=None, description="Multiplier for the transport currents in transport_currents_relative. Also used for the values in the source_csv_file.")


class HomogenizedConductorSolveSourceparameters(BaseModel):
    """
    Level 3: Class for material properties
    """
    boundary_condition_type: Literal['Natural','Essential'] = Field(
        default='Natural',
        description="Type of boundary condition applied at the outer domain boundary.",
    )
    source_type: Literal['sine', 'piecewise'] = Field(
        default='sine',
        description="Time evolution of applied current and magnetic field. Supported options are: sine, sine_with_DC, piecewise_linear, from_list.",
    )
    parallel_resistor: Optional[Union[bool, float]] = Field(
        default=False,
        title="Resistor parallel to the cable(s)",
        description=(
            "If False, no parallel resistor and the current source directly and only feeds the cable."
            " If True, a resistor is placed in parallel with the cable, with a default resistance of 1 Ohm. If float (cannot be zero), this defines the value of the resistance."
            " If more than one cable is modelled, they are all connected in series (and carry the same current)." 
        ),
    )
    excitation_coils: SolveExcitationCoils = SolveExcitationCoils()

    sine: SolveSineSource = SolveSineSource()
    piecewise: SolvePiecewiseSource = SolvePiecewiseSource()
    field_angle: Optional[float] = Field(default=90, description="Angle of the source magnetic field, with respect to the x-axis (degrees).")
    cable_current_multipliers: Optional[List[float]] = Field(
        default = None,
        description = "Individual multipliers applied to the transport current imposed in each cable. factors are applied according to the cable declarations in the geometry section of the yaml."
    )   



# -- Numerical parameters -- #
class HomogenizedConductorNumericalparametersSine(BaseModel):
    """ 
    Level 4: Numerical parameters corresponding to the sine source
    """
    timesteps_per_period: Optional[float] = Field(default=None, description="Initial value for number of time steps (-) per period for the sine source. Determines the initial time step size.")
    number_of_periods_to_simulate: Optional[float] = Field(default=None, description="Number of periods (-) to simulate for the sine source.")


class HomogenizedConductorNumericalparametersPiecewise(BaseModel):
    """
    Level 4: Numerical parameters corresponding to the piecewise source
    """
    time_to_simulate: Optional[float] = Field(default=None, description="Total time to simulate (s). Used for the piecewise source.")
    timesteps_per_time_to_simulate: Optional[float] = Field(default=None, description="If variable_max_timestep is False. Number of time steps (-) per period for the piecewise source.")
    force_stepping_at_times_piecewise_linear: bool = Field(default=False, description="If True, time-stepping will contain exactly the time instants that are in the times_source_piecewise_linear list (to avoid truncation maximum applied field/current values).")

    variable_max_timestep: bool = Field(default=False, description="If False, the maximum time step is kept constant through the simulation. If True, it varies according to the piecewise definition.")
    times_max_timestep_piecewise_linear: Optional[List[float]] = Field(default=None, description="Time instants (s) defining the piecewise linear maximum time step.")
    max_timestep_piecewise_linear: Optional[List[float]] = Field(default=None, description="Maximum time steps (s) at the times_max_timestep_piecewise_linear. Above the limits, linear extrapolation of the last two values.")


class HomogenizedConductorSolveNumericalparameters(BaseModel):
    """
    Level 3: Class for numerical parameters
    """

    sine: HomogenizedConductorNumericalparametersSine = HomogenizedConductorNumericalparametersSine()
    piecewise: HomogenizedConductorNumericalparametersPiecewise = HomogenizedConductorNumericalparametersPiecewise()


# -- FrequencyDomainSolver parameters -- #
class HomogenizedConductorSolveFrequencyDomainSweep(BaseModel):
    """ 
    Level 4: Class for the frequency sweep definition within a frequency domain solver.
    """
    run_sweep: Optional[bool] = Field(default=False, description='Enabling a frequency sweep.')

    start_frequency: Optional[float] = Field(default=1, description='Start frequency of the sweep in Hz.')
    end_frequency: Optional[float] = Field(default=100, description='End frequency of the sweep in Hz.')
    number_of_frequencies: Optional[int] = Field(default=3, description='Total number of frequencies in the sweep (logspaced)')


class HomogenizedConductorSolveFrequencyDomain(BaseModel):
    """
    Level 3: Class for frequency domain solver parameters
    """
    enable: Optional[bool] = Field(default=False, description='Enable frequency solver functionality in the solve step.')
    frequency_sweep: HomogenizedConductorSolveFrequencyDomainSweep = HomogenizedConductorSolveFrequencyDomainSweep()


# -- Formulation parameters -- #

class HomogenizedConductorFormulationparametersROHM(BaseModel):
    """
    Level 4: Class for ROHM model parameters
    """
    enable: Optional[bool] = Field(
        default=False, 
        description='Use ROHM to homogenize the magnetization hysteresis in the cables.'
    )
    parameter_csv_file: Optional[str] = Field(
        default=None,
        description='Name of the csv file containing the ROHM parameters within the inputs folder with expected row structure: [alpha,kappa,chi,gamma,lambda].'
    )
    weight_scaling: Optional[float] = Field(
        default=1.0,
        description='Downscaling factor (s<1.0) which is applied to all weights except the first, which is scaled up to compensate.'
    )
    tau_scaling: Optional[float] = Field(
        default=1.0,
        description='Scaling factor which is applied uniformly to all coupling time constants.'
    )

class HomogenizedConductorFormulationparametersDISCC(BaseModel):
    """
    Level 4: Class for DISCC model parameters
    """
    gamma_c: Optional[float] = Field(
        default=0.43,
        description='Main crossing scaling parameter (-) that quantifies crossing coupling due to field perpendicular to cable wide face.'
    )
    gamma_a: Optional[float] = Field(
        default=0.53,
        description='Main adjacent scaling parameter (-) that quantifies adjacent coupling due to field parallel to cable wide face.'
    )
    lambda_a: Optional[float] = Field(
        default=0.006,
        description='Mixing scaling parameter (-) that quantifies adjacent coupling due to field perpendicular to cable wide face.'
    )
    crossing_coupling_resistance: Optional[float] = Field(
        default=20e-6,
        description='Resistance (Ohm) of the contact between crossing strands.'
    )
    adjacent_coupling_resistance: Optional[float] = Field(
        default=10e-6,
        description='Resistance (Ohm) of the contact between adjacent strands over one periodicity length (strand twist pitch divided by the number of strands).'
    )
class HomogenizedConductorFormulationparametersROHF(BaseModel):
    """
    Level 4: Class for ROHF model parameters
    """
    enable: Optional[bool] = Field(
        default=False, 
        description='Use ROHF to homogenize the internal flux hysteresis in the cables.'
    )
    parameter_csv_file: Optional[str] = Field(
        default=None,
        description='Name of the csv file containing the ROHF parameters within the inputs folder with expected row structure: [alpha,kappa,tau].'
    )
class HomogenizedConductorFormulationparametersCS(BaseModel):
    """
    Level 4: Class for Current Sharing (CS) model parameters
    """
    superconductor_n_value: Optional[float] = Field(default=30, description="n value for the power law (-), used in current sharing law.")
    superconductor_Ic: Optional[float] = Field(default=350, description="Critical current of the strands (A) (e.g., typical value at T=1.9K and B=10T). Will be taken as a constant as in this model the field dependence is not included"
    " (the main purpose of the model is to verify the more efficient Homogenized Conductor model)."
    " Including field-dependence could be done but is not trivial because is mixes global and local quantities in this Rutherford model with strand discretized individually as stranded conductors.")
    matrix_resistance: Optional[float] = Field(default=6.536208e-04, description="Resistance of the matrix (per unit length) (Ohm/m) for the current sharing law. Kept constant in this model (for simplicity).")


class HomogenizedConductorFormulationparameters(BaseModel):
    """
    Level 3: Class for finite element formulation parameters
    """
    hphia: Optional[bool] = Field(default=False, description='Use hphia formulation.')



class HomogenizedConductorSolve(BaseModel):
    """
    Level 2: Class for FiQuS HomogenizedConductor solver settings
    """
    pro_template: Optional[Literal['HomogenizedConductor_template.pro']] = Field(
        default='HomogenizedConductor_template.pro',
        description="Name of the .pro template file."
    )
    general_parameters: HomogenizedConductorSolveGeneralparameters = (
        HomogenizedConductorSolveGeneralparameters()
    )
    formulation_parameters: HomogenizedConductorFormulationparameters = (
        HomogenizedConductorFormulationparameters()
    )
    discc: HomogenizedConductorFormulationparametersDISCC = (
        HomogenizedConductorFormulationparametersDISCC()
    )
    rohf: HomogenizedConductorFormulationparametersROHF = (
        HomogenizedConductorFormulationparametersROHF()
    )
    rohm: HomogenizedConductorFormulationparametersROHM = (
        HomogenizedConductorFormulationparametersROHM()
    )
    current_sharing: HomogenizedConductorFormulationparametersCS = (
        HomogenizedConductorFormulationparametersCS()
    )
    initial_conditions: HomogenizedConductorSolveInitialconditions = (
        HomogenizedConductorSolveInitialconditions()
    )
    source_parameters: HomogenizedConductorSolveSourceparameters = (
        HomogenizedConductorSolveSourceparameters()
    )
    numerical_parameters: HomogenizedConductorSolveNumericalparameters = (
        HomogenizedConductorSolveNumericalparameters()
    )
    frequency_domain_solver: HomogenizedConductorSolveFrequencyDomain = (
        HomogenizedConductorSolveFrequencyDomain()
    )


# ============= POSTPROC ============= #
class HomogenizedConductorFormulationparametersSampleLine(BaseModel):
    """
    Level 3: Class for sampling along a predefined line within the model
    """
    start_point: Optional[List[float]] = Field(
        default=None,
        description='Start point of the line in cartesian coordinates: [x,y,z].'
    )
    end_point: Optional[List[float]] = Field(
        default=None,
        description='End point of the line in cartesian coordinates: [x,y,z].'
    )
    samples: Optional[int] = Field(
        default=None,
        description='Integer number of evenly spaced sample points along the line including start and end point.'
    )

class HomogenizedConductorPostprocCleanup(BaseModel):
    """
    Level 3: Class for cleanup settings
    """
    remove_pre_file: bool = Field(
        default=False,
        description="Set True to remove the .pre-file after post-processing, to save disk space.",
    )
    remove_res_file: bool = Field(
        default=False,
        description="Set True to remove the .res-file after post-processing, to save disk space.",
    )
    remove_msh_file: bool = Field(
        default=False,
        description="Set True to remove the .msh-file after post-processing, to save disk space.",
    )


class HomogenizedConductorPostproc(BaseModel):
    """
    Level 2: Class for FiQuS ConductorAC
    """
    generate_pos_files: bool = Field(
        default=True,
        description="Set True to generate .pos-files during post-processing",
    )
    output_folder: Optional[str] = Field(
        default=None,
        description="Batch post-processing creates a folder with the given name in the output directory, where all the plots are saved.",
    )
    generate_report: Optional[bool] = Field(
        default=False,
        description="Generates a PDF report including all postprocessing graphs. File is saved in the output_folder."
    )
    save_last_current_density: Optional[str] = Field(
        default=None,
        description="Saves the last current density field solution (out-of-plane) in the file given as a string."
        " The '.pos' extension will be appended to it. Nothing is done if None."
        " This can be for using the current density as an initial condition (but not implemented yet).",
    )
    save_last_magnetic_field: Optional[str] = Field(
        default=None,
        description="Saves the last magnetic field solution (in-plane) in the file given as a string."
        " The '.pos' extension will be appended to it. Nothing is done if None."
        " This is for using the magnetic field as an initial condition for another resolution.",
    )
    cleanup: HomogenizedConductorPostprocCleanup = HomogenizedConductorPostprocCleanup()
    sample_line:  HomogenizedConductorFormulationparametersSampleLine = (
        HomogenizedConductorFormulationparametersSampleLine()
    )


# ============= BASE ============= #
class HomogenizedConductor(BaseModel):
    """
    Level 1: Class for FiQuS ConductorAC
    """

    type: Literal["HomogenizedConductor"]
    geometry: HomogenizedConductorGeometry = HomogenizedConductorGeometry()
    mesh: HomogenizedConductorMesh = HomogenizedConductorMesh()
    solve: HomogenizedConductorSolve = HomogenizedConductorSolve()
    postproc: HomogenizedConductorPostproc = HomogenizedConductorPostproc()
    
