#!/usr/bin/env bash
# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Script which validates sample pack config against the pack config schema.
#

if [ $# -ne 1 ]; then
    echo "Usage: ${0} <path to pack directory>"
    exit 1
fi

if [ ! -d ${PACK_DIR} ]; then
    echo "Pack directory \"${PACK_DIR}\" doesn't exist"
    exit 2
fi

PACK_DIR=$1
PACK_NAME=$(basename $PACK_DIR)

VALIDATE_SCRIPT_PATH="${ST2_REPO_PATH}/st2common/bin/st2-validate-pack-config"

CONFIG_SCHEMA_FILE=$(find ${PACK_DIR}/config.schema.yaml)
EXAMPLE_CONFIG_FILE=$(find ${PACK_DIR}/*.yaml.example)

if [ -z ${CONFIG_SCHEMA_FILE} ]; then
    echo "Pack ${PACK_NAME} doesn't contain config.schema.yaml file"
    exit 0
fi

if [ -z ${EXAMPLE_CONFIG_FILE} ]; then
    echo "No sample config file found for pack ${PACK_NAME}"
    exit 0
else
    echo "Validating example config ${EXAMPLE_CONFIG_FILE} for pack ${PACK_NAME}..."
    ${VALIDATE_SCRIPT_PATH} --schema-path ${CONFIG_SCHEMA_FILE} --config-path ${EXAMPLE_CONFIG_FILE}
    EXIT_CODE=$?
    exit ${EXIT_CODE}
fi
