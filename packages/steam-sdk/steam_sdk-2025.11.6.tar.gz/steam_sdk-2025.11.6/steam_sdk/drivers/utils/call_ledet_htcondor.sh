#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

# Validate arguments
if [ "$#" -lt 6 ]; then
    echo "Usage: $0 <input_file_path> <simulation_name> <simulation_number> <input_file_type> <output_file_path> <field_maps_file_path>"
    exit 1
fi

# Parse positional arguments
input_file_path="$1"
simulation_name="$2"
simulation_number="$3"
input_file_type="$4"
output_file_path="$5"
field_maps_file_path="$6"

SPACE_TOKEN="__HTCONDOR_SPACE__"

decode_spaces() {
    local value="$1"
    echo "${value//${SPACE_TOKEN}/ }"
}

# Determine a writable workdir (prefer Condor scratch if available)
WORKDIR="${_CONDOR_SCRATCH_DIR:-$(pwd)}"
mkdir -p "${WORKDIR}/ledet_input"
mkdir -p "${WORKDIR}/Field maps"
mkdir -p "${WORKDIR}/ledet_input/$(decode_spaces "$simulation_name")"
mkdir -p "${WORKDIR}/ledet_input/$(decode_spaces "$simulation_name")/Input"

# copy input file path to local scratch
SRC_INPUT="$(decode_spaces "$input_file_path")/$(decode_spaces "$simulation_name")/Input"

if [ ! -e "$SRC_INPUT" ]; then
    echo "ERROR: input path does not exist: $SRC_INPUT"
    exit 2
fi
echo "Copying input files from $SRC_INPUT to local scratch..."
cp -r "$SRC_INPUT"/* "${WORKDIR}/ledet_input/$(decode_spaces "$simulation_name")/Input"

# copy field maps to local scratch
SRC_FIELD_MAPS="$(decode_spaces "$field_maps_file_path")"
if [ -n "$SRC_FIELD_MAPS" ] && [ ! -e "$SRC_FIELD_MAPS" ]; then
    echo "WARNING: field maps path does not exist: $SRC_FIELD_MAPS"
else
    echo "Copying field maps from $SRC_FIELD_MAPS to local scratch..."
    cp -r "$SRC_FIELD_MAPS" "${WORKDIR}/ledet_input/Field maps/"
fi

# run LEDET
SIM_NAME_DECODED="$(decode_spaces "$simulation_name")"
SIM_NUM_DECODED="$(decode_spaces "$simulation_number")"
INPUT_TYPE_DECODED="$(decode_spaces "$input_file_type")"
echo "Running LEDET simulation $SIM_NAME_DECODED number $SIM_NUM_DECODED with input file type $INPUT_TYPE_DECODED"

LEDET_BIN="/ledet_binary/ledet"
if [ ! -x "$LEDET_BIN" ]; then
    echo "ERROR: LEDET binary not found or not executable at $LEDET_BIN"
    exit 3
fi

cmd=("$LEDET_BIN" "${WORKDIR}/ledet_input/" "$SIM_NAME_DECODED" "$SIM_NUM_DECODED" "$INPUT_TYPE_DECODED")
"${cmd[@]}"
rc=$?
if [ $rc -ne 0 ]; then
    echo "LEDET returned exit code $rc"
    exit $rc
fi


# make direcotory for output files if it does not exist
mkdir -p "$(decode_spaces "$output_file_path")"
mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")"

mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Output/"

mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Output/EXCEL_output"
mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Output/Mat Files"
mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Output/Reports"
mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Output/Txt Files"
mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Output/csv"
mkdir -p "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Output/LEDET Diaries"

output_dir="${WORKDIR}/ledet_input/$(decode_spaces "$simulation_name")/Output"

# rename LEDET diary file to include simulation number
LEDET_diary=$(find . -maxdepth 1 -type f -name "diaryLEDET*" | head -n 1)
cp "$LEDET_diary" "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/LEDET Diaries/diaryLEDET_$(decode_spaces "$simulation_number").txt"

# rename csv to include simulation number and copy
cp "${output_dir}/csv/LEDET_summary_FCC_MQ.csv" "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/csv/LEDET_summary_FCC_MQ_$(decode_spaces "$simulation_number").csv"

# copy EXCEL_output per magnet 
cp "${output_dir}/EXCEL_output/Temporary_EXCEL_file_for_simulation_output.csv" "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/EXCEL_output/Temporary_EXCEL_file_for_simulation_output_$(decode_spaces "$simulation_number").csv"

# copy "Mat Files" per magnet
cp "${output_dir}/Mat Files/"* "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Mat Files/"

# copy Reports per magnet
cp "${output_dir}/Reports/"* "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Reports/"

# copy Txt per magnet (optional, may fail)
cp "${output_dir}/Txt Files/"* "$(decode_spaces "$output_file_path")/$(decode_spaces "$simulation_name")/Txt Files/" || true