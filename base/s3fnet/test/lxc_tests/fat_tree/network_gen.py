

import sys
import os
import argparse



parser = argparse.ArgumentParser(description='Generates k-ary fat tree topology')
parser.add_argument('--num_emu_hosts', type=int,
                    help='Max number of emulated hosts', default=20)
parser.add_argument('--k', type=int, required=False, help='k-ary fat-tree topology',
                    default=16)
parser.add_argument('--mpi_type', type=str, default='mm')         
parser.add_argument('--run_time', type=float, default=20)
parser.add_argument('--enable_lookahead', type=int, default=1)
parser.add_argument('--fraction_servers', type=float, required=False,
                    help='Fraction of simulated hosts which are tcp servers',
                    default=0.1)


pod_num_emu_hosts_mapping = {}
pod_reserved_intfs_mapping = {}
pod_emu_netids = {}
pod_simulated_client_nhis = {}
pod_simulated_server_nhis = {}

def fill_pod_sim_hosts_mapping(num_emu_hosts, k, fraction_servers):
    global pod_num_emu_hosts_mapping
    global pod_simulated_client_nhis
    global pod_simulated_server_nhis

    for pod_no in range(0, k):
        pod_num_emu_hosts_mapping[pod_no] = 0
    num_used_hosts = 0
    while num_used_hosts < num_emu_hosts:
        for pod_no in range(0, k):
            pod_num_emu_hosts_mapping[pod_no] += 1
            num_used_hosts += 1

            if num_used_hosts == num_emu_hosts:
                break


    for pod_no in range(0, k):
        num_hosts_in_pod = int(k * k/4)
        num_sim_hosts_in_pod = num_hosts_in_pod - pod_num_emu_hosts_mapping[pod_no]
        num_sim_tcp_servers_added = max(1, int(num_sim_hosts_in_pod * fraction_servers))
        num_sim_tcp_clients_added = num_sim_hosts_in_pod - num_sim_tcp_servers_added
    

        pod_netid = pod_no + 1
        pod_tcp_client_host_start_id = k
        pod_tcp_client_host_end_id = k + num_sim_tcp_clients_added - 1
        pod_tcp_server_host_start_id = k + num_sim_tcp_clients_added
        pod_tcp_server_host_end_id = k + num_sim_tcp_clients_added + num_sim_tcp_servers_added - 1

        pod_simulated_client_nhis[pod_no] = (pod_netid, pod_tcp_client_host_start_id, 
            pod_tcp_client_host_end_id)
        pod_simulated_server_nhis[pod_no] = (pod_netid, pod_tcp_server_host_start_id,
            pod_tcp_server_host_end_id)

def get_sim_traffic_pattern(k):

    pattern_string = ""
    for pod_no in range(0, k):
        dest_pod = (pod_no + int(k/2)) % (k)
        dest_pod_netid, serv_start, server_end = pod_simulated_server_nhis[dest_pod]
        start = f"{dest_pod_netid}:{serv_start}"
        end = f"{dest_pod_netid}:{server_end}"

        if start == end:
            servers = f"""servers [ port 1024 nhi {start}(0) list "forTCP" ]"""
        else:
            servers = f"""servers [ port 1024 nhi_range [from {start}(0) to {end}(0)] list "forTCP" ]"""
        
        src_pod, cli_start, cli_end = pod_simulated_client_nhis[pod_no]
        for cli in range(cli_start, cli_end + 1):
            client = f"client {src_pod}:{cli}"
            pattern = f"""
        pattern [
            {client}
            {servers}
        ]"""
            pattern_string += pattern
    full_pattern = f"""
    traffic [
        {pattern_string}
    ]
    """
    return full_pattern




def generate_core_sim_network(k):

    num_core_switches = int(k/2) * int(k/2)
    intfs = ""
    for intf in range(0, k):
        intfs += f"""
            interface [id {intf} _extends .dict.100Gb]"""

    router_cfg = ""
    for i in range(0, num_core_switches):
        router =f"""
        router
        [
            id {i}
            _find .dict.routerGraph.graph
            {intfs}
        ]"""
        router_cfg += router

    CoreNet = f"""
    coreNetwork [
        {router_cfg}
    ]
        """
    return CoreNet

