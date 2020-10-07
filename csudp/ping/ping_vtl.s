	.text
	.file	"ping.c"
	.globl	checksum                # -- Begin function checksum
	.p2align	4, 0x90
	.type	checksum,@function
checksum:                               # @checksum
	.cfi_startproc
# %bb.0:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$17, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$12, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$1, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	pushq	%rax
	.cfi_def_cfa_offset 64
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movl	%esi, %r15d
	movq	%rdi, %r14
	callq	insCacheCallback
	xorl	%r13d, %r13d
	cmpl	$2, %r15d
	jl	.LBB0_4
# %bb.1:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$16, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$10, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currLoopID@GOTPCREL(%rip), %rcx
	movq	$1, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movq	%r14, %rbx
	leal	-2(%r15), %r12d
	andl	$-2, %r12d
	addq	%r12, %r14
	addq	$2, %r14
	movl	%r15d, %edi
	movl	$1, %esi
	movl	$-2, %edx
	callq	SetLoopLookahead
	xorl	%r13d, %r13d
	movl	%r15d, %ebp
	.p2align	4, 0x90
.LBB0_2:                                # =>This Inner Loop Header: Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$13, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$8, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$2, %esi
	movq	%rbx, %rdi
	callq	dataReadCacheCallback
	movzwl	(%rbx), %eax
	addq	$2, %rbx
	addl	%eax, %r13d
	addl	$-2, %ebp
	cmpl	$1, %ebp
	jg	.LBB0_2
# %bb.3:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$5, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$4, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	subl	%r12d, %r15d
	addl	$-2, %r15d
.LBB0_4:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$5, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	cmpl	$1, %r15d
	jne	.LBB0_6
# %bb.5:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$6, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$4, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$6, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$1, %esi
	movq	%r14, %rdi
	callq	dataReadCacheCallback
	movzbl	(%r14), %eax
	addl	%eax, %r13d
.LBB0_6:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$24, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$17, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$7, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	%r13d, %eax
	shrl	$16, %eax
	movzwl	%r13w, %ecx
	addl	%eax, %ecx
	movl	%ecx, %eax
	shrl	$16, %eax
	addl	%ecx, %eax
	notl	%eax
                                        # kill: def $ax killed $ax killed $eax
	addq	$8, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	checksum, .Lfunc_end0-checksum
	.cfi_endproc
                                        # -- End function
	.section	.rodata.cst8,"aM",@progbits,8
	.p2align	3               # -- Begin function display
.LCPI2_0:
	.quad	4652007308841189376     # double 1000
	.text
	.globl	display
	.p2align	4, 0x90
	.type	display,@function
display:                                # @display
	.cfi_startproc
# %bb.0:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$45, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$34, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$8, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$72, %rsp
	.cfi_def_cfa_offset 128
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movl	%esi, %r13d
	movq	%rdi, %rbx
	callq	insCacheCallback
	movl	$1, %esi
	movq	%rbx, %rdi
	callq	dataReadCacheCallback
	movl	(%rbx), %r14d
	leaq	12(%rbx), %rdi
	movl	$4, %esi
	callq	dataReadCacheCallback
	movl	12(%rbx), %ebp
	leaq	4(%rsp), %r15
	movl	$4, %esi
	movq	%r15, %rdi
	callq	dataWriteCacheCallback
	movl	%ebp, 4(%rsp)
	leaq	48(%rsp), %rdx
	movl	$2, %edi
	movq	%r15, %rsi
	movl	$20, %ecx
	callq	inet_ntop
	movq	%rax, %r12
	movl	$1, %esi
	movq	%rbx, %rdi
	callq	dataReadCacheCallback
	movl	(%rbx), %ebp
	leaq	8(%rbx), %rdi
	movl	$1, %esi
	movq	%rdi, 16(%rsp)          # 8-byte Spill
	callq	dataReadCacheCallback
	xorl	%r15d, %r15d
	cmpb	$-1, 8(%rbx)
	je	.LBB2_3
# %bb.1:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$8, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$8, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$9, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	movq	%r12, 8(%rsp)           # 8-byte Spill
	movl	%r13d, %r12d
	andl	$15, %r14d
	leaq	(%rbx,%r14,4), %r13
	callq	insCacheCallback
	movl	$1, %esi
	movq	%r13, %rdi
	callq	dataReadCacheCallback
	cmpb	$8, (%r13)
	je	.LBB2_3
