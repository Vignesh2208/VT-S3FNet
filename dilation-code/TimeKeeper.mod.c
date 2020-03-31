#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0x2afcd313, __VMLINUX_SYMBOL_STR(module_layout) },
	{ 0x5b36efdb, __VMLINUX_SYMBOL_STR(kmalloc_caches) },
	{ 0xb954402e, __VMLINUX_SYMBOL_STR(call_usermodehelper_exec) },
	{ 0x76ebea8, __VMLINUX_SYMBOL_STR(pv_lock_ops) },
	{ 0xd0d8621b, __VMLINUX_SYMBOL_STR(strlen) },
	{ 0xc8b57c27, __VMLINUX_SYMBOL_STR(autoremove_wake_function) },
	{ 0x2d37342e, __VMLINUX_SYMBOL_STR(cpu_online_mask) },
	{ 0xddd1554e, __VMLINUX_SYMBOL_STR(find_vpid) },
	{ 0x81e4d30c, __VMLINUX_SYMBOL_STR(hrtimer_cancel) },
	{ 0xb43a3177, __VMLINUX_SYMBOL_STR(remove_proc_entry) },
	{ 0x5b19634d, __VMLINUX_SYMBOL_STR(div_s64_rem) },
	{ 0x2230eee2, __VMLINUX_SYMBOL_STR(mutex_unlock) },
	{ 0xc78dda18, __VMLINUX_SYMBOL_STR(kthread_create_on_node) },
	{ 0xa8d39666, __VMLINUX_SYMBOL_STR(proc_mkdir) },
	{ 0x55e92ce1, __VMLINUX_SYMBOL_STR(current_task) },
	{ 0xd8c398c8, __VMLINUX_SYMBOL_STR(__mutex_init) },
	{ 0x50eedeb8, __VMLINUX_SYMBOL_STR(printk) },
	{ 0x66504571, __VMLINUX_SYMBOL_STR(kthread_stop) },
	{ 0x110038fe, __VMLINUX_SYMBOL_STR(netlink_kernel_release) },
	{ 0xb6ed1e53, __VMLINUX_SYMBOL_STR(strncpy) },
	{ 0xb4390f9a, __VMLINUX_SYMBOL_STR(mcount) },
	{ 0x7fbffc20, __VMLINUX_SYMBOL_STR(mutex_lock) },
	{ 0x396d0d21, __VMLINUX_SYMBOL_STR(netlink_unicast) },
	{ 0xceb78c3b, __VMLINUX_SYMBOL_STR(pid_task) },
	{ 0x5da5d401, __VMLINUX_SYMBOL_STR(init_net) },
	{ 0x8ff4079b, __VMLINUX_SYMBOL_STR(pv_irq_ops) },
	{ 0xc9cdc48, __VMLINUX_SYMBOL_STR(__alloc_skb) },
	{ 0xf0fdf6cb, __VMLINUX_SYMBOL_STR(__stack_chk_fail) },
	{ 0x4292364c, __VMLINUX_SYMBOL_STR(schedule) },
	{ 0xbdb257ba, __VMLINUX_SYMBOL_STR(hrtimer_start) },
	{ 0x73281734, __VMLINUX_SYMBOL_STR(pv_cpu_ops) },
	{ 0xd35ea988, __VMLINUX_SYMBOL_STR(wake_up_process) },
	{ 0xb82271ae, __VMLINUX_SYMBOL_STR(kmem_cache_alloc_trace) },
	{ 0x67f7403e, __VMLINUX_SYMBOL_STR(_raw_spin_lock) },
	{ 0xe1a9650c, __VMLINUX_SYMBOL_STR(sched_setscheduler) },
	{ 0xe45f60d8, __VMLINUX_SYMBOL_STR(__wake_up) },
	{ 0x80337f11, __VMLINUX_SYMBOL_STR(call_usermodehelper_setup) },
	{ 0xb3f7646e, __VMLINUX_SYMBOL_STR(kthread_should_stop) },
	{ 0xc3c4ce10, __VMLINUX_SYMBOL_STR(proc_create_data) },
	{ 0x4f68e5c9, __VMLINUX_SYMBOL_STR(do_gettimeofday) },
	{ 0xe04c4853, __VMLINUX_SYMBOL_STR(__netlink_kernel_create) },
	{ 0x37a0cba, __VMLINUX_SYMBOL_STR(kfree) },
	{ 0x622fa02a, __VMLINUX_SYMBOL_STR(prepare_to_wait) },
	{ 0x3e3cedcc, __VMLINUX_SYMBOL_STR(send_sig_info) },
	{ 0x781c6eca, __VMLINUX_SYMBOL_STR(hrtimer_init) },
	{ 0x74c134b9, __VMLINUX_SYMBOL_STR(__sw_hweight32) },
	{ 0x75bb675a, __VMLINUX_SYMBOL_STR(finish_wait) },
	{ 0x362ef408, __VMLINUX_SYMBOL_STR(_copy_from_user) },
	{ 0xfcece2c4, __VMLINUX_SYMBOL_STR(__nlmsg_put) },
	{ 0x268cc6a2, __VMLINUX_SYMBOL_STR(sys_close) },
	{ 0x4cdb3178, __VMLINUX_SYMBOL_STR(ns_to_timeval) },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=";


MODULE_INFO(srcversion, "10CC5724473F1CE0415F15D");
