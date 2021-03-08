import sys
import os
import argparse

TOTAL_LANS = 20
TOTAL_BACKBONE_ROUTERS = 18

parser = argparse.ArgumentParser(description='Generates campus network topology')
parser.add_argument('--num_sim_hosts_per_lan', type=int,
                    help='Number of simulated hosts per lan', default=50)
parser.add_argument('--num_emu_hosts_per_lan', type=int,
                    help='Number of emulated hosts per lan', default=1)
parser.add_argument('--fraction_servers', type=float, required=False,
                    help='Fraction of simulated hosts which are tcp servers',
                    default=0.1)
parser.add_argument('--emu_flow_type', type=str, default='periodic')
parser.add_argument('--emu_flow_period_us', type=int, default=200000)
parser.add_argument('--emu_flow_mean_arrival_us', type=int, default=200000)
parser.add_argument('--transfer_size_kb', type=int, default=8)
parser.add_argument('--transfer_rate_mbps', type=int, default=10)
parser.add_argument('--run_time', type=int, default=10)
parser.add_argument('--enable_lookahead', type=int, default=1)

backbone_network = """
    # Reference. https://www.researchgate.net/figure/The-DARPA-NMS-campus-network-instrumented-with-CAPE_fig13_224710922
    Net 
    [ 
        id 0    
        alignment 0		
        router																	# Router 0:0
        [
            id 0    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
        ]
        router																	# Router 0:1
        [
            id 1    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
        ]
        router																	# Router 0:2
        [
            id 2    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
        ]
        router																	# Router 1:0
        [
            id 3    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 1:1
        [
            id 4   
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
        ]
        router																	# Router 2:0
        [
            id 5    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 2:1
        [
            id 6    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 2:2
        [
            id 7    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 2:3
        [
            id 8    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 2:4
        [
            id 9    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
        ]
        router																	# Router 2:5
        [
            id 10    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 2:6
        [
            id 11    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 3:0
        [
            id 12    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 3:1
        [
            id 13    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
            interface [id 4 _extends .dict.100Gb]
        ]
        router																	# Router 3:2
        [
            id 14    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 3:3
        [
            id 15    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 4
        [
            id 16    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]
        router																	# Router 5
        [
            id 17    
            _find .dict.routerGraph.graph
            interface [id 0 _extends .dict.100Gb]
            interface [id 1 _extends .dict.100Gb]
            interface [id 2 _extends .dict.100Gb]
            interface [id 3 _extends .dict.100Gb]
        ]

        # links. 

        # 0:0 - 0:1
        link [ attach 0(0) attach 1(0) _extends .dict.link_delay_1us ]
        # 0:0 - 0:2
        link [ attach 0(1) attach 2(0) _extends .dict.link_delay_1us ]
        # 0:0 - 4
        link [ attach 0(2) attach 16(0) _extends .dict.link_delay_1us ]
        # 0:1 - 0:2
        link [ attach 1(1) attach 2(1) _extends .dict.link_delay_1us ]
        # 0:1 - 1:0
        link [ attach 1(2) attach 3(2) _extends .dict.link_delay_1us ]
        # 0:2 - 5
        link [ attach 2(2) attach 17(0) _extends .dict.link_delay_1us ]
        # 1:0 - 1:1
        link [ attach 3(3) attach 4(2) _extends .dict.link_delay_1us ]


        # 2:0 - 4
        link [ attach 5(1) attach 16(1) _extends .dict.link_delay_1us ]
        # 2:0 - 2:1
        link [ attach 5(2) attach 6(1) _extends .dict.link_delay_1us ]
        # 2:0 - 2:2
        link [ attach 5(3) attach 7(1) _extends .dict.link_delay_1us ]
        # 2:1 - 4
        link [ attach 6(2) attach 16(2) _extends .dict.link_delay_1us ]
        # 2:1 - 2:3
        link [ attach 6(3) attach 8(1) _extends .dict.link_delay_1us ]

        # 2:2 - 2:3
        link [ attach 7(2) attach 8(2) _extends .dict.link_delay_1us ]
        # 2:2 - 2:4
        link [ attach 7(3) attach 9(1) _extends .dict.link_delay_1us ]
        # 2:3 - 2:5
        link [ attach 8(3) attach 10(1) _extends .dict.link_delay_1us ]
        # 2:4 - 2:5
        link [ attach 9(2) attach 10(2) _extends .dict.link_delay_1us ]
        # 2:5 - 2:6
        link [ attach 10(3) attach 11(3) _extends .dict.link_delay_1us ]

        # 4 - 5
        link [ attach 16(3) attach 17(1) _extends .dict.link_delay_1us ]

        # 5 - 3:0
        link [ attach 17(2) attach 12(2) _extends .dict.link_delay_1us ]
        # 5 - 3:1
        link [ attach 17(3) attach 13(1) _extends .dict.link_delay_1us ]
        # 3:0 - 3:1
        link [ attach 12(3) attach 13(2) _extends .dict.link_delay_1us ]
        # 3:1 - 3:2
        link [ attach 13(3) attach 14(2) _extends .dict.link_delay_1us ]
        # 3:1 - 3:3
        link [ attach 13(4) attach 15(2) _extends .dict.link_delay_1us ]
        # 3:2 - 3:3
        link [ attach 14(3) attach 15(3) _extends .dict.link_delay_1us ]
    ]

"""