# %bb.2:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$83, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$49, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$10, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	shll	$2, %ebp
	andl	$60, %ebp
	subl	%ebp, %r12d
	callq	insCacheCallback
	leaq	24(%rsp), %rbp
	movq	%rbp, %rdi
	xorl	%esi, %esi
	callq	gettimeofday
	movl	$8, %esi
	movq	%rbp, %rdi
	callq	dataReadCacheCallback
	imulq	$1000000, 24(%rsp), %r14 # imm = 0xF4240
	leaq	32(%rsp), %rdi
	movl	$8, %esi
	callq	dataReadCacheCallback
	addq	32(%rsp), %r14
	movl	$1, %esi
	movq	%rbx, %rdi
	callq	dataReadCacheCallback
	movl	(%rbx), %eax
	andl	$15, %eax
	leaq	(%rbx,%rax,4), %rdi
	addq	$8, %rdi
	leaq	40(%rsp), %rsi
	movl	$10, %edx
	callq	strtol
	movq	%rax, %r15
	movl	$1, %esi
	movq	%r13, %rdi
	callq	dataReadCacheCallback
	movzbl	(%r13), %eax
	movl	%eax, (%rsp)            # 4-byte Spill
	leaq	6(%r13), %rdi
	movl	$2, %esi
	callq	dataReadCacheCallback
	movzwl	6(%r13), %ebp
	movl	$1, %esi
	movq	16(%rsp), %rdi          # 8-byte Reload
	callq	dataReadCacheCallback
	subq	%r15, %r14
	cvtsi2ss	%r14, %xmm0
	movzbl	8(%rbx), %r9d
	cvtss2sd	%xmm0, %xmm0
	divsd	.LCPI2_0(%rip), %xmm0
	movl	$.L.str, %edi
	movl	%r12d, %esi
	movq	8(%rsp), %rdx           # 8-byte Reload
	movl	(%rsp), %ecx            # 4-byte Reload
	movl	%ebp, %r8d
	movb	$1, %al
	callq	printf
	movl	$stdout, %edi
	movl	$8, %esi
	callq	dataReadCacheCallback
	movq	stdout(%rip), %rdi
	callq	fflush
	movl	$1, %r15d
.LBB2_3:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$10, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$9, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$11, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	%r15d, %eax
	addq	$72, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	display, .Lfunc_end1-display
	.cfi_endproc
                                        # -- End function
	.globl	listener                # -- Begin function listener
	.p2align	4, 0x90
	.type	listener,@function
listener:                               # @listener
	.cfi_startproc
# %bb.0:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$18, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$14, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$12, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$1064, %rsp             # imm = 0x428
	.cfi_def_cfa_offset 1120
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movl	%edi, %r13d
	callq	insCacheCallback
	movl	$2, %edi
	movl	$3, %esi
	movl	$1, %edx
	callq	socket
	testl	%eax, %eax
	js	.LBB3_8
# %bb.1:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$13, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$10, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$13, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	movl	%eax, %r14d
	callq	insCacheCallback
	movl	$.Lstr, %edi
	callq	puts
	movl	$stdout, %edi
	movl	$8, %esi
	callq	dataReadCacheCallback
	movq	stdout(%rip), %rdi
	callq	fflush
	xorl	%r12d, %r12d
	leaq	12(%rsp), %r15
	leaq	32(%rsp), %rbp
	.p2align	4, 0x90
.LBB3_2:                                # =>This Inner Loop Header: Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$21, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$17, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$14, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$4, %esi
	movq	%r15, %rdi
	callq	dataWriteCacheCallback
	movl	$16, 12(%rsp)
	movl	$1024, %edx             # imm = 0x400
	movq	%rbp, %rdi
	xorl	%esi, %esi
	callq	memset
	movl	$1024, %edx             # imm = 0x400
	movl	%r14d, %edi
	movq	%rbp, %rsi
	xorl	%ecx, %ecx
	leaq	16(%rsp), %r8
	movq	%r15, %r9
	callq	recvfrom
	movq	%rax, %rbx
	testl	%ebx, %ebx
	jle	.LBB3_4
# %bb.3:                                #   in Loop: Header=BB3_2 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$6, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$5, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$15, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movq	%rbp, %rdi
	movl	%ebx, %esi
	callq	display
	cmpl	$1, %eax
	sbbl	$-1, %r12d
.LBB3_5:                                #   in Loop: Header=BB3_2 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$16, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	cmpl	$-1, %r13d
	je	.LBB3_2
