#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 fiqusPath inputFile fiqusDataModelPath eosOutputFolder relativeOutputPath copyDepth eraseFDSandFDMInputFiles [eosInputFolder]"
   echo -e "\tfiqusPath: path to FiQuS root folder"
   echo -e "\tinputFile: path to FiQuS input file"
   echo -e "\tfiqusDataModelPath: path to FiQuS data model file"
   echo -e "\teosOutputFolder: path to FiQuS output path"
   echo -e "\trelativeOutputPath: relative path to FiQuS folder to be copied to EOS"
   echo -e "\tcopyDepth: copy depth"
   echo -e "\teraseFDSandFDMInputFiles: erase FDS and FDM input files"
   echo -e "\teosInputFolder: EOS file path to copy to sandbox (optional)"
   exit 1 # Exit script after printing help
}

# Parse positional arguments
fiqusPath="$1"
inputFile="$2"
fiqusDataModelPath="$3"
eosOutputFolder="$4"
relativeOutputPath="$5"
copyDepth="$6"
eraseFDSandFDMInputFiles="$7"
eosInputFolder="$8"  # Optional

SPACE_TOKEN="__HTCONDOR_SPACE__"

decode_spaces() {
    local value="$1"
    echo "${value//${SPACE_TOKEN}/ }"
}

fiqusPath="$(decode_spaces "$fiqusPath")"
inputFile="$(decode_spaces "$inputFile")"
fiqusDataModelPath="$(decode_spaces "$fiqusDataModelPath")"
eosOutputFolder="$(decode_spaces "$eosOutputFolder")"
relativeOutputPath="$(decode_spaces "$relativeOutputPath")"
copyDepth="$(decode_spaces "$copyDepth")"
eraseFDSandFDMInputFiles="$(decode_spaces "$eraseFDSandFDMInputFiles")"
if [ -n "$eosInputFolder" ]; then
    eosInputFolder="$(decode_spaces "$eosInputFolder")"
fi

echo "===== ARGS ====="
for a in "$@"; do
    echo "[$a]"
done

# Print helpFunction in case parameters are empty
if [ -z "$fiqusPath" ] || [ -z "$inputFile" ] || [ -z "$fiqusDataModelPath" ] || [ -z "$eosOutputFolder" ] || [ -z "$relativeOutputPath" ] || [ -z "$eraseFDSandFDMInputFiles" ];
then
   echo "ERROR: Some or all of the required parameters are empty";
   echo ""
   echo "Missing parameters:"
   [ -z "$fiqusPath" ] && echo "  - fiqusPath (-f) is empty"
   [ -z "$inputFile" ] && echo "  - inputFile (-i) is empty"
   [ -z "$fiqusDataModelPath" ] && echo "  - fiqusDataModelPath (-m) is empty"
   [ -z "$eosOutputFolder" ] && echo "  - eosOutputFolder (-o) is empty"
   [ -z "$relativeOutputPath" ] && echo "  - relativeOutputPath (-r) is empty"
   [ -z "$eraseFDSandFDMInputFiles" ] && echo "  - eraseFDSandFDMInputFiles (-e) is empty"
   echo ""
   helpFunction
fi

# # change home to temporary file system as gmsh will write the .gmshsock2 socket file to there. This path can not be on /afs nor on /eos.
mkdir -p /tmp/$USER
OLDHOME=${HOME}
HOME="/tmp/$USER"

SCRATCHBOX_TEMP_OUTPUT=${_CONDOR_SCRATCH_DIR}/fiqus

# copy eos file to sandbox
if [ -z "$eosInputFolder" ]; then
   echo "No files to copy from EOS to sandbox."
else 
    echo "Copy folder ${eosInputFolder} to ${SCRATCHBOX_TEMP_OUTPUT}"
   export EOS_MGM_URL=root://eosuser.cern.ch
     eos cp --depth="${copyDepth}" -r "${eosInputFolder}" "${SCRATCHBOX_TEMP_OUTPUT}/"
fi

cd "${fiqusPath}"

/fiqus-dev_venv/bin/python3 fiqus/MainFiQuS.py "${inputFile}" -g getdp -o "${SCRATCHBOX_TEMP_OUTPUT}" -m "${fiqusDataModelPath}" -j ${CONDOR_JOB_ID}

# Erase FDS and FDM input files if requested
# typically they should be in the same parent folder, but still get the paths separately
fdmpath=$(dirname "${fiqusDataModelPath}")
parentpathfdm=$(dirname "${fdmpath}")
modelinputpathfdm=$(dirname "${parentpathfdm}")

if [ "${eraseFDSandFDMInputFiles}" == "yes" ]; then
    echo "Erase FDS and FDM input file paths as requested."
    rm -rf "${fdmpath}"
    rm -rf "${fdspath}"
fi

if [ -z "$(find "${parentpathfdm}" -mindepth 1 -maxdepth 1)" ]; then
    echo "FDM folder ${parentpathfdm} is empty, removing folder."
    rm -rf "${parentpathfdm}"
fi 

if [ -z "$(find "${modelinputpathfdm}" -mindepth 1 -maxdepth 1)" ]; then
    echo "Model input folder ${modelinputpathfdm} is empty, removing folder."
    rm -rf "${modelinputpathfdm}"
fi

echo "Copy FiQuS logs from ${SCRATCHBOX_TEMP_OUTPUT}/logs to ${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath}/logs"
mkdir -p "${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath}/logs"
cp -r "${SCRATCHBOX_TEMP_OUTPUT}/logs" "${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath}/"

echo "Copy HTCondor stdout and err from ${SCRATCHBOX_TEMP_OUTPUT} to ${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath}/logs"
cp "${_CONDOR_SCRATCH_DIR}/_condor_stderr" "${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath}/logs/condor_stderr.txt"
cp "${_CONDOR_SCRATCH_DIR}/_condor_stdout" "${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath}/logs/condor_stdout.txt"

echo "Copy folder ${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath} to ${eosOutputFolder}"
export EOS_MGM_URL=root://eosuser.cern.ch
eos cp -r "${SCRATCHBOX_TEMP_OUTPUT}/${relativeOutputPath}" "${eosOutputFolder}"

HOME=${OLDHOME}
cd "${SCRATCHBOX_TEMP_OUTPUT}"