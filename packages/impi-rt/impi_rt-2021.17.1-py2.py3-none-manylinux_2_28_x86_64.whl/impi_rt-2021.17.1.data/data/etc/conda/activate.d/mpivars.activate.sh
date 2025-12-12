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

if [ "${SETVARS_CALL}" != "1" ]
then
    export I_MPI_ROOT="${CONDA_PREFIX}"

    # PATH is setup by Conda automatically.

    if [ -z "${CLASSPATH}" ]
    then
        export CLASSPATH="${I_MPI_ROOT}/lib/mpi.jar"
    else
        export CLASSPATH="${I_MPI_ROOT}/lib/mpi.jar:${CLASSPATH}"
    fi

    # MPI libs will be found through python. No needs to set LD_LIBRARY_PATH.

    if [ -z "${MANPATH}" ]
    then
        export MANPATH="${I_MPI_ROOT}/share/man":`manpath 2>/dev/null`
    else
        export MANPATH="${I_MPI_ROOT}/share/man:${MANPATH}"
    fi

    if [ -z "${I_MPI_OFI_LIBRARY_INTERNAL}" ]
    then
        i_mpi_ofi_library_internal="1"
    else
        i_mpi_ofi_library_internal="${I_MPI_OFI_LIBRARY_INTERNAL}"
    fi

    case "$i_mpi_ofi_library_internal" in
        0|no|off|disable)
            ;;
        1|yes|on|enable)
            export PATH="${I_MPI_ROOT}/bin/libfabric:${PATH}"
            export LD_LIBRARY_PATH="${I_MPI_ROOT}/lib:${LD_LIBRARY_PATH}"
            if [ -z "${LIBRARY_PATH}" ]
            then
                export LIBRARY_PATH="${I_MPI_ROOT}/lib"
            else
                export LIBRARY_PATH="${I_MPI_ROOT}/lib:${LIBRARY_PATH}"
            fi
            if [ -n "$( cat /etc/*release* 2>/dev/null | grep -i "Ubuntu" )" ];
            then
                export FI_PROVIDER_PATH="${I_MPI_ROOT}/lib:/usr/lib/x86_64-linux-gnu/libfabric"
            else
                export FI_PROVIDER_PATH="${I_MPI_ROOT}/lib:/usr/lib64/libfabric"
            fi
            ;;
        *)
            ;;
    esac
fi