# %bb.6:                                #   in Loop: Header=BB3_2 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$2, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$17, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	cmpl	%r13d, %r12d
	jl	.LBB3_2
	jmp	.LBB3_7
.LBB3_4:                                #   in Loop: Header=BB3_2 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$3, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$18, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.L.str.3, %edi
	callq	perror
	jmp	.LBB3_5
.LBB3_7:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$9, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$8, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$19, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	addq	$1064, %rsp             # imm = 0x428
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.LBB3_8:
	.cfi_def_cfa_offset 1120
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$5, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$4, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$20, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.L.str.1, %edi
	callq	perror
	xorl	%edi, %edi
	callq	exit
.Lfunc_end2:
	.size	listener, .Lfunc_end2-listener
	.cfi_endproc
                                        # -- End function
	.section	.rodata.cst4,"aM",@progbits,4
	.p2align	2               # -- Begin function ping
.LCPI4_0:
	.long	1232348160              # float 1.0E+6
	.text
	.globl	ping
	.p2align	4, 0x90
	.type	ping,@function
ping:                                   # @ping
	.cfi_startproc
# %bb.0:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$25, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$19, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$21, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r13
	.cfi_def_cfa_offset 40
	pushq	%r12
	.cfi_def_cfa_offset 48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	subq	$120, %rsp
	.cfi_def_cfa_offset 176
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movl	%esi, 12(%rsp)          # 4-byte Spill
	movss	%xmm0, 8(%rsp)          # 4-byte Spill
	movq	%rdi, 24(%rsp)          # 8-byte Spill
	callq	insCacheCallback
	leaq	16(%rsp), %rdi
	movl	$4, %esi
	callq	dataWriteCacheCallback
	movl	$64, 16(%rsp)
	movl	$2, %edi
	movl	$3, %esi
	movl	$1, %edx
	callq	socket
	testl	%eax, %eax
	js	.LBB4_1
# %bb.2:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$11, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$9, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$22, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	movl	%eax, %ebx
	callq	insCacheCallback
	leaq	16(%rsp), %rcx
	movl	%ebx, %edi
	xorl	%esi, %esi
	movl	$2, %edx
	movl	$4, %r8d
	callq	setsockopt
	testl	%eax, %eax
	jne	.LBB4_3
.LBB4_4:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$9, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$8, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$23, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	%ebx, 20(%rsp)          # 4-byte Spill
	movl	%ebx, %edi
	movl	$4, %esi
	movl	$2048, %edx             # imm = 0x800
	xorl	%eax, %eax
	callq	fcntl
	testl	%eax, %eax
	jne	.LBB4_5
.LBB4_6:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$21, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$10, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$24, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$100000, %edi           # imm = 0x186A0
	callq	usleep
	leaq	56(%rsp), %rbp
	movss	8(%rsp), %xmm0          # 4-byte Reload
                                        # xmm0 = mem[0],zero,zero,zero
	mulss	.LCPI4_0(%rip), %xmm0
	cvttss2si	%xmm0, %eax
	movl	%eax, 8(%rsp)           # 4-byte Spill
	movl	$1, %ebx
	leaq	48(%rsp), %r12
	leaq	32(%rsp), %r14
	.p2align	4, 0x90
