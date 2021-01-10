import sys
import os
import time
import vt_functions as kf
import sys
import argparse
import json
import shutil



script_dir = os.path.dirname(os.path.realpath(__file__))

EXP_CBE = 1
VIRTUAL = 1

cmds_to_run = {
    "bzip2_c1": f"{script_dir}/401.bzip2/bzip2 {script_dir}/401.bzip2/test/input/dryer.jpg 2",
    "bzip2_c2": f"{script_dir}/401.bzip2/bzip2 {script_dir}/401.bzip2/test/input/dryer.jpg 3",
    "bzip2_c3": f"{script_dir}/401.bzip2/bzip2 {script_dir}/401.bzip2/test/input/dryer.jpg 4",
    "sjeng_c1": f"{script_dir}/458.sjeng/sjeng {script_dir}/458.sjeng/ref_c1.txt",
    "sjeng_c2": f"{script_dir}/458.sjeng/sjeng {script_dir}/458.sjeng/ref_c2.txt",
    "sjeng_c3": f"{script_dir}/458.sjeng/sjeng {script_dir}/458.sjeng/ref_c3.txt",
    "h264ref_c1": f"{script_dir}/464.h264ref/h264ref -d {script_dir}/464.h264ref/h264ref_c1.cfg",
    "h264ref_c2": f"{script_dir}/464.h264ref/h264ref -d {script_dir}/464.h264ref/h264ref_c2.cfg",
    "h264ref_c3": f"{script_dir}/464.h264ref/h264ref -d {script_dir}/464.h264ref/h264ref_c3.cfg",
    #"sysbench_c1": "/usr/local/bin/sysbench --test=cpu --cpu-max-prime=5000 run",
    #"sysbench_c2": "/usr/local/bin/sysbench --test=cpu --cpu-max-prime=7000 run",
    #"sysbench_c3": "/usr/local/bin/sysbench --test=cpu --cpu-max-prime=10000 run",
    "sysbench_c1": "/usr/local/bin/sysbench --max-requests=1 --test=cpu --cpu-max-prime=1000000 run",
    "sysbench_c2": "/usr/local/bin/sysbench --max-requests=1 --test=cpu --cpu-max-prime=2000000 run",
    "sysbench_c3": "/usr/local/bin/sysbench --max-requests=1 --test=cpu --cpu-max-prime=3000000 run",
    "mmultiply_c1": f"{script_dir}/mmultiply/mmultiply",
    "mmultiply_c2": f"{script_dir}/mmultiply/mmultiply",
    "mmultiply_c3": f"{script_dir}/mmultiply/mmultiply"
}

normal_cmds_to_run = {
    "bzip2_c1": f"{script_dir}/401.bzip2/bzip2_gcc {script_dir}/401.bzip2/test/input/dryer.jpg 2",
    "bzip2_c2": f"{script_dir}/401.bzip2/bzip2_gcc {script_dir}/401.bzip2/test/input/dryer.jpg 3",
    "bzip2_c3": f"{script_dir}/401.bzip2/bzip2_gcc {script_dir}/401.bzip2/test/input/dryer.jpg 4",
    "sjeng_c1": f"{script_dir}/458.sjeng/sjeng_gcc {script_dir}/458.sjeng/ref_c1.txt",
    "sjeng_c2": f"{script_dir}/458.sjeng/sjeng_gcc {script_dir}/458.sjeng/ref_c2.txt",
    "sjeng_c3": f"{script_dir}/458.sjeng/sjeng_gcc {script_dir}/458.sjeng/ref_c3.txt",
    "h264ref_c1": f"{script_dir}/464.h264ref/h264ref_gcc -d {script_dir}/464.h264ref/h264ref_c1.cfg",
    "h264ref_c2": f"{script_dir}/464.h264ref/h264ref_gcc -d {script_dir}/464.h264ref/h264ref_c2.cfg",
    "h264ref_c3": f"{script_dir}/464.h264ref/h264ref_gcc -d {script_dir}/464.h264ref/h264ref_c3.cfg",
    #"sysbench_c1": "/usr/local/bin/sysbench --test=cpu --cpu-max-prime=5000 run",
    #"sysbench_c2": "/usr/local/bin/sysbench --test=cpu --cpu-max-prime=7000 run",
    #"sysbench_c3": "/usr/local/bin/sysbench --test=cpu --cpu-max-prime=10000 run",
    "sysbench_c1": "/usr/local/bin/sysbench --max-requests=1 --test=cpu --cpu-max-prime=1000000 run",
    "sysbench_c2": "/usr/local/bin/sysbench --max-requests=1 --test=cpu --cpu-max-prime=2000000 run",
    "sysbench_c3": "/usr/local/bin/sysbench --max-requests=1 --test=cpu --cpu-max-prime=3000000 run",
    "mmultiply_c1": f"{script_dir}/mmultiply/mmultiply_gcc",
    "mmultiply_c2": f"{script_dir}/mmultiply/mmultiply_gcc",
    "mmultiply_c3": f"{script_dir}/mmultiply/mmultiply_gcc"
}

def start_process(cmd_to_run, log_file_fd, exp_type, project):
    
    newpid = os.fork()
    if newpid == 0:
        os.dup2(log_file_fd, sys.stdout.fileno())
        os.dup2(log_file_fd, sys.stderr.fileno())

        if exp_type == VIRTUAL:
            args = ["ttn_tracer", "-t", str(0), "-i", str(1),
                    "-c", cmd_to_run, "-e", str(EXP_CBE), "-p", project]
            os.execvp(args[0], args)
        else:
            args = cmd_to_run.split(' ')
            os.execvp(args[0], args)
    else:
        return newpid

