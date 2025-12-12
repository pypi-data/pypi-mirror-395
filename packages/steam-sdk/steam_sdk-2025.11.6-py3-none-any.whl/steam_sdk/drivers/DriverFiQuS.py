import os
import sys
import subprocess
import json
import importlib.util
import platform 

from steam_sdk.data.DataSettings import DataSettings
import getpass
import pandas as pd
import time
from steam_sdk.utils.parse_str_to_list import parse_str_to_list
from steam_sdk.utils.rhasattr import rhasattr
from steam_sdk.utils.sgetattr import rsetattr

from pathlib import Path
class DriverFiQuS:
    """
        Class to drive FiQuS models
    """
    def __init__(self, FiQuS_path: str = '', path_folder_FiQuS_input: str = None, path_folder_FiQuS_output: str = None, GetDP_path: str = None, verbose: bool = False, htcondor_settings: DataSettings = None) -> object:
        """

        :param FiQuS_path: full path to fiqus module
        :type FiQuS_path: str
        :param path_folder_FiQuS_input: full path to FiQuS input folder, i.e. where the input file .yaml is
        :type path_folder_FiQuS_input: str
        :param path_folder_FiQuS_output: full path to FiQuS output folder. This is typically where the same as the path_folder_FiQuS_input
        :type path_folder_FiQuS_output: str
        :param GetDP_path: full path to GetDP executable, with the executable name and extension
        :type GetDP_path: str
        :param verbose: if set to True more logs are printed to the console
        :type verbose: bool
        :param htcondor: if set to True, the driver is used in an HTCondor environment
        :type htcondor: bool
        """
        self.FiQuS_path = FiQuS_path
        self.path_folder_FiQuS_input = path_folder_FiQuS_input
        self.path_folder_FiQuS_output = path_folder_FiQuS_output
        self.GetDP_path = GetDP_path
        self.verbose = verbose
        self.htcondor_settings = htcondor_settings

        # default: not an htcondor run
        self.htcondor = False

        if 'pypi' in self.FiQuS_path:
            spec = importlib.util.find_spec("fiqus.MainFiQuS")
            self.FiQuS_path = spec.origin
        else:
            self.FiQuS_path = os.path.join(self.FiQuS_path, 'fiqus', 'MainFiQuS.py')

        if self.verbose:
            print('FiQuS path =               {}'.format(self.FiQuS_path))
            print('path_folder_FiQuS_input =  {}'.format(self.path_folder_FiQuS_input))
            print('path_folder_FiQuS_output = {}'.format(self.path_folder_FiQuS_output))
            print('GetDP_path =               {}'.format(self.GetDP_path))

        if htcondor_settings is not None and platform.system() == "Linux":
            self.htcondor = True

    def setup_htcondor(self, sim_file_name, simulation_name, sim_number):
        """
        Method to setup FiQuS for HTCondor runs by creating the input dictionaries and checking directories.
        :param sim_file_name: name of the input file (without .yaml) that must be inside the path_folder_FiQuS_input specified in the initialization
        :type sim_file_name: str
        """
        from fiqus.utils.Utils import FilesAndFolders as Util
        from fiqus.data import DataFiQuS as dF

        input_file_name = os.path.join(self.path_folder_FiQuS_input, sim_file_name + '.yaml')
        input_file_path = os.path.abspath(input_file_name)
        fdm = Util.read_data_from_yaml(input_file_name, dF.FDM)

        # folder_should_exist contains all folders that are needed as input for that run type
        if fdm.run.type in ["start_from_yaml", "geometry_only", "geometry_and_mesh"]:
            folders_should_exist = []
        elif fdm.run.type in ["mesh_only", "mesh_and_solve_with_post_process_python"]:
            folders_should_exist = ["Geometry"]
        elif fdm.run.type in ["solve_with_post_process_python", "solve_only"]:
            folders_should_exist = ["Geometry", "Mesh"]
        elif fdm.run.type in ["post_process_getdp_only", "post_process_python_only", "plot_python"]:
            folders_should_exist = ["Geometry", "Mesh", "Solution"] 
            raise Exception(f"{fdm.run.type} is not supported by HTCondor yet!")
        
        # folders_to_be_returned contains all folders that are needed as output for that run type
        if fdm.run.type == "start_from_yaml":
            folders_to_be_returned = ["Geometry", "Mesh", "Solution"]
        elif fdm.run.type == "geometry_only":
            folders_to_be_returned = ["Geometry"]
        elif fdm.run.type == "geometry_and_mesh":
            folders_to_be_returned = ["Geometry", "Mesh"]
        elif fdm.run.type == "mesh_only":
            folders_to_be_returned = ["Mesh"]
        elif fdm.run.type == "mesh_and_solve_with_post_process_python":
            folders_to_be_returned = ["Mesh", "Solution"]
        elif fdm.run.type in ["solve_with_post_process_python", "solve_only", "post_process_getdp_only", "post_process_python_only", "plot_python"]:
            folders_to_be_returned = ["Solution"]

        # compute paths for folders and check that necessary folders exist
                        # check if either geometry, mesh, or solution path are the same as another entry in the htcondor csv (of course depending on run type)
        htcondor_csv_filepath = self.htcondor_settings.run_log_path

        if not htcondor_csv_filepath:
            raise Exception("No path to htcondor run log csv file has been provided in data settings. Please provide a valid path.")
        
        # check if required folders of model files exists
        # compute paths
        base_path_model_files = self.htcondor_settings.local_FiQuS_folder

        geometry_folder = self.compute_and_check_path("Geometry", fdm.run.geometry, "Geometry" in folders_should_exist, "Geometry" in folders_to_be_returned, base_path_model_files, input_file_name, fdm.run.type, simulation_name, sim_number, htcondor_csv_filepath, fdm)

        mesh_folder = self.compute_and_check_path("Mesh", fdm.run.mesh, "Mesh" in folders_should_exist, "Mesh" in folders_to_be_returned, base_path_model_files, input_file_name, fdm.run.type, simulation_name, sim_number, htcondor_csv_filepath, fdm, geo_folder=geometry_folder)

        solution_folder = self.compute_and_check_path("Solution", fdm.run.solution, "Solution" in folders_should_exist, "Solution" in folders_to_be_returned, base_path_model_files, input_file_name, fdm.run.type, simulation_name, sim_number, htcondor_csv_filepath, fdm, geo_folder=geometry_folder, mesh_folder=mesh_folder)

        import htcondor
        username = getpass.getuser()
        first_letter = username[0]
        _ = htcondor.Collector()
        credd = htcondor.Credd()
        credd.add_user_cred(htcondor.CredTypes.Kerberos, None)
        self.sub = htcondor.Submit()

        root_folder_to_be_returned = folders_to_be_returned[0]
        def _path_component(path_value: str | None) -> str | None:
            if not path_value or path_value == "-":
                return None
            return os.path.basename(path_value)

        def _join_nonempty(*parts: str | None) -> str:
            cleaned = [part for part in parts if part]
            return os.path.join(*cleaned) if cleaned else ""

        geometry_base = _path_component(geometry_folder)
        mesh_base = _path_component(mesh_folder)
        solution_base = _path_component(solution_folder)

        if root_folder_to_be_returned == "Geometry":
            eos_output_folder = os.path.dirname(geometry_folder)
            relative_output_folder = geometry_base or ""
            copy_eos_folder = ""
            copy_depth = 1
        elif root_folder_to_be_returned == "Mesh":
            eos_output_folder = os.path.dirname(mesh_folder)
            relative_output_folder = _join_nonempty(geometry_base, mesh_base)
            copy_eos_folder = f"-c {geometry_folder}"
            copy_depth = 1
        elif root_folder_to_be_returned == "Solution":
            eos_output_folder = os.path.dirname(solution_folder)
            relative_output_folder = _join_nonempty(geometry_base, mesh_base, solution_base)
            copy_eos_folder = f"-c {geometry_folder}"
            copy_depth = 2

        self.sub['+WANT_SUSPEND'] = "FALSE"
        self.sub['+WANT_VACATE'] = "FALSE"
        self.sub['+WANT_VACATE'] = "MaxJobRetirementTime"

        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)

        if self.htcondor_settings.FiQuS_path == "pypi":
            # if pypi, load path of pip installed fiqus package
            spec = importlib.util.find_spec("fiqus.MainFiQuS")
            fiqus_dir = str(Path(spec.origin).parent.parent)
        else:
            fiqus_dir = self.htcondor_settings.FiQuS_path

        self.sub['executable'] = os.path.join(file_dir, "utils", "call_mainfiqus_htcondor.sh")

        # Encode arguments so HTCondor does not split on spaces; the shell script decodes them.
        space_token = "__HTCONDOR_SPACE__"

        def _encode(value: str) -> str:
            return str(value).replace(" ", space_token)

        self.sub["fiqus_path"] = _encode(fiqus_dir)
        self.sub["input_file"] = _encode(input_file_path)
        self.sub["data_model"] = _encode(input_file_name)
        self.sub["eos_output"] = _encode(eos_output_folder)
        self.sub["rel_output"] = _encode(relative_output_folder)
        self.sub["copy_depth"] = _encode(str(copy_depth))
        self.sub["erase_files"] = _encode('yes' if self.htcondor_settings.remove_input_files_from_afs else 'no')

        if copy_eos_folder:
            copy_eos_path = copy_eos_folder.split(None, 1)[1]
            self.sub["eos_input"] = _encode(os.path.normpath(copy_eos_path))
            self.sub["arguments"] = "$(fiqus_path) $(input_file) $(data_model) $(eos_output) $(rel_output) $(copy_depth) $(erase_files) $(eos_input)"
        else:
            self.sub["arguments"] = "$(fiqus_path) $(input_file) $(data_model) $(eos_output) $(rel_output) $(copy_depth) $(erase_files)"
        
        self.sub['environment'] = f"CONDOR_JOB_ID=$(Cluster)"

        self.sub['error'] = self.htcondor_settings.error
        self.sub['output'] = self.htcondor_settings.output
        self.sub['log'] = self.htcondor_settings.log
        self.sub['request_cpus'] = str(self.htcondor_settings.request_cpus)
        if self.htcondor_settings.request_memory:
            self.sub['request_memory'] = self.htcondor_settings.request_memory
        if self.htcondor_settings.request_disk:
            self.sub['request_disk'] = self.htcondor_settings.request_disk

        if self.htcondor_settings.singularity_image_path:
            self.sub['+SingularityImage'] = f"\"{self.htcondor_settings.singularity_image_path}\""
        elif self.htcondor_settings.cerngetdp_version:
            self.sub['+SingularityImage'] = '"/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/steam/steam-fiqus-dev-public-docker:' + f"{self.htcondor_settings.cerngetdp_version}\""
        else:
            self.sub['+SingularityImage'] = '"/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/steam/steam-fiqus-dev-public-docker:latest/"'
        # get access to eos in singularity container
        self.sub['+SingularityBind'] = "'/eos:/eos'"

        self.sub['should_transfer_files'] = 'YES'
        self.sub['when_to_transfer_output'] = 'ON_EXIT_OR_EVICT'
        self.sub['preserve_relative_paths'] = True
        self.sub['+MaxRuntime'] = self.htcondor_settings.max_run_time
        self.sub['output_destination'] = f"root://eosuser.cern.ch/{self.htcondor_settings.htcondor_log_path}/$(Cluster)"
        self.sub['MY.SendCredential'] = True
        self.sub['+BigMemJob'] = self.htcondor_settings.big_mem_job

        self.input_file_name = input_file_name
        self.fdm = fdm
        self.geometry_folder = geometry_folder
        self.mesh_folder = mesh_folder 
        self.solution_folder = solution_folder
        self.simulation_name = simulation_name
        self.sim_number = sim_number
        self.htcondor_csv_filepath = htcondor_csv_filepath

    def run_FiQuS(self, sim_file_name: str, return_summary: bool = False):
        """
        Method to run FiQuS with a given input file name. The run type is specified in the input file.
        :param return_summary: summary of relevant parameters
        :rtype return_summary: dict
        :param sim_file_name: name of the input file (without .yaml) that must be inside the path_folder_FiQuS_input specified in the initialization
        :type sim_file_name: str
        """
        if not self.htcondor:

            call_commands_list = [
                sys.executable,
                self.FiQuS_path,
                os.path.join(self.path_folder_FiQuS_input, sim_file_name + '.yaml'),
                '-o', self.path_folder_FiQuS_output,
                '-g', self.GetDP_path,
            ]
            if self.verbose:
                command_string = " ".join(call_commands_list)
                print(f'Calling MainFiQuS via Python Subprocess.call() with: {command_string}')
            try:
                result = subprocess.call(call_commands_list, shell=False)
            # except subprocess.CalledProcessError as e:
            #     # Handle exceptions if the command fails
            #     print("Error:", e)
            #     if result != 0:
            #         raise _error_handler(call_commands_list, result, "Command failed.")
            #     return result
            except subprocess.CalledProcessError as e:
                # Handle exceptions if the command fails
                raise _error_handler(call_commands_list, e.returncode, e.stderr)
                
            if return_summary:
                summary = json.load(open(f"{os.path.join(self.path_folder_FiQuS_output, sim_file_name)}.json"))
                return summary

        else:

            import htcondor 
            schedd = htcondor.Schedd()
            result = schedd.submit(self.sub)

            cluster_id = result.cluster()

            time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S")

            # write to run log csv
            run_log_row = [
                time_stamp,
                cluster_id,
                self.input_file_name,
                self.fdm.run.type,
                self.geometry_folder,
                self.mesh_folder,
                self.solution_folder,
                "Submitted",
                self.simulation_name,
                self.sim_number
            ]
            self.add_to_htcondor_log(
                self.htcondor_csv_filepath, run_log_row
            )

            #print(f"Singularity image {sub['+SingularityImage']} will be used")

            print(f"The FiQuS job was successfully submitted with cluster id {cluster_id}.{os.linesep}{os.linesep}")

    def compute_and_check_path(self, folder_type, folder_suffix, folder_is_required, folder_is_returned, base_path_model_files, input_file_name, run_type, parametric_csv, i, csv_filepath, fdm, geo_folder=None, mesh_folder=None):

        # Determine a sensible base path depending on available inputs.
        # - If `base_path_model_files` is provided (HTCondor/EOS root), join it with
        #   the input file name's basename so we get a consistent folder under that root.
        # - Otherwise fall back to the directory containing the input YAML.
        if folder_type == "Geometry":
            # input_file_name may be absolute; use its basename without extension when joining with the base root
            base_input = parametric_csv
            base_path = os.path.join(base_path_model_files, base_input)
        elif folder_type == "Mesh":
            base_path = geo_folder
        elif folder_type == "Solution":
            base_path = mesh_folder

        if folder_is_required:
            folder_name = f"{folder_type}_{folder_suffix}"
            folder = os.path.join(base_path, folder_name)

            if not os.path.exists(folder):
                raise Exception(f'{folder_type} folder {folder} does not exist but is needed for run type {run_type}')
            
        else:
            if folder_is_returned:
                if pd.isna(folder_suffix):     
                    folder_name = f"{folder_type}_{parametric_csv}_row_{i}"
                    folder = os.path.join(base_path, folder_name)

                    print(f'changing input: {f"run.{folder_type.lower()}"} to: {f"{parametric_csv}_row_{i}"}')
                    self.__set_attribute(fdm, f"run.{folder_type.lower()}", f"{parametric_csv}_row_{i}")
                else:
                    folder_name = f"{folder_type}_{folder_suffix}"
                    folder = os.path.join(base_path, folder_name)

                if os.path.exists(folder):
                    raise Exception(f'{folder_type} folder {folder} already exists on EOS. This operation would overwrite the contents of the folder.')

                if self.is_entry_in_run_log(csv_filepath, f"{folder_type} Folder", folder):
                    raise Exception(f'{folder_type} folder {folder} already exists in the htcondor csv file. This operation would overwrite the contents of the folder.')
            else:
                folder = '-'
                print(f'changing input: {f"run.{folder_type.lower()}"} to: None')
                self.__set_attribute(fdm, f"run.{folder_type.lower()}", 'None')

        print(f'{folder_type} will be stored in {folder}')
        return folder

    @staticmethod
    def add_to_htcondor_log(path_to_csv, run_log_row):
        import csv

        # If file does not exist or is empty, write the header
        if not os.path.isfile(path_to_csv) or os.path.getsize(path_to_csv) == 0:
            header = [
                "Time Stamp",
                "Job ID",
                "Model Name",
                "Run Type",
                "Geometry Folder",
                "Mesh Folder",
                "Solution Folder",
                "Status",
                "Loop CSV File",
                "Loop CSV Row"
            ]

            with open(path_to_csv, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(header)

        # Open the CSV file in append mode
        with open(path_to_csv, "a+", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(run_log_row)

    @staticmethod
    def is_entry_in_run_log(path_to_csv, column_header, column_value):

        if not os.path.isfile(path_to_csv) or os.path.getsize(path_to_csv) == 0:
            return False
        
        # Load the CSV file
        df = pd.read_csv(path_to_csv)

        # Access the column by its title
        column_data = df[column_header]

        return column_data.isin([column_value]).any()

    @staticmethod
    def __set_attribute(dm, var_name, var_value):
        if rhasattr(dm, var_name):
            # Handle different data types more carefully
            if isinstance(var_value, (int, float, bool)):
                # Convert float to int if the field expects int
                if isinstance(var_value, float) and var_value.is_integer():
                    var_value = int(var_value)
                rsetattr(dm, var_name, var_value)
            elif isinstance(var_value, str):
                # Only parse to list if the string looks like a list
                if var_value.startswith('[') and var_value.endswith(']'):
                    parsed_value = parse_str_to_list(var_value)
                else:
                    parsed_value = var_value
                rsetattr(dm, var_name, parsed_value)
            elif isinstance(var_value, list):
                # Handle list values directly
                rsetattr(dm, var_name, var_value)
            else:
                rsetattr(dm, var_name, var_value)
        else:
            raise Exception(f'Invalid data: {var_value} in column name {var_name}')

class _error_handler(Exception):
    def __init__(self, command, return_code, stderr):
        self.command = command
        self.return_code = return_code
        self.stderr = stderr
        super().__init__(f"Command '{command}' failed with return code {return_code}. Error: {stderr}")