.LBB4_7:                                # =>This Inner Loop Header: Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$69, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$53, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$25, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	movl	%ebx, %r15d
	callq	insCacheCallback
	xorps	%xmm0, %xmm0
	movaps	%xmm0, 96(%rsp)
	movaps	%xmm0, 80(%rsp)
	movaps	%xmm0, 64(%rsp)
	movaps	%xmm0, 48(%rsp)
	movl	$1, %esi
	movq	%r12, %rdi
	callq	dataWriteCacheCallback
	movb	$8, 48(%rsp)
	movl	$pid, %edi
	movl	$4, %esi
	callq	dataReadCacheCallback
	movzwl	pid(%rip), %ebx
	movl	$2, %esi
	leaq	52(%rsp), %rdi
	callq	dataWriteCacheCallback
	movw	%bx, 52(%rsp)
	movq	%r14, %rdi
	xorl	%esi, %esi
	callq	gettimeofday
	movl	$8, %esi
	movq	%r14, %rdi
	callq	dataReadCacheCallback
	imulq	$1000000, 32(%rsp), %r13 # imm = 0xF4240
	movl	$8, %esi
	leaq	40(%rsp), %rdi
	callq	dataReadCacheCallback
	addq	40(%rsp), %r13
	xorps	%xmm0, %xmm0
	movups	%xmm0, 32(%rbp)
	movups	%xmm0, 16(%rbp)
	movups	%xmm0, (%rbp)
	movq	$0, 48(%rbp)
	movl	$.L.str.6, %esi
	movq	%rbp, %rdi
	movq	%r13, %rdx
	xorl	%eax, %eax
	callq	sprintf
	movl	$2, %esi
	leaq	54(%rsp), %rdi
	callq	dataWriteCacheCallback
	movw	%r15w, 54(%rsp)
	movq	%r12, %rdi
	movl	$64, %esi
	callq	checksum
	movl	%eax, %ebx
	movl	$2, %esi
	leaq	50(%rsp), %rdi
	callq	dataWriteCacheCallback
	movw	%bx, 50(%rsp)
	movl	$64, %edx
	movl	20(%rsp), %edi          # 4-byte Reload
	movq	%r12, %rsi
	xorl	%ecx, %ecx
	movq	24(%rsp), %r8           # 8-byte Reload
	movl	$16, %r9d
	callq	sendto
	testq	%rax, %rax
	jle	.LBB4_8
.LBB4_9:                                #   in Loop: Header=BB4_7 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$5, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$5, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$26, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	leal	1(%r15), %ebx
	movl	8(%rsp), %edi           # 4-byte Reload
	callq	usleep
	cmpl	$-1, 12(%rsp)           # 4-byte Folded Reload
	je	.LBB4_7
# %bb.10:                               #   in Loop: Header=BB4_7 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$2, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$27, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	cmpl	12(%rsp), %r15d         # 4-byte Folded Reload
	jl	.LBB4_7
	jmp	.LBB4_11
.LBB4_8:                                #   in Loop: Header=BB4_7 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$3, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$28, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.L.str.7, %edi
	callq	perror
	jmp	.LBB4_9
.LBB4_11:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$0, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$29, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
.LBB4_12:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$9, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$8, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$30, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	addq	$120, %rsp
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%r12
	.cfi_def_cfa_offset 40
	popq	%r13
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.LBB4_1:
	.cfi_def_cfa_offset 176
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$3, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$31, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.L.str.1, %edi
	callq	perror
	jmp	.LBB4_12
.LBB4_3:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$3, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$32, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.L.str.4, %edi
	callq	perror
	jmp	.LBB4_4
.LBB4_5:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$3, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$33, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.L.str.5, %edi
	callq	perror
	jmp	.LBB4_6
.Lfunc_end3:
	.size	ping, .Lfunc_end3-ping
	.cfi_endproc
                                        # -- End function
	.section	.rodata.cst4,"aM",@progbits,4
	.p2align	2               # -- Begin function main
.LCPI5_0:
	.long	1065353216              # float 1
.LCPI5_1:
	.long	0                       # float 0
	.text
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$14, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$10, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$34, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%rbx
	.cfi_def_cfa_offset 40
	subq	$24, %rsp
	.cfi_def_cfa_offset 64
	.cfi_offset %rbx, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rsi, %r15
	movl	%edi, %ebp
	callq	insCacheCallback
	movss	.LCPI5_0(%rip), %xmm0   # xmm0 = mem[0],zero,zero,zero
	movss	%xmm0, 4(%rsp)          # 4-byte Spill
	movl	$-1, %r14d
.LBB5_1:                                # =>This Loop Header: Depth=1
                                        #     Child Loop BB5_2 Depth 2
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$0, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$35, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
.LBB5_2:                                #   Parent Loop BB5_1 Depth=1
                                        # =>  This Inner Loop Header: Depth=2
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$5, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$6, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$36, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.L.str.8, %edx
	movl	%ebp, %edi
	movq	%r15, %rsi
	callq	getopt
	cmpl	$-1, %eax
	je	.LBB5_10
# %bb.3:                                #   in Loop: Header=BB5_2 Depth=2
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$37, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	cmpl	$99, %eax
	je	.LBB5_8
# %bb.4:                                #   in Loop: Header=BB5_2 Depth=2
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$38, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	cmpl	$105, %eax
	jne	.LBB5_15