def run_experiment(cmd_to_run, iter_no):    
    log_fd = os.open(f"/tmp/normal_{cmd_to_run}/{cmd_to_run}_log_{iter_no}.txt", os.O_RDWR | os.O_CREAT )
    start_time = float(time.time())
    project = cmd_to_run.split('_')[0]
    print (f"Cmd project = {project}")
    pid = start_process(normal_cmds_to_run[cmd_to_run], log_fd, 0, project)
    pid, status = os.waitpid(pid, 0)
    elapsed_time = float(time.time()) - start_time

    time_taken = {
        "elapsed_time": elapsed_time,
        "cmd": normal_cmds_to_run[cmd_to_run]
    }
    with open(f"/tmp/normal_{cmd_to_run}/overhead_{iter_no}.json", "w") as f:
        json.dump(time_taken, f)

    print ("Finished executing process. Wait returned, pid = %d, status = %d" % (pid, status))
    os.close(log_fd)

def run_vt_experiment(cmd_to_run, timeslice_ns, num_rounds, iter_no):

    if num_rounds * timeslice_ns <= 0 :
        return

    log_fd = os.open(f"/tmp/vt_{cmd_to_run}_ts{timeslice_ns}/{cmd_to_run}_log_{iter_no}.txt", os.O_RDWR | os.O_CREAT )
    print ("Running iteration number: ", iter_no)

    print ("Initializing VT Module !")   
    if kf.InitializeVtExp(EXP_CBE, 1, 1) < 0 :
        print ("VT module initialization failed ! Make sure you are running\
               the dilated kernel and kronos module is loaded !")
        sys.exit(0)

    project = cmd_to_run.split('_')[0]
    print (f"Cmd project = {project}")
    print ("Starting all commands to run !")
    start_process(cmds_to_run[cmd_to_run], log_fd, VIRTUAL, project)
    
    
    print ("Synchronizing anf freezing tracers ...")
    while kf.SynchronizeAndFreeze() <= 0:
        print ("VT Module >> Synchronize and Freeze failed. Retrying in 1 sec")
        time.sleep(1)


    print ("Starting Synchronized Experiment !")
    start_time = float(time.time())
    if num_rounds > 0 :
        print ("Running for %d rounds ... " %(num_rounds))
        kf.ProgressBy(timeslice_ns, num_rounds)
    elapsed_time = float(time.time()) - start_time
    print ("Total time elapsed (secs) = ", elapsed_time)

    time_taken = {
        "elapsed_time": elapsed_time,
        "cmd": cmds_to_run[cmd_to_run],
        "overhead_ratio": elapsed_time/float(timeslice_ns * num_rounds)
    }
    with open(f"/tmp/vt_{cmd_to_run}_ts{timeslice_ns}/overhead_{iter_no}.json", "w") as f:
        json.dump(time_taken, f)
    print ("Stopping Synchronized Experiment !")
    kf.StopExp()
    os.close(log_fd)


def main():

    
    parser = argparse.ArgumentParser()


    parser.add_argument('--cmd_to_run', dest='cmd_to_run',
                        help='cmd to run: sysbench, bzip2, sjeng, h264ref, mmultiply or all', \
                        type=str, default='bzip2')

    parser.add_argument('--cfg', dest='cfg',
                        help='command config: c1, c2 or c3', \
                        type=str, default='c1')


    parser.add_argument('--timeslice_ns', dest='timeslice_ns',
                        help='Number of insns per round', type=int,
                        default=1000000)

    parser.add_argument('--num_secs', dest='num_secs',
                        help='Number of rounds to run', type=int,
                        default=100)

    parser.add_argument('--num_exp_iterations', dest='num_exp_iterations',
                        help='Number of experiment iterations', type=int,
                        default=1)

    parser.add_argument('--exp_type', dest='exp_type',
        help='0 - Normal, 1 - Virtual-Time Control', type=int, default=1)

    

    args = parser.parse_args()
    cfg = args.cfg
    assert (cfg in ['c1', 'c2', 'c3'])
    assert (args.cmd_to_run in ['bzip2', 'sjeng', 'h264ref', 'sysbench', 'mmultiply', 'all'])
 
    num_progress_rounds = int(args.num_secs * 1000000000 / args.timeslice_ns)
    timeslice_ns = args.timeslice_ns
    if args.cmd_to_run == 'all':
        cmds_to_run = ['sysbench', 'bzip2', 'sjeng', 'h264ref', 'mmultiply']
    else:
        cmds_to_run = [args.cmd_to_run]
    for cmd in cmds_to_run:
        cmd_to_run = f"{cmd}_{cfg}"
        
        if args.exp_type == VIRTUAL:
            if os.path.exists(f"/tmp/vt_{cmd_to_run}_ts{timeslice_ns}"):
                shutil.rmtree(f"/tmp/vt_{cmd_to_run}_ts{timeslice_ns}")
            if not os.path.exists(f"/tmp/vt_{cmd_to_run}_ts{timeslice_ns}"):
                os.mkdir(f"/tmp/vt_{cmd_to_run}_ts{timeslice_ns}")
        else:
            if os.path.exists(f"/tmp/normal_{cmd_to_run}"):
                shutil.rmtree(f"/tmp/normal_{cmd_to_run}")
            if not os.path.exists(f"/tmp/normal_{cmd_to_run}"):
                os.mkdir(f"/tmp/normal_{cmd_to_run}")
        for i in range(0, args.num_exp_iterations):
            if args.exp_type == VIRTUAL:
                run_vt_experiment(cmd_to_run, timeslice_ns, num_progress_rounds, i + 1)
            else:
                run_experiment(cmd_to_run, i + 1)
    os.system("sudo chmod -R 777 /tmp/*")
            

if __name__ == "__main__":
	main()