def get_emulated_host_cfgs(k):
    global pod_emu_netids
    global pod_num_emu_hosts_mapping
    tl = 1
    emu_cfg = ""
    for pod_no in range(0, k):
        
        pod_emu_netids[pod_no] = []
        for host_tl in range(tl,  tl + pod_num_emu_hosts_mapping[pod_no]):
            curr_host_cfg = f"""
    Net 
    [ 
        id {host_tl + k}
        alignment {host_tl}
        host 
        [ 
            id 0
            _extends .dict.emuHost
        ]
    ]
            """
            emu_cfg += curr_host_cfg
            pod_emu_netids[pod_no].append(host_tl + k)
        tl += pod_num_emu_hosts_mapping[pod_no]
    return emu_cfg

def get_lxc_cfg_string(params, k, num_emu_hosts):

    global pod_emu_netids
    mpiCmdPath = params['cmd']
    ttnProject = params['ttnProject']
    logDir = params['logDir']
    settings_string = ""

    rank = 0
    for pod_no in range(0, k):
        for emu_netid in pod_emu_netids[pod_no]:
            if rank == 0:
                fullCmd = f"{mpiCmdPath} {rank} {num_emu_hosts} {emu_netid}:0 > {logDir}/master.log"
            else:
                fullCmd = f"{mpiCmdPath} {rank} {num_emu_hosts} {emu_netid}:0 > {logDir}/worker{rank}.log"
            lxc_settings = f"""
        settings [ lxcNHI {emu_netid}:0 ttnProject "{ttnProject}" cmd "{fullCmd}" ]"""
            settings_string += lxc_settings
            rank += 1

        
    lxc_config_string = f"""
    lxcConfig
	[
        {settings_string}
    ]
    """
    return lxc_config_string


def get_emu_host_links(k):
    # Connect each emulated host in lan to corresponding edge switch
    global pod_emu_netids
    global pod_num_emu_hosts_mapping
    global pod_reserved_intfs_mapping

    EmuHostLinks = ""
    
    for pod_no in range(0, k):
        emuHostNo = 0
        emuHostSwitchIntfMapping = {}

        for edgeSwitchIdx, num_rsvd in enumerate(pod_reserved_intfs_mapping[pod_no]):
            #print ("Edge Switch Id = ", edgeSwitchIdx, " Num Rsvd = ", num_rsvd)
            for intf in range(0, num_rsvd):
                emuHostSwitchIntfMapping[emuHostNo] = (edgeSwitchIdx, intf)
                emuHostNo += 1

        emuHostNo = 0
        for emu_netid in pod_emu_netids[pod_no]:
            pod_sim_netid = pod_no + 1
            edgeSwitchIdx, edgeSwitchIntf = emuHostSwitchIntfMapping[emuHostNo]
            EmuHostLinks += f"""
    link [ attach {emu_netid}:0(0) attach {pod_sim_netid}:{edgeSwitchIdx}({edgeSwitchIntf}) _extends .dict.link_delay_1us ]"""
            emuHostNo += 1
    return EmuHostLinks



coreSwitchUsedIntfs = {}

def generate_core_pod_links(pod_no, k):
    global coreSwitchUsedIntfs
    podCoreLinks = ""
    coreSwitchIdStart = 0

    for currPodSwitchId in range(int(k/2), k):
        #if currPodSwitchId % 2 == 0:
        #    coreSwitchIdStart = 0
        #else:
        
        currCoreSwitchId = coreSwitchIdStart
        for currPodSwitchIntf in range(int(k/2), k):
            currCoreSwitchIntf = coreSwitchUsedIntfs[currCoreSwitchId] + 1
            coreSwitchUsedIntfs[currCoreSwitchId] = currCoreSwitchIntf
            podCoreLinks += f"""
    link [ attach {pod_no+1}:{currPodSwitchId}({currPodSwitchIntf}) attach 0:{currCoreSwitchId}({currCoreSwitchIntf}) _extends .dict.link_delay_1us ]"""
            currCoreSwitchId += 1
            
        coreSwitchIdStart += int(k/2)
    return podCoreLinks

def generate_all_core_pod_links(k):

    num_core_switches = int(k/2) * int(k/2)
    for i in range(0, num_core_switches):
        coreSwitchUsedIntfs[i] = -1

    allPodCoreLinks = ""
    for pod_no in range(0, k):
        allPodCoreLinks += generate_core_pod_links(pod_no, k)
    return allPodCoreLinks


