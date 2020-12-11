#ifndef __VIRTUAL_TIME_MANAGER_H
#define __VIRTUAL_TIME_MANAGER_H

#include <string>
#include "tk_lxc_manager.h"

typedef long long s64;

namespace s3f {

class VirtualTimeManagerInterface {

public:
    VirtualTimeManagerType vtManagerType;

    VirtualTimeManagerInterface(VirtualTimeManagerType vtManagerType) :
        vtManagerType(vtManagerType) {};

    //! Returns the current virtual time of a tracer with specified id
    s64 GetCurrentVirtualTimeTracer(int tracer_id);

    //! Returns encapsulated tracer start command
    std::string GetEncalsulatedTracerCommand(
        int tracer_id, int timeline_id, float rel_cpu_speed, std::string ttn_project,
        std::string cmd, std::string ipAddr);


    //! Initializes a virtual time managed experiment
    /*!
        \param num_timelines Number of timelines (in case of EXP_CS). Set to 0 for EXP_CBE 
        \param num_expected_tracers Number of tracers which would be spawned
    */
    int InitializeVirtualTimeExp(int num_timelines, int num_expected_tracers);


    //! Synchronizes and Freezes all started tracers
    int SyncAndFreezeVirtualTimeExp(void);

    //! Initiates Stoppage of the experiment
    int StopVirtualTimeExp(void);


    //! Advance a EXP_CS timeline by the specified duration. 
    int RunTimelineFor(int timeline_id, s64 duration);

    //! Gets the packet send time given its hash. 
    s64 GetPktSendTime(int tracer_id, int pkt_hash);


    //! Sets the earliest arrival time for a tracer. 
    int SetTracerEarliestArrivalTime(int tracer_id, s64 eat_tstamp);


    //! Returns the lookahead of a node. This API could be used by a network simulator
    //  Returns absolute timestamp.
    s64 GetTracerLookaheadTimestamp(int tracer_id);

    //! Returns the lookahead of a node after excluding all threads/processes which
    //  are currerntly blocked on a packet receive.
    s64 GetTracerLookaheadExclTimestamp(int tracer_id);
};


}

#endif