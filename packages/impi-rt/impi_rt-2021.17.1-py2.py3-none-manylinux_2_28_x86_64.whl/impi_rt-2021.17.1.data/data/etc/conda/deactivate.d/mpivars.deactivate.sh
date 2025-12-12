#!/bin/sh
#
# Copyright Intel Corporation.
# 
# This software and the related documents are Intel copyrighted materials, and
# your use of them is governed by the express license under which they were
# provided to you (License). Unless the License provides otherwise, you may
# not use, modify, copy, publish, distribute, disclose or transmit this
# software or the related documents without Intel's prior written permission.
# 
# This software and the related documents are provided as is, with no express
# or implied warranties, other than those that are expressly stated in the
# License.
#

# remove the first occurrence from the list 
__internal_remove_impi_env_variable_path() {
    var_name="$1"
    remove_path="$2"
    var_value=$(eval echo \"\$$var_name\")

    new_value=$(echo "$var_value" | awk -F: -v remove="^$remove_path\$" '
    BEGIN { OFS = ":" }
    {
        removed = 0
        for (i = 1; i <= NF; i++) {
            if (!removed && $i ~ remove) {
                removed = 1
                continue
            }
            printf "%s%s", (i > 1 ? OFS : ""), $i
        }
        print ""
    }' | sed 's/:$//')

    eval "export $var_name=\"$new_value\""
}

if [ "${SETVARS_CALL}" != "1" ]
then

    export CLASSPATH=`echo ${CLASSPATH} | sed "s|${CONDA_PREFIX}/lib/mpi.jar:\?||"`
    __internal_remove_impi_env_variable_path LD_LIBRARY_PATH "${CONDA_PREFIX}/lib"
    __internal_remove_impi_env_variable_path MANPATH "${CONDA_PREFIX}/share/man"
    __internal_remove_impi_env_variable_path LIBRARY_PATH "${CONDA_PREFIX}/lib"
    __internal_remove_impi_env_variable_path PATH "${CONDA_PREFIX}/bin/libfabric"

    # if fi_info is on the PATH and part of compilers_and_libraries, set I_MPI_ROOT to the root of that location
    FIP=`which fi_info`
    if echo "${FIP}" | grep -q "compilers_and_libraries.*mpi"; then
        export I_MPI_ROOT=`echo ${FIP} | rev| cut -f1 -d' '| rev| sed "s|/intel64/libfabric/bin/fi_info||"`
    # if fi_info is part of oneAPI, set I_MPI_ROOT as root from oneAPI.
    elif echo "${FIP}" | grep -q "/mpi/"; then
        export I_MPI_ROOT=`echo ${FIP} | rev| cut -f1 -d' '| rev| sed "s|/libfabric/bin/fi_info||"`
    else
        export I_MPI_ROOT=
    fi

    # only change FI_PROVIDER_PATH if it points to the python prefix
    if echo "${FI_PROVIDER_PATH}" | grep -q "${CONDA_PREFIX}"; then
        # if I_MPI_ROOT is set, set the provider path to MPI's prov dir
        if [[ "${I_MPI_ROOT}" != "" ]]; then
            # if I_MPI_ROOT from PSXE package
            if echo "${I_MPI_ROOT}" | grep -q "compilers_and_libraries.*mpi"; then
                if [ -n "$( cat /etc/*release* 2>/dev/null | grep -i "Ubuntu" )" ]; then
                    export FI_PROVIDER_PATH=${I_MPI_ROOT}/intel64/libfabric/lib/prov:/usr/lib/x86_64-linux-gnu/libfabric
                else
                    export FI_PROVIDER_PATH=${I_MPI_ROOT}/intel64/libfabric/lib/prov:/usr/lib64/libfabric
                fi
            # if I_MPI_ROOT from oneAPI package
            else
                if [ -n "$( cat /etc/*release* 2>/dev/null | grep -i "Ubuntu" )" ]; then
                    export FI_PROVIDER_PATH=${I_MPI_ROOT}/libfabric/lib/prov:/usr/lib/x86_64-linux-gnu/libfabric
                else
                    export FI_PROVIDER_PATH=${I_MPI_ROOT}/libfabric/lib/prov:/usr/lib64/libfabric
                fi
            fi
        else
            export FI_PROVIDER_PATH=
        fi
    fi
fi