router_num_lan_mapping = {
    0: 0,
    1: 0,
    2: 0,
    3: 2,
    4: 2,
    5: 1,
    6: 1,
    7: 1,
    8: 1,
    9: 1,
    10: 1,
    11: 3,
    12: 2,
    13: 1,
    14: 2,
    15: 2,
    16: 0,
    17: 0
}

lan_router_intf_mapping = {}

lan_emu_netids = {}
lan_simulated_client_nhis = {}
lan_simulated_server_nhis = {}

def fill_lan_router_intf_mapping(num_sim_hosts_per_lan, fraction_servers):
    global lan_router_intf_mapping
    global lan_simulated_client_nhis
    global lan_simulated_server_nhis

    num_sim_tcp_clients_added = max(1, int(num_sim_hosts_per_lan * (1.0 - fraction_servers)))
    num_sim_tcp_servers_added = max(1, int(num_sim_hosts_per_lan * fraction_servers))

    

    last_checked_router = -1
    num_avail_lans = 0
    start_intf_number = 0
    for i in range(0, TOTAL_LANS):
        while num_avail_lans == 0:
            last_checked_router += 1
            num_avail_lans = router_num_lan_mapping[last_checked_router]

            if num_avail_lans > 0:
                start_intf_number = 0
        lan_router_intf_mapping[i] = {
            'router': last_checked_router,
            'intf': start_intf_number
        }

        start_intf_number += 1
        num_avail_lans -= 1

        lan_netid = i + 1
        lan_tcp_client_host_start_id = 1
        lan_tcp_client_host_end_id = num_sim_tcp_clients_added
        lan_tcp_server_host_start_id = num_sim_tcp_clients_added + 1
        lan_tcp_server_host_end_id = num_sim_tcp_clients_added + num_sim_tcp_servers_added

        lan_simulated_client_nhis[i] = (lan_netid, lan_tcp_client_host_start_id, 
            lan_tcp_client_host_end_id)
        lan_simulated_server_nhis[i] = (lan_netid, lan_tcp_server_host_start_id,
            lan_tcp_server_host_end_id)

def get_sim_traffic_pattern():

    pattern_string = ""
    for lan_no in range(0, TOTAL_LANS):
        dest_lan = (lan_no + int(TOTAL_LANS/2)) % (TOTAL_LANS)
        dest_lan_netid, serv_start, server_end = lan_simulated_server_nhis[dest_lan]
        start = f"{dest_lan_netid}:{serv_start}"
        end = f"{dest_lan_netid}:{server_end}"

        if start == end:
            servers = f"""servers [ port 1024 nhi {start}(0) list "forTCP" ]"""
        else:
            servers = f"""servers [ port 1024 nhi_range [from {start}(0) to {end}(0)] list "forTCP" ]"""
        
        src_lan, cli_start, cli_end = lan_simulated_client_nhis[lan_no]
        for cli in range(cli_start, cli_end + 1):
            client = f"client {src_lan}:{cli}"
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



