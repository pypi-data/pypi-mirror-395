#!/bin/sh

# ifstate: wrapper to run hooks

# debugging
export IFS_VERBOSE=${verbose}
if [ "$$IFS_VERBOSE" = 1 ]; then
    set -x
fi

# return codes
export IFS_RC_OK="${rc_ok}"
export IFS_RC_ERROR="${rc_error}"
export IFS_RC_STARTED="${rc_started}"
export IFS_RC_STOPPED="${rc_stopped}"
export IFS_RC_CHANGED="${rc_changed}"

# generic environment variables
export IFS_SCRIPT="${script}"
export IFS_RUNDIR="${rundir}"

export IFS_IFNAME="${ifname}"
export IFS_INDEX="${index}"
export IFS_NETNS="${netns}"
export IFS_VRF="${vrf}"

# hook arguments
${args}

# run hook NetNS and VRF aware
if [ -z "$$IFS_NETNS" ]; then
    if [ -z "$$IFS_VRF" ]; then
        # just exec the script
        exec "$$IFS_SCRIPT" "$$@"
    else
        # exec in VRF
        exec ip vrf exec "$$IFS_VRF" "$$IFS_SCRIPT" "$$@"
    fi
else
    if [ -z "$$IFS_VRF" ]; then
        # exec in NetNS
        exec ip netns exec "$$IFS_NETNS" "$$IFS_SCRIPT" "$$@"
    else
        # exec in NetNS->VRF
        exec ip -n "$$IFS_NETNS" vrf exec "$$IFS_VRF" "$$IFS_SCRIPT" "$$@"
    fi
fi

# somthing gone wrong
return $$IFS_RC_ERROR
