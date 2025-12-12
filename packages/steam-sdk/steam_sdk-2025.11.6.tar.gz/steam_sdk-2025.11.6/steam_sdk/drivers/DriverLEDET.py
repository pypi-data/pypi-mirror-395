import os.path
import subprocess
import os
import getpass
from steam_sdk.utils.make_folder_if_not_existing import make_folder_if_not_existing

class DriverLEDET:
    '''
        Class to drive LEDET models
    '''

    def __init__(self, path_exe=None, path_folder_LEDET=None, verbose=False, htcondor_settings=None):
        # Unpack arguments
        self.path_exe          = path_exe
        self.path_folder_LEDET = path_folder_LEDET
        self.verbose           = verbose
        self.htcondor_settings = htcondor_settings
        if verbose:
            print('path_exe =          {}'.format(path_exe))
            print('path_folder_LEDET = {}'.format(path_folder_LEDET))

        self.working_directory = os.getcwd()

        #default: not HTCondor run
        self.htcondor = False

        if htcondor_settings is not None:
            self.htcondor = True


    def setup_htcondor(self, simulation_name, sim_number):
        """
        Method to setup FiQuS for HTCondor runs by creating the input dictionaries and checking directories.
        :param sim_file_name: name of the input file (without .yaml) that must be inside the path_folder_FiQuS_input specified in the initialization
        :type sim_file_name: str
        """
        
        htcondor_csv_filepath = self.htcondor_settings.run_log_path

        if not htcondor_csv_filepath:
            raise Exception("No path to htcondor run log csv file has been provided in data settings. Please provide a valid path.")

        import htcondor
        username = getpass.getuser()
        first_letter = username[0]
        _ = htcondor.Collector()
        credd = htcondor.Credd()
        credd.add_user_cred(htcondor.CredTypes.Kerberos, None)
        self.sub = htcondor.Submit()

        self.sub['+WANT_SUSPEND'] = "FALSE"
        self.sub['+WANT_VACATE'] = "FALSE"
        self.sub['+WANT_VACATE'] = "MaxJobRetirementTime"

        file_path = os.path.abspath(__file__)
        file_dir = os.path.dirname(file_path)

        self.sub['executable'] = os.path.join(file_dir, "utils", "call_ledet_htcondor.sh")

        # Encode arguments so HTCondor does not split on spaces; the shell script decodes them.
        space_token = "__HTCONDOR_SPACE__"

        def _encode(value: str) -> str:
            return str(value).replace(" ", space_token)
        

        # Copy input files 
        input_file_path = os.path.join(self.working_directory, self.path_folder_LEDET)
        field_maps_file_path = os.path.join(self.working_directory,"Field maps")
        
        # no Excel installed on Docker image, so only yaml input files are supported for HTCondor runs
        input_file_type = ".yaml"

        # we read from AFS for the inputs, no copying needed
        self.sub['input_file_path'] = _encode(input_file_path)
        self.sub['simulation_name'] = _encode(simulation_name)
        self.sub['simulation_number'] = _encode(sim_number)
        self.sub['input_file_type'] = _encode(input_file_type)
        self.sub['output_file_path'] = _encode(self.htcondor_settings.local_LEDET_folder)
        self.sub['field_maps_file_path'] = _encode(field_maps_file_path)

        self.sub['arguments'] = "$(input_file_path) $(simulation_name) $(simulation_number) $(input_file_type) $(output_file_path) $(field_maps_file_path)"

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
        elif self.htcondor_settings.ledet_version:
            self.sub['+SingularityImage'] = '"/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/steam/steam-ledet:' + f"{self.htcondor_settings.ledet_version}\""
        else:
            self.sub['+SingularityImage'] = '"/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/steam/steam-ledet:latest/"'
        # get access to eos in singularity container
        self.sub['+SingularityBind'] = "'/eos:/eos'"

        self.sub['should_transfer_files'] = 'YES'
        self.sub['when_to_transfer_output'] = 'ON_EXIT_OR_EVICT'
        self.sub['preserve_relative_paths'] = True
        self.sub['+MaxRuntime'] = self.htcondor_settings.max_run_time
        self.sub['output_destination'] = f"root://eosuser.cern.ch/{self.htcondor_settings.htcondor_log_path}/$(Cluster)"
        self.sub['MY.SendCredential'] = True
        self.sub['+BigMemJob'] = self.htcondor_settings.big_mem_job

        self.simulation_name = simulation_name
        self.sim_number = sim_number
        self.htcondor_csv_filepath = htcondor_csv_filepath

        # ['/afs/cern.ch/work/e/eschnaub/fcc-mq-magnet-quench-protection-study/\\\\eosproject-smb\\e...\\releases\\ledet\\Windows\\LEDET_v2_05_01.exe', 'ledet_output', 'FCC_MQ', '601', '.xlsx']
    
    def run_LEDET(self, nameMagnet: str, simsToRun: str, simFileType: str = '.xlsx'):
        '''
        ** Run LEDET model **
        :param nameMagnet: Name of the magnet model to run
        :param simsToRun: Number identifying the simulation to run
        :param simFileType: String identifying the type of input file (supported: .xlsx, .yaml, .json)
        :return:
        '''

        if not self.htcondor:
            # Unpack arguments
            path_exe = self.path_exe
            path_folder_LEDET = self.path_folder_LEDET
            verbose = self.verbose
            if simFileType == None:
                simFileType = '.xlsx'  # set to default

            if verbose:
                print('path_exe =          {}'.format(path_exe))
                print('path_folder_LEDET = {}'.format(path_folder_LEDET))
                print('nameMagnet =        {}'.format(nameMagnet))
                print('simsToRun =         {}'.format(simsToRun))
                print('simFileType =       {}'.format(simFileType))

            # Run model
            # ['/afs/cern.ch/work/e/eschnaub/fcc-mq-magnet-quench-protection-study/\\\\eosproject-smb\\e...\\releases\\ledet\\Windows\\LEDET_v2_05_01.exe', 'ledet_output', 'FCC_MQ', '601', '.xlsx']
            ledet_logs_folder = os.path.join(path_folder_LEDET, nameMagnet, 'Output', 'Logs')
            make_folder_if_not_existing(ledet_logs_folder)
            current_folder = os.getcwd()
            os.chdir(ledet_logs_folder)
            subprocess.call([path_exe, path_folder_LEDET, nameMagnet, simsToRun, simFileType])
            os.chdir(current_folder)
            return {'dummy_value': 123456789} # this is temporary only. It is needed for Dakota
        else:

            # BEWARE: no logic implemented to avoid re-running the same simulation multiple times
            import htcondor

            # Create HTCondor job submission
            schedd = htcondor.Schedd()
            result = schedd.submit(self.sub)

            print(f"LEDET HTCondor job submitted with Cluster ID {result.cluster()} for simulation {self.simulation_name}.")

            return {'htcondor_cluster_id': result.cluster()}