def gen_basic_simulated_lan(num_emu_hosts_per_lan, num_sim_hosts_per_lan, fraction_servers):
    # A simulated lan network containing one main router and some simulated hosts connected to it
    num_sim_tcp_clients_added = max(1, int(num_sim_hosts_per_lan * (1.0 - fraction_servers)))
    num_sim_tcp_servers_added = max(1, int(num_sim_hosts_per_lan * fraction_servers))

    LanSimRouterInterfaces = ""
    numInterfaces = num_emu_hosts_per_lan + num_sim_tcp_clients_added + num_sim_tcp_servers_added + 1
    for i in range (0, numInterfaces):
        LanSimRouterInterfaces += f"""
            interface [id {i} _extends .dict.100Gb]"""
    LanSimRouter = f"""
        router
        [
            id 0
            _find .dict.routerGraph.graph
            {LanSimRouterInterfaces}
        ]
    """
    numEmuHostLinks = num_emu_hosts_per_lan
    numSimHostLinks = num_sim_tcp_clients_added + num_sim_tcp_servers_added
    SimHostLinks = ""
    for host in range(1, numSimHostLinks + 1):
        LanRouterId = 0
        LanRouterIntf = numEmuHostLinks + host # First 0 to numEmuHostLinks is reserved and used later
        SimHostLinks += f"""
        link [ attach {host}(0) attach {LanRouterId}({LanRouterIntf}) _extends .dict.link_delay_1us ]"""
    
    if num_sim_tcp_servers_added > 1:
        SimNetDict = f"""
    basicSimNet [
        {LanSimRouter}
        host 																	# Host 1:0
        [ 
            idrange [from 1 to {num_sim_tcp_clients_added}]
            _extends .dict.TCPClient
        ]
        host 																	# Host 1:0
        [ 
            idrange [from {num_sim_tcp_clients_added + 1} to {num_sim_tcp_clients_added + num_sim_tcp_servers_added }]
            _extends .dict.TCPServer
        ]
        {SimHostLinks}
    ]
        """
    else:
        SimNetDict = f"""
    basicSimNet [
        {LanSimRouter}
        host 																	# Host 1:0
        [ 
            idrange [from 1 to {num_sim_tcp_clients_added}]
            _extends .dict.TCPClient
        ]
        host 																	# Host 1:0
        [ 
            id {num_sim_tcp_clients_added + 1}
            _extends .dict.TCPServer
        ]
        {SimHostLinks}
    ]
        """

    return SimNetDict

def get_emulated_host_cfgs(num_emu_hosts_per_lan):
    global lan_emu_netids
    emu_cfg = ""
    for lan_no in range(0, TOTAL_LANS):
        emu_timeline_id_start = lan_no * num_emu_hosts_per_lan + 1
        lan_emu_netids[lan_no] = []
        for tl in range(emu_timeline_id_start, 
            emu_timeline_id_start + num_emu_hosts_per_lan):
            curr_host_cfg = f"""
    Net 
    [ 
        id {tl + TOTAL_LANS}
        alignment {tl}
        host 
        [ 
            id 0
            _extends .dict.emuHost
        ]
    ]
            """
            emu_cfg += curr_host_cfg
            lan_emu_netids[lan_no].append(tl + TOTAL_LANS)
    return emu_cfg