def generate_pod_sim_network(pod_no, k, fraction_servers):
    # Two levels
    global pod_num_emu_hosts_mapping
    global pod_reserved_intfs_mapping

    num_emu_hosts_in_pod = min(pod_num_emu_hosts_mapping[pod_no], int(k*k/4))
    num_sim_hosts_in_pod = int(k*k/4) - num_emu_hosts_in_pod
    if num_sim_hosts_in_pod == 0:
        num_sim_tcp_clients_added = 0
        num_sim_tcp_servers_added = 0
    else:
        num_sim_tcp_servers_added = max(1, int(num_sim_hosts_in_pod * fraction_servers))
        num_sim_tcp_clients_added = num_sim_hosts_in_pod - num_sim_tcp_servers_added
    
    intfs = ""
    for intf in range(0, k):
        intfs += f"""
            interface [id {intf} _extends .dict.100Gb]"""

    router_cfg = ""
    for i in range(0, k):
        router =f"""
        router
        [
            id {i}
            _find .dict.routerGraph.graph
            {intfs}
        ]"""
        router_cfg += router

    pod_reserved_intfs_mapping[pod_no] = [] 
    for i in range(0, int(k/2)):
        pod_reserved_intfs_mapping[pod_no].append(0)

    i = 0
    while i < num_emu_hosts_in_pod:
        pod_reserved_intfs_mapping[pod_no][i % int(k/2)] += 1
        i += 1


    # SimHost-Edge Switch Links
    numSimHostLinks = num_sim_hosts_in_pod
    currEdgeSwitchId = 0
    currEdgeSwitchIntf = pod_reserved_intfs_mapping[pod_no][currEdgeSwitchId]
    numMappedHosts = pod_reserved_intfs_mapping[pod_no][currEdgeSwitchId]
    
    SimHostLinks = ""
    for host in range(k, k + numSimHostLinks):
        if numMappedHosts == int(k/2):
            #print ("Curr Switch = ", currEdgeSwitchId, numSimHostLinks)
            numMappedHosts = pod_reserved_intfs_mapping[pod_no][currEdgeSwitchId + 1]
            currEdgeSwitchIntf = pod_reserved_intfs_mapping[pod_no][currEdgeSwitchId + 1]
            currEdgeSwitchId += 1
        
        SimHostLinks += f"""
        link [ attach {host}(0) attach {currEdgeSwitchId}({currEdgeSwitchIntf}) _extends .dict.link_delay_1us ]"""

        numMappedHosts += 1
        currEdgeSwitchIntf += 1

    # Edge-Agg switch links
    edgeAggLinks = ""
    currEdgeSwitchId = 0
    currAggSwitchIntf = 0
    
    for edgeSwitch in range(0, int(k/2)):
        currEdgeSwitchIntf = int(k/2)
        for aggSwitch in range(int(k/2), k):
            edgeAggLinks += f"""
        link [ attach {edgeSwitch}({currEdgeSwitchIntf}) attach {aggSwitch}({currAggSwitchIntf}) _extends .dict.link_delay_1us ]"""
            currEdgeSwitchIntf += 1

        currAggSwitchIntf += 1


    if num_sim_tcp_clients_added == 0:
        podDict = f"""
    podNet{pod_no} [
        {router_cfg}
        {SimHostLinks}
        {edgeAggLinks}
    ]
        """
        return podDict
  
    if num_sim_tcp_servers_added > 1:
        podDict = f"""
    podNet{pod_no} [
        {router_cfg}
        host 																	# Host 1:0
        [ 
            idrange [from {k} to {k + num_sim_tcp_clients_added -1}]
            _extends .dict.TCPClient
        ]
        host 																	# Host 1:0
        [ 
            idrange [from {k + num_sim_tcp_clients_added} to {k + num_sim_tcp_clients_added + num_sim_tcp_servers_added - 1}]
            _extends .dict.TCPServer
        ]
        {SimHostLinks}
        {edgeAggLinks}
    ]
        """
    else:
        podDict = f"""
    podNet{pod_no} [
        {router_cfg}
        host 																	# Host 1:0
        [ 
            idrange [from {k} to {k + num_sim_tcp_clients_added - 1}]
            _extends .dict.TCPClient
        ]
        host 																	# Host 1:0
        [ 
            id {k + num_sim_tcp_clients_added}
            _extends .dict.TCPServer
        ]
        {SimHostLinks}
        {edgeAggLinks}
    ]
        """
    return podDict
    
    
