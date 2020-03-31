#include "dilation_module.h"
#include "scripts/TimeKeeper_definitions.h"

/*
Has basic functionality for the Kernel Module itself. It defines how the userland process communicates with the kernel module,
as well as what should happen when the kernel module is initialized and removed.
*/

extern asmlinkage long (*ref_sys_sleep)(struct timespec __user *rqtp, struct timespec __user *rmtp);


extern int proc_num; // number of LXCs in the experiment
extern struct mutex exp_mutex; // experiment mutex to prevent race conditions
extern struct task_struct *catchup_task; // the main synchronization kernel thread for CBE experiments
extern struct dilation_task_struct *leader_task; // the leader task of the experiment
extern int experiment_stopped; // flag to determine state of the experiment
extern struct list_head exp_list; // linked list of all tasks in the experiment
extern s64 chainlength[EXP_CPUS]; // maintains the runtime of each CPU within a round

extern struct timeline* timelineHead[EXP_CPUS]; // an array of timelines (for S3F (CS))

//for CS, per CPU synchronization variables
extern spinlock_t cpuLock[EXP_CPUS];
extern int cpuIdle[EXP_CPUS];
extern struct list_head cpuWorkList[EXP_CPUS];

// Proc file declarations
static struct proc_dir_entry *dilation_dir;
static struct proc_dir_entry *dilation_file;

unsigned long **sys_call_table; //address of the sys_call_table, so we can hijack certain system calls

int TOTAL_CPUS; //number of CPUs in the system

unsigned long original_cr0; //The register to hijack sys_call_table

extern struct sock *nl_sk; //the socket to send data from kernel to userspace

extern struct task_struct *loop_task; //task that loops endlessly (64-bit)
/*
Gets the PID of our spinner task (only in 64 bit)
*/
int getSpinnerPid(struct subprocess_info *info, struct cred *new) {
        loop_task = current;
        return 0;
}

/*
Hack to get 64 bit running correctly. Starts a process that will just loop while the experiment is going
on. Starts an executable specified in the path in user space from kernel space.
*/
int call_usermodehelper_dil(char *path, char **argv, char **envp, int wait)
{
	struct subprocess_info *info;
        gfp_t gfp_mask = (wait == UMH_NO_WAIT) ? GFP_ATOMIC : GFP_KERNEL;

        info = call_usermodehelper_setup(path, argv, envp, gfp_mask, getSpinnerPid, NULL, NULL);
        if (info == NULL)
                return -ENOMEM;

        return call_usermodehelper_exec(info, wait);
}

/***
This handles how a process from userland communicates with the kernel module. The process basically writes to:
/proc/dilation/status with a command ie, 'W', which will tell the kernel module to call the sec_clean_exp() function
***/
ssize_t status_write(struct file *file, const char __user *buffer, size_t count, loff_t *data)
{
	char write_buffer[STATUS_MAXSIZE];
	unsigned long buffer_size;

 	if(count > STATUS_MAXSIZE)
	{
    		buffer_size = STATUS_MAXSIZE;
  	}
	else
	{
		buffer_size = count;
	}

  	if(copy_from_user(write_buffer, buffer, buffer_size))
	{
	    return -EFAULT;
	}

	// Use +2 to skip over the first two characters (i.e. the switch and the ,)
	if (write_buffer[0] == FREEZE_OR_UNFREEZE)
                yield_proc(write_buffer+2);
	else if (write_buffer[0] == FREEZE_OR_UNFREEZE_ALL)
		yield_proc_recurse(write_buffer+2);
	else if (write_buffer[0] == DILATE)
		dilate_proc(write_buffer+2);
	else if (write_buffer[0] == DILATE_ALL)
		dilate_proc_recurse(write_buffer+2);
	else if (write_buffer[0] == ADD_TO_EXP_CBE)
		add_to_exp_proc(write_buffer+2);
	else if (write_buffer[0] == STOP_EXP)
                set_clean_exp();
	else if (write_buffer[0] == LEAP)
                leap_proc(write_buffer+2);
	else if (write_buffer[0] == START_EXP)
		core_sync_exp();
	else if (write_buffer[0] == PROGRESS)
		s3f_progress_timeline(write_buffer+2);
	else if (write_buffer[0] == ADD_TO_EXP_CS)
		s3f_add_to_exp_proc(write_buffer+2);
	else if (write_buffer[0] == RESET)
		s3f_reset(write_buffer+2);
	else if (write_buffer[0] == SET_INTERVAL)
		s3f_set_interval(write_buffer+2);
	else if (write_buffer[0] == SYNC_AND_FREEZE)
		sync_and_freeze();
	else if (write_buffer[0] == FIX_TIMELINE)
		fix_timeline_proc(write_buffer+2);
	else if (write_buffer[0] == DEBUG_PROC_INFO)
		print_proc_info(write_buffer+2);
	else if (write_buffer[0] == DEBUG_SEND_MESSAGE)
		send_a_message_proc(write_buffer+2);
	else if (write_buffer[0] == DEBUG_CHILDREN_INFO)
		print_children_info_proc(write_buffer+2);
	else if (write_buffer[0] == DEBUG_THREAD_INFO)
		print_threads_proc(write_buffer+2);
        else if (write_buffer[0] == DEBUG_PROGRESS_EXP)
                progress_exp();
	else
		printk(KERN_ALERT "Invalid Write Command: %s\n", write_buffer);
	return count;
}