# def RunSimulationsLEDET(LEDETFolder, LEDETExe, MagnetName, Simulations = 'All', RunSimulations = False):
#     # ExcelFolder = LEDETFolder + "//LEDET//" + MagnetName + "//Input//"  # original
#     ExcelFolder = LEDETFolder + "/LEDET/" + MagnetName + "/Input/"  # edited to pass tests on Gitlab
#     StartFile = LEDETFolder + "//startLEDET.xlsx"
#     SimNumbers = []
#
#     #1. Prepare everything
#     if len(Simulations)==3:
#         if Simulations =='All':
#             items = os.listdir(ExcelFolder)
#             for item in items:
#                 if item.startswith(MagnetName) and item.endswith('.xlsx'):
#                     if ".sys" not in item:
#                         num = item.replace('.xlsx', '')
#                         num = num.replace(MagnetName+'_', '')
#                         num = int(num)
#                         SimNumbers.append(num)
#     else:
#         SimNumbers = Simulations
#
#     df = pd.read_excel(StartFile, header=None)
#     df.rename(columns={0: 'a', 1: 'b', 2: 'c'}, inplace=True)
#     df.loc[df['b'] == 'currFolder', 'c'] = LEDETFolder + "\\LEDET"
#     df.loc[df['b'] == 'nameMagnet', 'c'] = MagnetName
#     df.loc[df['b'] == 'simsToRun',  'c'] = str(SimNumbers)
#     writer = pd.ExcelWriter(StartFile)
#     df.to_excel(writer, index=False, index_label=False, header=False, sheet_name='startLEDET')
#     writer.save()
#
#     #2. Run Executable
#     if RunSimulations:
#         os.chdir(LEDETFolder)
#         os.system(LEDETExe)
#
#
# def run_LEDET(self, LEDET_exe_full_path):
#     RunSimulationsLEDET(self.base_folder, LEDET_exe_full_path, self.nameCircuit, Simulations=self.model_no,
#                    RunSimulations=False)
#     LEDET_exe_path = os.path.join(self.base_folder, LEDET_exe_full_path)
#     os.chdir(self.base_folder)
#     subprocess.call([LEDET_exe_path])