# %bb.5:                                #   in Loop: Header=BB5_2 Depth=2
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$15, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$10, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$39, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$optarg, %edi
	movl	$8, %esi
	callq	dataReadCacheCallback
	movq	optarg(%rip), %rdi
	callq	atof
	cvtsd2ss	%xmm0, %xmm0
	movss	%xmm0, 4(%rsp)          # 4-byte Spill
	xorps	%xmm1, %xmm1
	ucomiss	%xmm0, %xmm1
	jb	.LBB5_2
	jmp	.LBB5_6
	.p2align	4, 0x90
.LBB5_8:                                #   in Loop: Header=BB5_1 Depth=1
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$7, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$7, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$40, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$optarg, %edi
	movl	$8, %esi
	callq	dataReadCacheCallback
	movq	optarg(%rip), %rdi
	callq	atoi
	movl	%eax, %r14d
	testl	%eax, %eax
	jg	.LBB5_1
# %bb.9:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$2, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$41, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.Lstr.13, %edi
	jmp	.LBB5_7
.LBB5_10:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$42, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	cmpl	$1, %ebp
	jle	.LBB5_15
# %bb.11:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$55, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$45, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$43, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	callq	getpid
	movl	%eax, %ebx
	movl	$pid, %edi
	movl	$4, %esi
	callq	dataWriteCacheCallback
	movl	%ebx, pid(%rip)
	movl	$.L.str.12, %edi
	callq	getprotobyname
	movq	%rax, %rbx
	movl	$proto, %edi
	movl	$8, %esi
	callq	dataWriteCacheCallback
	movq	%rbx, proto(%rip)
	movslq	%ebp, %rbx
	leaq	(%r15,%rbx,8), %rdi
	addq	$-8, %rdi
	movl	$8, %esi
	callq	dataReadCacheCallback
	movq	-8(%r15,%rbx,8), %rdi
	callq	gethostbyname
	movq	%rax, %rbx
	leaq	16(%rsp), %rdi
	movl	$8, %esi
	callq	dataWriteCacheCallback
	movq	$0, 16(%rsp)
	leaq	16(%rbx), %rdi
	movl	$4, %esi
	callq	dataReadCacheCallback
	movzwl	16(%rbx), %ebp
	leaq	8(%rsp), %rdi
	movl	$2, %esi
	callq	dataWriteCacheCallback
	movw	%bp, 8(%rsp)
	leaq	10(%rsp), %rdi
	movl	$2, %esi
	callq	dataWriteCacheCallback
	movw	$0, 10(%rsp)
	leaq	24(%rbx), %rdi
	movl	$8, %esi
	callq	dataReadCacheCallback
	movq	24(%rbx), %rbx
	movl	$8, %esi
	movq	%rbx, %rdi
	callq	dataReadCacheCallback
	movq	(%rbx), %rbx
	movl	$8, %esi
	movq	%rbx, %rdi
	callq	dataReadCacheCallback
	movl	(%rbx), %ebx
	leaq	12(%rsp), %rdi
	movl	$4, %esi
	callq	dataWriteCacheCallback
	movl	%ebx, 12(%rsp)
	callq	fork
	testl	%eax, %eax
	je	.LBB5_12
# %bb.13:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$9, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$7, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$44, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	leaq	8(%rsp), %rdi
	movss	4(%rsp), %xmm0          # 4-byte Reload
                                        # xmm0 = mem[0],zero,zero,zero
	movl	%r14d, %esi
	callq	ping
	xorl	%edi, %edi
	callq	wait
	jmp	.LBB5_14
.LBB5_12:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$2, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$2, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$45, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	%r14d, %edi
	callq	listener
.LBB5_14:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$10, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$7, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$46, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	xorl	%eax, %eax
	addq	$24, %rsp
	.cfi_def_cfa_offset 40
	popq	%rbx
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.LBB5_15:
	.cfi_def_cfa_offset 64
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$12, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$8, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$47, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$8, %esi
	movq	%r15, %rdi
	callq	dataReadCacheCallback
	movq	(%r15), %rsi
	movl	$.L.str.11, %edi
	xorl	%eax, %eax
	callq	printf
	xorl	%edi, %edi
	callq	exit
.LBB5_6:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$1, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$1, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$48, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	insCacheCallback
	movl	$.Lstr.14, %edi
