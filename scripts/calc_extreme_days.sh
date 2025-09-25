#!/bin/bash

# Local paths
HOME_DIR="/home/benjamin"
MODULE_DIR="${HOME_DIR}/dlesymanalysis"
OUTPUT_DIR="${MODULE_DIR}/outputs"

# Input paths
GBUCKET="gs://dlesym-storage"
OCEAN_STORE="${GBUCKET}/ocean_prediction_scaled.zarr"
ATMOS_STORE="${GBUCKET}/atmos_prediction_scaled.zarr"
OCEAN_PERCENTILES_PATH="${GBUCKET}/ocean_percentiles.zarr"
ATMOS_PERCENTILES_PATH="${GBUCKET}/atmos_percentiles.zarr"

# Output paths
OUTPUT_FILE="${OUTPUT_DIR}/calc_extreme_days.out" # Path to catch errors and logs
OCEAN_PATH="${GBUCKET}/ocean_extreme_days.zarr"
ATMOS_PATH="${GBUCKET}/atmos_extreme_days.zarr"


#############################################################
cd ${MODULE_DIR}
export PYTHONPATH=${HOME_DIR}

# Delete the output file if it already exists
if [ -f ${OUTPUT_FILE} ]; then
    rm ${OUTPUT_FILE}
fi

RUN_CMD="python scripts/calc_extreme_days.py \
    --ocean-store ${OCEAN_STORE} \
    --atmos-store ${ATMOS_STORE} \
    --ocean-output ${OCEAN_PATH} \
    --atmos-output ${ATMOS_PATH} \
    --ocean-quantiles-path ${OCEAN_PERCENTILES_PATH} \
    --atmos-quantiles-path ${ATMOS_PERCENTILES_PATH}"

# If output file is given, redirect output
if [[ -n "${OUTPUT_FILE}" ]]; then
    ${RUN_CMD} &>> ${OUTPUT_FILE}
else
    ${RUN_CMD}
fi