def get_lxc_cfg_string(params):

    tgenCmdPath = params['cmd']
    ttnProject = params['ttnProject']
    flowType = params['flowType']
    periodUs = params['periodUs']
    muArrivalUs = params['muArrivalUs']
    txSizeKb = params['txSizeKb']
    txRateMbps = params['txRateMbps']
    logDir = params['logDir']
    settings_string = ""

    mixed_cfg = [('periodic', 8), ('poisson', 8), ('rate', 10), ('periodic', 256), ('poisson', 256), ('rate', 100), ('periodic', 2000),  ('poisson', 2000), ('rate', 1000), ('rate', 1)]

    cmd_count = 0
    for lan_no in range(0, int(TOTAL_LANS/2)):
        dest_lan = (lan_no + int(TOTAL_LANS / 2))

        for idx, cli_netid in enumerate(lan_emu_netids[lan_no]):
            dependantTl = lan_emu_netids[dest_lan][idx] - TOTAL_LANS
            server_netid = lan_emu_netids[dest_lan][idx]
            if flowType == 'periodic':
                cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 periodic {periodUs} {txSizeKb} > {logDir}/client{cli_netid}.log"
            elif flowType == 'poisson':
                cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 poisson {muArrivalUs} {txSizeKb} > {logDir}/client{cli_netid}.log"
            elif flowType == 'rate':
                cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 rate {txRateMbps} > {logDir}/client{cli_netid}.log"
            else:
                # Mixed
                cmd, param = mixed_cfg[cmd_count % len(mixed_cfg)]
                if cmd == 'periodic':
                    cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 periodic {periodUs} {param} > {logDir}/client{cli_netid}.log"
                elif cmd == 'poisson':
                    cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 poisson {muArrivalUs} {param} > {logDir}/client{cli_netid}.log"
                else:
                    cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 rate {param} > {logDir}/client{cli_netid}.log"


                #if cmd_count % 3 == 1:
                #    cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 periodic {periodUs} {txSizeKb} > {logDir}/client{cli_netid}.log"
                #elif cmd_count % 3 == 2:
                #    cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 poisson {muArrivalUs} {txSizeKb} > {logDir}/client{cli_netid}.log"
                #else:
                #    cliCmd = f"{tgenCmdPath} client {cli_netid} {server_netid}:0 7891 rate {txRateMbps} > {logDir}/client{cli_netid}.log"

                cmd_count += 1
            cli_settings = f"""
        settings [ lxcNHI {cli_netid}:0 ttnProject "{ttnProject}" dependants "{dependantTl}" cmd "{cliCmd}" ]"""
            settings_string += cli_settings

        for idx, server_netid in enumerate(lan_emu_netids[dest_lan]):
            dependantTl = lan_emu_netids[lan_no][idx] - TOTAL_LANS
            serverCmd = f"{tgenCmdPath} server {server_netid} {server_netid}:0 7891 > {logDir}/server{server_netid}.log"
            server_settings = f"""
        settings [ lxcNHI {server_netid}:0 ttnProject "{ttnProject}" dependants "{dependantTl}" cmd "{serverCmd}" ]"""
            settings_string += server_settings

    lxc_config_string = f"""
    lxcConfig
	[
        {settings_string}
    ]
    """
    return lxc_config_string




def get_emu_host_links(num_emu_hosts_per_lan):
    # Connect each emulated host in lan to corresponding main lan sim router
    EmuHostLinks = ""

    for lan_no in range(0, TOTAL_LANS):
        lan_sim_netid = lan_no + 1

        emu_host_netid_start = lan_no * num_emu_hosts_per_lan + 1 + TOTAL_LANS
        
        Intf = 1
        for host in range(emu_host_netid_start, emu_host_netid_start + num_emu_hosts_per_lan):
            EmuHostLinks += f"""
    link [ attach {host}:0(0) attach {lan_sim_netid}:0({Intf}) _extends .dict.link_delay_1us ]"""
            Intf += 1
    return EmuHostLinks

def get_lan_backbone_links():
    # Connect each lan sim router to backbone network
    LanBackBoneLinks = ""
    back_bone_netid = 0

    for lan_no in range(0, TOTAL_LANS):
        lan_sim_netid = lan_no + 1
        lan_sim_router_id = 0
        mapped_router_id = lan_router_intf_mapping[lan_no]['router']
        mapped_router_intf = lan_router_intf_mapping[lan_no]['intf']

        LanBackBoneLinks += f"""
    link  [ attach {lan_sim_netid}:{lan_sim_router_id}(0) attach {back_bone_netid}:{mapped_router_id}({mapped_router_intf}) _extends .dict.link_delay_1us ]"""

    return LanBackBoneLinks
        


def compose_all_sim_nets():
    sim_net_string = ""
    for lan_no in range(0, TOTAL_LANS):
        curr_sim_net = f"""
    Net [
        id {lan_no + 1}
        alignment 0
        _extends .sim.basicSimNet
    ]
        """
        sim_net_string += curr_sim_net
    return sim_net_string