/***
This function gets executed when the kernel module is loaded. It creates the file for process -> kernel module communication,
sets up mutexes, timers, and hooks the system call table.
***/
int __init my_module_init(void)
{
	int i;

   	printk(KERN_INFO "TimeKeeper: Loading TimeKeeper MODULE\n");

	//Set up TimeKeeper status file in /proc
  	dilation_dir = proc_mkdir(DILATION_DIR, NULL);
  	if(dilation_dir == NULL)
	{
	    	remove_proc_entry(DILATION_DIR, NULL);
   		printk(KERN_INFO "TimeKeeper: Error: Could not initialize /proc/%s\n", DILATION_DIR);
   		return -ENOMEM;
  	}
  	printk(KERN_INFO "TimeKeeper: /proc/%s created\n", DILATION_DIR);
	dilation_file = proc_create(DILATION_FILE, 0660, dilation_dir,&proc_file_fops);
	if(dilation_file == NULL)
	{
	    	remove_proc_entry(DILATION_FILE, dilation_dir);
   		printk(KERN_ALERT "Error: Could not initialize /proc/%s/%s\n", DILATION_DIR, DILATION_FILE);
   		return -ENOMEM;
  	}
	printk(KERN_INFO "TimeKeeper: /proc/%s/%s created\n", DILATION_DIR, DILATION_FILE);

	//If it is 64-bit, initialize the looping script // *** What is this ?
	#ifdef __x86_64
		char *argv[] = { "/bin/x64_synchronizer", NULL };
	        static char *envp[] = {
        	"HOME=/",
	        "TERM=linux",
        	"PATH=/sbin:/bin:/usr/sbin:/usr/bin", NULL };
	        call_usermodehelper_dil( argv[0], argv, envp, UMH_NO_WAIT );
	#endif

	//Set up socket so Kernel can send message to userspace
	struct netlink_kernel_cfg cfg = { .input = send_a_message, };
	nl_sk = netlink_kernel_create(&init_net, NETLINK_USER, &cfg);
    	if (!nl_sk)
    	{
        	printk(KERN_ALERT "Error creating socket.\n");
        	return -10;
    	}

	//Acquire number of CPUs on system
	TOTAL_CPUS = num_online_cpus();
	printk(KERN_INFO "TimeKeeper: Number of CPUS: %d\n", num_online_cpus());

	if (EXP_CPUS > TOTAL_CPUS) {
		printk(KERN_INFO "TimeKeeper: WARNING -- EXP_CPUS LARGER THAN TOTAL_CPUS! FIX IN dilation_module.h\n");
	}

	//Initialize experiment specific variables
	for (i =0; i<EXP_CPUS; i++) {
		timelineHead[i] = NULL;
		chainlength[i] = 0;
		cpuIdle[i] = 0;
		spin_lock_init(&cpuLock[i]);
		INIT_LIST_HEAD(&cpuWorkList[i]);
	}
	leader_task = NULL;
	experiment_stopped = NOTRUNNING;
	proc_num = 0;
	INIT_LIST_HEAD(&exp_list);
	mutex_init(&exp_mutex);
	catchup_task = kthread_run(&catchup_func, NULL, "catchup_task");


	//Acquire sys_call_table, hook system calls
        if(!(sys_call_table = aquire_sys_call_table()))
                return -1;
	original_cr0 = read_cr0();
	write_cr0(original_cr0 & ~0x00010000);
	ref_sys_sleep = (void *)sys_call_table[__NR_nanosleep];
        sys_call_table[__NR_nanosleep] = (unsigned long *)sys_sleep_new;
	write_cr0(original_cr0);

	//Wait to stop loop_task
	#ifdef __x86_64
        	if (loop_task != NULL)
                	kill(loop_task, SIGSTOP, NULL);
        	else
                	printk(KERN_INFO "TimeKeeper: Loop_task is null??\n");
	#endif

  	return 0;
}

/***
This function gets called when the kernel module is unloaded. It frees up all memory, deletes timers, and fixes
the system call table.
***/
void __exit my_module_exit(void)
{
	int i;

	set_clean_exp();
	netlink_kernel_release(nl_sk);

	remove_proc_entry(DILATION_FILE, dilation_dir);
   	printk(KERN_INFO "TimeKeeper: /proc/%s/%s deleted\n", DILATION_DIR, DILATION_FILE);
   	remove_proc_entry(DILATION_DIR, NULL);
   	printk(KERN_INFO "TimeKeeper: /proc/%s deleted\n", DILATION_DIR);


	//Fix sys_call_table
        if(!sys_call_table)
                return;
	write_cr0(original_cr0 & ~0x00010000);
        sys_call_table[__NR_nanosleep] = (unsigned long *)ref_sys_sleep;
	write_cr0(original_cr0);

	//busy wait briefly for tasks to finish
	for (i = 0; i < 1000000000; i++) {}

	if ( kthread_stop(catchup_task) )
        {
                printk(KERN_INFO "TimeKeeper: Stopping catchup_task error\n");
        }

	//Kill the looping task
	#ifdef __x86_64
		if (loop_task != NULL)
			kill(loop_task, SIGKILL, NULL);
	#endif
   		printk(KERN_INFO "TimeKeeper: MP2 MODULE UNLOADED\n");
}

//needs to be defined, but we do not read from /proc/dilation/status so we do not do anything here
ssize_t status_read(struct file *pfil, char __user *pBuf, size_t len, loff_t *p_off)
{
        return 0;
}

// Register the init and exit functions here so insmod can run them
module_init(my_module_init);
module_exit(my_module_exit);

// Required by kernel
MODULE_LICENSE("GPL");