def compose_all_sim_nets(k):
    sim_net_string = """
    Net [
        id 0
        alignment 0
        _extends .sim.coreNetwork
    ]
        """
    
    for pod_no in range(0, k):
        curr_sim_net = f"""
    Net [
        id {pod_no + 1}
        alignment 0
        _extends .sim.podNet{pod_no}
    ]
        """
        sim_net_string += curr_sim_net
    return sim_net_string


def main():
    args = parser.parse_args()

    

    from os.path import expanduser
    home = expanduser("~")
    k = args.k
    num_emu_hosts = min(args.num_emu_hosts, int(k*k*k/4))
    total_num_timelines = num_emu_hosts + 1

    if args.enable_lookahead:
        lookahead_status = "LA_Enabled"
    else:
        lookahead_status = "LA_Disabled"

    if total_num_timelines > 1:
       
        log_dir = f"MPI_{lookahead_status}_nemus_{total_num_timelines - 1}_mpi_{args.mpi_type}"
        if args.mpi_type == 'mm':
            mpiCmd = f"{home}/VT-S3FNet/csudp/mpi_matrix/mpi_mm"
            ttnProject = 'mpi_mat'
        elif args.mpi_type == 'int':
            mpiCmd = f"{home}/VT-S3FNet/csudp/mpi_integral/mpi_int"
            ttnProject = 'mpi_int'
        elif args.mpi_type == 'sat':
            mpiCmd = f"{home}/VT-S3FNet/csudp/mpi_sat/mpi_csat"
            ttnProject = 'mpi_sat'
        else:
            mpiCmd = f"{home}/VT-S3FNet/csudp/mpi_norm/mpi_norm"
            ttnProject = 'mpi_norm'

    else:
        log_dir = "MPI_FullSim"
        mpiCmd = f"{home}/VT-S3FNet/csudp/mpi_mm/mpi_test"
        ttnProject = 's3fmpi'


    
    logDirPath = f"{home}/VT-S3FNet/experiment-data"
    params = {
        'cmd': mpiCmd,
        'ttnProject': ttnProject,
        'logDir': f"{logDirPath}/{log_dir}"
    }

    fill_pod_sim_hosts_mapping(num_emu_hosts, k, args.fraction_servers)
    emu_host_cfg = get_emulated_host_cfgs(k)

    pod_sim = ""
    for pod_no in range(0, k):
        pod_sim += generate_pod_sim_network(pod_no, k, args.fraction_servers)
    
    pod_sim += generate_core_sim_network(k)

    basic_sim_dict = f"""
sim [
    {pod_sim}
]
    """
    with open('sim.dml', 'w') as f:
        f.write(basic_sim_dict)

    
    if total_num_timelines > 1:
        overall_cfg = f"""
total_timeline {total_num_timelines}	
tick_per_second 6	
run_time {args.run_time + 0.1}
seed 1	
log_dir "{log_dir}"		
virtual_time_manager "TITAN"
max_lookahead_us 1000
enable_lookahead {args.enable_lookahead}

Net [

    # LXC Config settings
{get_lxc_cfg_string(params, k, num_emu_hosts)}

    # Simulated TCP Traffic Pattern
{get_sim_traffic_pattern(k)}

    # Composed Sim Nets
{compose_all_sim_nets(k)}

    # Composed Emulated Hosts
{emu_host_cfg}

    # Links between agg switch and core network
{generate_all_core_pod_links(k)}

    # Links between emu hosts and edge routers
{get_emu_host_links(k)}

]
    """
    else:
        overall_cfg = f"""
total_timeline {total_num_timelines}	
tick_per_second 6	
run_time {args.run_time + 0.1}
seed 1	
log_dir "{log_dir}"		
virtual_time_manager "TITAN"
max_lookahead_us 1000
enable_lookahead {args.enable_lookahead}

Net [

    # Simulated TCP Traffic Pattern
{get_sim_traffic_pattern(k)}

    # Composed Sim Nets
{compose_all_sim_nets(k)}

    # Links between agg switch and core network
{generate_all_core_pod_links(k)}

]
    """


    with open('test.dml', 'w') as f:
        f.write(overall_cfg)
    
if __name__ == "__main__":
    main()





