
#include <s3f.h>
#include "virtual_time_manager.h"


#ifdef ENABLED_VT_MANAGER_TITAN
extern "C" 
{
    #include <VT_functions.h>
    #include <utility_functions.h>
}
#else
extern "C" 
{
    #include <Kronos_functions.h>
    #include <kronos_utility_functions.h>
}
#endif

using namespace s3f;

#ifdef ENABLED_VT_MANAGER_TITAN
//! Sends the command to the virtual time module as an ioctl call
s64 SendToKronosModule(
    unsigned int cmd, ioctl_args* arg) {
    int fp = open("/proc/kronos", O_RDWR);
    int ret = 0;
    struct timeval vt;
    if (fp < 0) {
        printf("ERROR communicating with VT module: Could not open proc file\n");
        return -1;
    }

    if (cmd != VT_GET_CURRENT_VIRTUAL_TIME) {
        if (!arg) {
            printf("ERROR communicating with VT module: Missing argument !\n");
            close(fp);
            return -1;
        }
        if (strlen(arg->cmd_buf) > BUF_MAX_SIZE) {
            printf("ERROR communicating with VT module: Too much data to copy !\n");
            close(fp);
            return -1;
        }
        ret = ioctl(fp, cmd, arg);
        if (ret < 0) {
            close(fp);
            return ret;
        }
    } else {
        ret = ioctl(fp, VT_GET_CURRENT_VIRTUAL_TIME, (struct timeval *)&vt);
        if (ret < 0) {
            printf("Error executing VT_GET_CURRENT_VIRTUAL_TIME cmd\n");
            close(fp);
            return ret;
        }
        close(fp);
        return (vt.tv_sec * 1000000 + vt.tv_usec) * 1000;
    }
    close(fp);
    if (cmd == VT_WRITE_RESULTS ||
        cmd == VT_REGISTER_TRACER ||
        cmd == VT_GETTIME_TRACER)
        return arg->cmd_value;
    return ret;
}
#endif

//! Returns the current virtual time of a tracer with specified id
s64 VirtualTimeManagerInterface::GetCurrentVirtualTimeTracer(int tracer_id) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return GetCurrentTimeTracer(tracer_id);
    }

    ioctl_args arg;
    InitIoctlArg(&arg);
    if (tracer_id < 0) {
        printf("getCurrentTimeTracer: incorrect id: %d\n", tracer_id);
        return -1;
    }
    sprintf(arg.cmd_buf, "%d", tracer_id);
    return SendToKronosModule(VT_GETTIME_TRACER, &arg);
    #else
    return getCurrentTimeTracer(tracer_id);
    #endif
}


//! Returns encapsulated tracer start command
std::string VirtualTimeManagerInterface::GetEncalsulatedTracerCommand(
    int tracer_id, int timeline_id, float rel_cpu_speed, std::string ttn_project,
    std::string cmd) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::KRONOS) {
        return "/usr/bin/tracer -i " + std::to_string(tracer_id) + " -t "
               + std::to_string(timeline_id)
               + " -r " + std::to_string(rel_cpu_speed)
               + " -c \"" + cmd + "\"";
    }
    return "/usr/bin/ttn_tracer -i " + std::to_string(tracer_id)
            + " -t " + std::to_string(timeline_id)
            + " -e 2" + " -p " + ttn_project
            + " -c \"" + cmd + "\"";
    #else
        return "/usr/bin/tracer -i " + std::to_string(tracer_id) + " -t "
               + std::to_string(timeline_id)
               + " -r " + std::to_string(rel_cpu_speed)
               + " -c \"" + cmd + "\"";
    #endif
}



int VirtualTimeManagerInterface::InitializeVirtualTimeExp(
    int num_timelines, int num_expected_tracers) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return InitializeVtExp(EXP_CS, num_timelines, num_expected_tracers);
    }
    ioctl_args arg;
    InitIoctlArg(&arg);
    if (num_expected_tracers < 0) {
        printf("InitializeVtExp: num expected tracers: %d < 0 !\n",
            num_expected_tracers);
        return -1;
    }

    if (num_timelines <= 0) {
        printf("InitializeVtExp: Number of timelines cannot be <= 0\n");
        return -1;
    }

    sprintf(arg.cmd_buf, "%d,%d,%d", EXP_CS, num_timelines,
            num_expected_tracers);

    return SendToKronosModule(VT_INITIALIZE_EXP, &arg);
    #else
    return initializeVtExp(EXP_CS, num_timelines, num_expected_tracers);
    #endif
}


//! Synchronizes and Freezes all started tracers
int VirtualTimeManagerInterface::SyncAndFreezeVirtualTimeExp(void) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return SynchronizeAndFreeze();
    }
    ioctl_args arg;
    InitIoctlArg(&arg);
    return SendToKronosModule(VT_SYNC_AND_FREEZE, &arg);
    #else
    return synchronizeAndFreeze();
    #endif
}

//! Initiates Stoppage of the experiment
int VirtualTimeManagerInterface::StopVirtualTimeExp(void) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return StopExp();
    }
    ioctl_args arg;
    InitIoctlArg(&arg);
    return SendToKronosModule(VT_STOP_EXP, &arg);
    #else
    return stopExp();
    #endif
}


//! Advance a EXP_CS timeline by the specified duration. 
int VirtualTimeManagerInterface::RunTimelineFor(int timeline_id, s64 duration) {

    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return ProgressTimelineBy(timeline_id, duration);
    }
    if (timeline_id < 0 || duration <= 0) {
        printf("progress_timeline_By: incorrect arguments !\n");
        return -1;
    }
    ioctl_args arg;
    InitIoctlArg(&arg);
    sprintf(arg.cmd_buf, "%d,", timeline_id);
    arg.cmd_value = duration;
    return SendToKronosModule(VT_PROGRESS_TIMELINE_BY, &arg);
    #else
    return progressTimelineBy(timeline_id, duration);
    #endif
}

//! Gets the packet send time given its hash. 
s64 VirtualTimeManagerInterface::GetPktSendTime(int tracer_id, int pkt_hash) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return GetPktSendTimeAPI(tracer_id, pkt_hash);
    }
    #endif
    return GetCurrentVirtualTimeTracer(tracer_id);
}


//! Sets the earliest arrival time for a tracer. 
int VirtualTimeManagerInterface::SetTracerEarliestArrivalTime(
    int tracer_id, s64 eat_tstamp) {
    #ifdef ENABLED_VT_MANAGER_TITAN    
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return SetEarliestArrivalTime(tracer_id, eat_tstamp);
    }
    #endif
    return 0;
}


//! Returns the lookahead of a node. This API could be used by a network simulator
//  Returns absolute timestamp.
s64 VirtualTimeManagerInterface::GetTracerLookaheadTimestamp(int tracer_id) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return GetTracerLookahead(tracer_id);
    }
    #endif
    return GetCurrentVirtualTimeTracer(tracer_id);
}

s64 VirtualTimeManagerInterface::GetTracerLookaheadExclTimestamp(int tracer_id) {
    #ifdef ENABLED_VT_MANAGER_TITAN
    if (vtManagerType == VirtualTimeManagerType::TITAN) {
        return GetTracerNEATLookahead(tracer_id);
    }
    #endif
    return GetCurrentVirtualTimeTracer(tracer_id);
}

