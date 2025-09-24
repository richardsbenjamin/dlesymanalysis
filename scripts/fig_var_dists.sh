#!/bin/bash

# Local paths
HOME_DIR="/home/benjamin"
MODULE_DIR="${HOME_DIR}/dlesymanalysis"
OUTPUT_DIR="${MODULE_DIR}/outputs"

# Input paths
GBUCKET="gs://dlesym-storage"
OCEAN_STORE="${GBUCKET}/ocean_prediction_scaled.zarr"
ATMOS_STORE="${GBUCKET}/atmos_prediction_scaled.zarr"

# Output paths
OUTPUT_FILE="${OUTPUT_DIR}/fig_var_dists.out" # Path to catch errors and logs
SINGLES_PATH="https://data.earthdatahub.destine.eu/era5/reanalysis-era5-single-levels-v0.zarr"
FIG_SAVE_PATH="${GBUCKET}/var_dists.png"


#############################################################
cd ${MODULE_DIR}
export PYTHONPATH=${HOME_DIR}

# Delete the output file if it already exists
if [ -f ${OUTPUT_FILE} ]; then
    rm ${OUTPUT_FILE}
fi

RUN_CMD="python scripts/fig_var_dists.py \
    --ocean-store ${OCEAN_STORE} \
    --atmos-store ${ATMOS_STORE} \
    --singles-path ${SINGLES_PATH} \
    --fig-save-path ${FIG_SAVE_PATH}"

# If output file is given, redirect output
if [[ -n "${OUTPUT_FILE}" ]]; then
    ${RUN_CMD} &>> ${OUTPUT_FILE}
else
    ${RUN_CMD}
fi