# There will be 20 lans - fixed
def main():
    args = parser.parse_args()

    num_sim_hosts_per_lan = args.num_sim_hosts_per_lan
    num_emu_hosts_per_lan = args.num_emu_hosts_per_lan

    print (f"Generating for LA-Enabled: {args.enable_lookahead}, Num Emu Hosts Per Lan: {args.num_emu_hosts_per_lan} ")
    print (f"Flow Type: {args.emu_flow_type}, Flow-Period: {args.emu_flow_period_us}, Flow-Mu-Arrival: {args.emu_flow_mean_arrival_us}, Flow-TxSize: {args.transfer_size_kb}, Flow-Rate: {args.transfer_rate_mbps}")

    from os.path import expanduser
    home = expanduser("~")

    total_num_timelines = num_emu_hosts_per_lan * TOTAL_LANS + 1

    if args.enable_lookahead:
        lookahead_status = "LA_Enabled"
    else:
        lookahead_status = "LA_Disabled"

    if total_num_timelines > 1:
        if args.emu_flow_type == 'periodic':
            log_dir = f"TCP_{lookahead_status}_nemus_{total_num_timelines - 1}_periodic_period_{args.emu_flow_period_us}_txsize_{args.transfer_size_kb}"
        elif args.emu_flow_type == 'poisson':
            log_dir = f"TCP_{lookahead_status}_nemus_{total_num_timelines - 1}_poisson_mu_{args.emu_flow_mean_arrival_us}_txsize_{args.transfer_size_kb}"
        elif args.emu_flow_type == 'rate':
            log_dir = f"TCP_{lookahead_status}_nemus_{total_num_timelines - 1}_ratelim_rate_{args.transfer_rate_mbps}"
        else:
            #log_dir = f"TCP_{lookahead_status}_nemus_{total_num_timelines - 1}_mixed_period_{args.emu_flow_period_us}_mu_{args.emu_flow_mean_arrival_us}_txsize_{args.transfer_size_kb}_rate_{args.transfer_rate_mbps}"
            log_dir = f"TCP_{lookahead_status}_nemus_{total_num_timelines - 1}_mixed"
    else:
        log_dir = "TCP_FullSim"


    tgenCmd = f"{home}/VT-S3FNet/csudp/tcp_tgen/tgen"
    logDirPath = f"{home}/VT-S3FNet/experiment-data"
    params = {
        'cmd': tgenCmd,
        'ttnProject': 'tcp_tgen',
        'flowType': args.emu_flow_type,
        'periodUs': args.emu_flow_period_us,
        'muArrivalUs': args.emu_flow_mean_arrival_us,
        'txSizeKb': args.transfer_size_kb,
        'txRateMbps': args.transfer_rate_mbps,
        'logDir': f"{logDirPath}/{log_dir}"
    }

    fill_lan_router_intf_mapping(num_sim_hosts_per_lan, args.fraction_servers)
    emu_host_cfg = get_emulated_host_cfgs(num_emu_hosts_per_lan)
    basic_sim_lan = gen_basic_simulated_lan(num_emu_hosts_per_lan,
        num_sim_hosts_per_lan, args.fraction_servers)
    
    basic_sim_lan_dict = f"""
sim [
    {basic_sim_lan}
]
    """
    with open('sim.dml', 'w') as f:
        f.write(basic_sim_lan_dict)

    
    if total_num_timelines > 1:
        overall_cfg = f"""
total_timeline {total_num_timelines}	
tick_per_second 6	
run_time {args.run_time + 0.1}
seed 1	
log_dir "{log_dir}"		
virtual_time_manager "TITAN"
eat_update_period_us 1000
enable_lookahead {args.enable_lookahead}

Net [

    # LXC Config settings
{get_lxc_cfg_string(params)}

    # Simulated TCP Traffic Pattern
{get_sim_traffic_pattern()}

    # Backbone Network with links
{backbone_network}

    # Composed Sim Nets
{compose_all_sim_nets()}

    # Composed Emulated Hosts
{emu_host_cfg}

    # Links between sim lan router and backbone network
{get_lan_backbone_links()}

    # Links between emu hosts and lan router
{get_emu_host_links(num_emu_hosts_per_lan)}

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
eat_update_period_us 1000
enable_lookahead {args.enable_lookahead}

Net [

    # Simulated TCP Traffic Pattern
{get_sim_traffic_pattern()}

    # Backbone Network with links
{backbone_network}

    # Composed Sim Nets
{compose_all_sim_nets()}

    # Links between sim lan router and backbone network
{get_lan_backbone_links()}

]
    """


    with open('test.dml', 'w') as f:
        f.write(overall_cfg)
    
if __name__ == "__main__":
    main()