.LBB5_7:
	pushq	%rax
	pushfq
	popq	%rax
	pushq	%rax
	pushq	%rdx
	pushq	%rcx
	movq	currBurstCyclesLeft@GOTPCREL(%rip), %rcx
	movq	(%rcx), %rdx
	subq	$4, %rdx
	movq	%rdx, (%rcx)
	movq	currBBInsCacheMissPenalty@GOTPCREL(%rip), %rcx
	movq	$3, (%rcx)
	movq	currBBID@GOTPCREL(%rip), %rcx
	movq	$49, (%rcx)
	callq	__Vt_Stub
	popq	%rcx
	popq	%rdx
	popq	%rax
	pushq	%rax
	popfq
	popq	%rax
	callq	puts
	xorl	%edi, %edi
	callq	exit
.Lfunc_end4:
	.size	main, .Lfunc_end4-main
	.cfi_endproc
                                        # -- End function
	.section	.text.__Vt_Stub,"axG",@progbits,__Vt_Stub,comdat
	.weak	__Vt_Stub               # -- Begin function __Vt_Stub
	.p2align	4, 0x90
	.type	__Vt_Stub,@function
__Vt_Stub:                              # @__Vt_Stub
# %bb.2:
	testq	%rdx, %rdx
	jns	.LBB1_0
# %bb.1:
	pushq	%rbp
	pushq	%rax
	pushq	%rbx
	pushq	%rsi
	pushq	%rdi
	pushq	%r8
	pushq	%r9
	pushq	%r10
	pushq	%r11
	callq	vtCallbackFn
	popq	%r11
	popq	%r10
	popq	%r9
	popq	%r8
	popq	%rdi
	popq	%rsi
	popq	%rbx
	popq	%rax
	popq	%rbp
.LBB1_0:
	retq
.Lfunc_end5:
	.size	__Vt_Stub, .Lfunc_end5-__Vt_Stub
                                        # -- End function
	.type	pid,@object             # @pid
	.data
	.globl	pid
	.p2align	2
pid:
	.long	4294967295              # 0xffffffff
	.size	pid, 4

	.type	proto,@object           # @proto
	.bss
	.globl	proto
	.p2align	3
proto:
	.quad	0
	.size	proto, 8

	.type	.L.str,@object          # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%d bytes from: %s: icmp_type = %d icmp_seq = %d ttl = %d time = %f ms\n"
	.size	.L.str, 71

	.type	.L.str.1,@object        # @.str.1
.L.str.1:
	.asciz	"socket"
	.size	.L.str.1, 7

	.type	.L.str.3,@object        # @.str.3
.L.str.3:
	.asciz	"recvfrom"
	.size	.L.str.3, 9

	.type	.L.str.4,@object        # @.str.4
.L.str.4:
	.asciz	"Set TTL option"
	.size	.L.str.4, 15

	.type	.L.str.5,@object        # @.str.5
.L.str.5:
	.asciz	"Request nonblocking I/O"
	.size	.L.str.5, 24

	.type	.L.str.6,@object        # @.str.6
.L.str.6:
	.asciz	"%lu"
	.size	.L.str.6, 4

	.type	.L.str.7,@object        # @.str.7
.L.str.7:
	.asciz	"sendto"
	.size	.L.str.7, 7

	.type	.L.str.8,@object        # @.str.8
.L.str.8:
	.asciz	"i:c:h"
	.size	.L.str.8, 6

	.type	.L.str.11,@object       # @.str.11
.L.str.11:
	.asciz	"usage: %s [-ic] <addr>\n Options:\n -i: interval in secs\n -c number of pings"
	.size	.L.str.11, 75

	.type	.L.str.12,@object       # @.str.12
.L.str.12:
	.asciz	"ICMP"
	.size	.L.str.12, 5

	.type	.Lstr,@object           # @str
.Lstr:
	.asciz	"Started listener !"
	.size	.Lstr, 19

	.type	.Lstr.13,@object        # @str.13
.Lstr.13:
	.asciz	"ERROR: num pings must be positive!"
	.size	.Lstr.13, 35

	.type	.Lstr.14,@object        # @str.14
.Lstr.14:
	.asciz	"ERROR: ping interval must be positive!"
	.size	.Lstr.14, 39


	.ident	"clang version 9.0.1 (https://github.com/llvm/llvm-project.git c1a0a213378a458fbea1a5c77b315c7dce08fd05)"
	.section	".note.GNU-stack","",@progbits
	.addrsig
	.addrsig_sym SetLoopLookahead
	.addrsig_sym insCacheCallback
	.addrsig_sym dataReadCacheCallback
	.addrsig_sym dataWriteCacheCallback
