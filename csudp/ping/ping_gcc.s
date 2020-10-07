	.file	"ping.c"
	.text
	.globl	pid
	.data
	.align 4
	.type	pid, @object
	.size	pid, 4
pid:
	.long	-1
	.globl	proto
	.bss
	.align 8
	.type	proto, @object
	.size	proto, 8
proto:
	.zero	8
	.text
	.globl	checksum
	.type	checksum, @function
checksum:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -24(%rbp)
	movl	%esi, -28(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, -8(%rbp)
	movl	$0, -12(%rbp)
	movl	$0, -12(%rbp)
	jmp	.L2
.L3:
	movq	-8(%rbp), %rax
	leaq	2(%rax), %rdx
	movq	%rdx, -8(%rbp)
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	addl	%eax, -12(%rbp)
	subl	$2, -28(%rbp)
.L2:
	cmpl	$1, -28(%rbp)
	jg	.L3
	cmpl	$1, -28(%rbp)
	jne	.L4
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	addl	%eax, -12(%rbp)
.L4:
	movl	-12(%rbp), %eax
	shrl	$16, %eax
	movl	%eax, %edx
	movl	-12(%rbp), %eax
	movzwl	%ax, %eax
	addl	%edx, %eax
	movl	%eax, -12(%rbp)
	movl	-12(%rbp), %eax
	shrl	$16, %eax
	addl	%eax, -12(%rbp)
	movl	-12(%rbp), %eax
	notl	%eax
	movw	%ax, -14(%rbp)
	movzwl	-14(%rbp), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	checksum, .-checksum
	.section	.rodata
	.align 8
.LC1:
	.string	"%d bytes from: %s: icmp_type = %d icmp_seq = %d ttl = %d time = %f ms\n"
	.text
	.globl	display
	.type	display, @function
display:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$144, %rsp
	movq	%rdi, -136(%rbp)
	movl	%esi, -140(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	-136(%rbp), %rax
	movq	%rax, -96(%rbp)
	movq	-96(%rbp), %rax
	movzbl	(%rax), %eax
	andl	$15, %eax
	movzbl	%al, %eax
	sall	$2, %eax
	movslq	%eax, %rdx
	movq	-136(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -88(%rbp)
	movq	-96(%rbp), %rax
	movl	12(%rax), %eax
	movl	%eax, -116(%rbp)
	movq	-96(%rbp), %rax
	movl	16(%rax), %eax
	movl	%eax, -112(%rbp)
	leaq	-32(%rbp), %rdx
	leaq	-116(%rbp), %rax
	movl	$20, %ecx
	movq	%rax, %rsi
	movl	$2, %edi
	call	inet_ntop@PLT
	movq	%rax, -80(%rbp)
	movq	-96(%rbp), %rax
	movzbl	(%rax), %eax
	andl	$15, %eax
	movzbl	%al, %eax
	leal	0(,%rax,4), %edx
	movl	-140(%rbp), %eax
	subl	%edx, %eax
	movl	%eax, -108(%rbp)
	movq	-96(%rbp), %rax
	movzbl	8(%rax), %eax
	cmpb	$-1, %al
	je	.L7
	movq	-88(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	$8, %al
	je	.L7
	leaq	-48(%rbp), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	gettimeofday@PLT
	movq	-48(%rbp), %rax
	imulq	$1000000, %rax, %rdx
	movq	-40(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -72(%rbp)
	movq	-96(%rbp), %rax
	movzbl	(%rax), %eax
	andl	$15, %eax
	movzbl	%al, %eax
	sall	$2, %eax
	cltq
	leaq	8(%rax), %rdx
	movq	-136(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -64(%rbp)
	leaq	-104(%rbp), %rcx
	movq	-64(%rbp), %rax
	movl	$10, %edx
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	strtol@PLT
	movq	%rax, -56(%rbp)
	movq	-72(%rbp), %rax
	subq	-56(%rbp), %rax
	cvtsi2ssq	%rax, %xmm0
	cvtss2sd	%xmm0, %xmm0
	movsd	.LC0(%rip), %xmm1
	divsd	%xmm1, %xmm0
	movq	-96(%rbp), %rax
	movzbl	8(%rax), %eax
	movzbl	%al, %edi
	movq	-88(%rbp), %rax
	movzwl	6(%rax), %eax
	movzwl	%ax, %esi
	movq	-88(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %ecx
	movq	-80(%rbp), %rdx
	movl	-108(%rbp), %eax
	movl	%edi, %r9d
	movl	%esi, %r8d
	movl	%eax, %esi
	leaq	.LC1(%rip), %rdi
	movl	$1, %eax
	call	printf@PLT
	movq	stdout(%rip), %rax
	movq	%rax, %rdi
	call	fflush@PLT
	movl	$1, %eax
	jmp	.L9
.L7:
	movl	$0, %eax
.L9:
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L10
	call	__stack_chk_fail@PLT
.L10:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	display, .-display
	.section	.rodata
.LC2:
	.string	"socket"
.LC3:
	.string	"Started listener !"
.LC4:
	.string	"recvfrom"
	.text
	.globl	listener
	.type	listener, @function
listener:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$1088, %rsp
	movl	%edi, -1076(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	$1, %edx
	movl	$3, %esi
	movl	$2, %edi
	call	socket@PLT
	movl	%eax, -1064(%rbp)
	cmpl	$0, -1064(%rbp)
	jns	.L12
	leaq	.LC2(%rip), %rdi
	call	perror@PLT
	movl	$0, %edi
	call	exit@PLT
.L12:
	leaq	.LC3(%rip), %rdi
	call	puts@PLT
	movq	stdout(%rip), %rax
	movq	%rax, %rdi
	call	fflush@PLT
	movl	$0, -1068(%rbp)
	movl	$0, -1060(%rbp)
.L17:
	movl	$16, -1072(%rbp)
	movl	$0, -1060(%rbp)
	leaq	-1040(%rbp), %rax
	movl	$1024, %esi
	movq	%rax, %rdi
	call	bzero@PLT
	leaq	-1072(%rbp), %rcx
	leaq	-1056(%rbp), %rdx
	leaq	-1040(%rbp), %rsi
	movl	-1064(%rbp), %eax
	movq	%rcx, %r9
	movq	%rdx, %r8
	movl	$0, %ecx
	movl	$1024, %edx
	movl	%eax, %edi
	call	recvfrom@PLT
	movl	%eax, -1060(%rbp)
	cmpl	$0, -1060(%rbp)
	jle	.L13
	movl	-1060(%rbp), %edx
	leaq	-1040(%rbp), %rax
	movl	%edx, %esi
	movq	%rax, %rdi
	call	display
	testl	%eax, %eax
	je	.L15
	addl	$1, -1068(%rbp)
	jmp	.L15
.L13:
	leaq	.LC4(%rip), %rdi
	call	perror@PLT
.L15:
	movl	-1068(%rbp), %eax
	cmpl	-1076(%rbp), %eax
	jl	.L17
	cmpl	$-1, -1076(%rbp)
	je	.L17
	movl	$0, %edi
	call	exit@PLT
	.cfi_endproc
.LFE7:
	.size	listener, .-listener
	.section	.rodata
.LC5:
	.string	"Set TTL option"
.LC6:
	.string	"Request nonblocking I/O"
.LC7:
	.string	"%lu"
.LC8:
	.string	"sendto"
	.text
	.globl	ping
	.type	ping, @function
ping:
.LFB8:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$144, %rsp
	movq	%rdi, -136(%rbp)
	movss	%xmm0, -140(%rbp)
	movl	%esi, -144(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movl	$64, -124(%rbp)
	movl	$1, -116(%rbp)
	movl	$1, %edx
	movl	$3, %esi
	movl	$2, %edi
	call	socket@PLT
	movl	%eax, -112(%rbp)
	cmpl	$0, -112(%rbp)
	jns	.L20
	leaq	.LC2(%rip), %rdi
	call	perror@PLT
	jmp	.L19
.L20:
	leaq	-124(%rbp), %rdx
	movl	-112(%rbp), %eax
	movl	$4, %r8d
	movq	%rdx, %rcx
	movl	$2, %edx
	movl	$0, %esi
	movl	%eax, %edi
	call	setsockopt@PLT
	testl	%eax, %eax
	je	.L22
	leaq	.LC5(%rip), %rdi
	call	perror@PLT
.L22:
	movl	-112(%rbp), %eax
	movl	$2048, %edx
	movl	$4, %esi
	movl	%eax, %edi
	movl	$0, %eax
	call	fcntl@PLT
	testl	%eax, %eax
	je	.L23
	leaq	.LC6(%rip), %rdi
	call	perror@PLT
.L23:
	movl	$100000, %edi
	call	usleep@PLT
.L29:
	movl	$16, -108(%rbp)
	leaq	-80(%rbp), %rax
	movl	$64, %esi
	movq	%rax, %rdi
	call	bzero@PLT
	movb	$8, -80(%rbp)
	movl	pid(%rip), %eax
	movw	%ax, -76(%rbp)
	leaq	-96(%rbp), %rax
	movl	$0, %esi
	movq	%rax, %rdi
	call	gettimeofday@PLT
	movq	-96(%rbp), %rax
	imulq	$1000000, %rax, %rdx
	movq	-88(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -104(%rbp)
	movl	$0, -120(%rbp)
	jmp	.L24
.L25:
	movl	-120(%rbp), %eax
	cltq
	movb	$0, -72(%rbp,%rax)
	addl	$1, -120(%rbp)
.L24:
	movl	-120(%rbp), %eax
	cmpl	$55, %eax
	jbe	.L25
	movq	-104(%rbp), %rax
	leaq	-80(%rbp), %rdx
	leaq	8(%rdx), %rcx
	movq	%rax, %rdx
	leaq	.LC7(%rip), %rsi
	movq	%rcx, %rdi
	movl	$0, %eax
	call	sprintf@PLT
	movl	-116(%rbp), %eax
	movw	%ax, -74(%rbp)
	leaq	-80(%rbp), %rax
	movl	$64, %esi
	movq	%rax, %rdi
	call	checksum
	movw	%ax, -78(%rbp)
	movq	-136(%rbp), %rdx
	leaq	-80(%rbp), %rsi
	movl	-112(%rbp), %eax
	movl	$16, %r9d
	movq	%rdx, %r8
	movl	$0, %ecx
	movl	$64, %edx
	movl	%eax, %edi
	call	sendto@PLT
	testq	%rax, %rax
	jg	.L26
	leaq	.LC8(%rip), %rdi
	call	perror@PLT
.L26:
	addl	$1, -116(%rbp)
	movss	-140(%rbp), %xmm1
	movss	.LC9(%rip), %xmm0
	mulss	%xmm1, %xmm0
	cvttss2si	%xmm0, %eax
	movl	%eax, %edi
	call	usleep@PLT
	cmpl	$-1, -144(%rbp)
	je	.L29
	movl	-116(%rbp), %eax
	cmpl	-144(%rbp), %eax
	jg	.L31
	jmp	.L29
.L31:
	nop
.L19:
	movq	-8(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L30
	call	__stack_chk_fail@PLT
.L30:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	ping, .-ping
	.section	.rodata
	.align 8
.LC12:
	.string	"ERROR: ping interval must be positive!"
	.align 8
.LC13:
	.string	"ERROR: num pings must be positive!"
	.align 8
.LC14:
	.string	"usage: %s [-ic] <addr>\n Options:\n -i: interval in secs\n -c number of pings"
.LC15:
	.string	"i:c:h"
.LC16:
	.string	"ICMP"
	.text
	.globl	main
	.type	main, @function
main:
.LFB9:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$144, %rsp
	movl	%edi, -132(%rbp)
	movq	%rsi, -144(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movss	.LC10(%rip), %xmm0
	movss	%xmm0, -116(%rbp)
	movl	$-1, -112(%rbp)
	movl	$0, -108(%rbp)
	jmp	.L33
.L40:
	movl	-108(%rbp), %eax
	cmpl	$99, %eax
	je	.L35
	cmpl	$105, %eax
	jne	.L47
	movq	optarg(%rip), %rax
	movq	%rax, %rdi
	call	atof@PLT
	cvtsd2ss	%xmm0, %xmm1
	movss	%xmm1, -116(%rbp)
	pxor	%xmm0, %xmm0
	ucomiss	-116(%rbp), %xmm0
	jb	.L48
	leaq	.LC12(%rip), %rdi
	call	puts@PLT
	movl	$0, %edi
	call	exit@PLT
.L48:
	jmp	.L33
.L35:
	movq	optarg(%rip), %rax
	movq	%rax, %rdi
	call	atoi@PLT
	movl	%eax, -112(%rbp)
	cmpl	$0, -112(%rbp)
	jg	.L33
	leaq	.LC13(%rip), %rdi
	call	puts@PLT
	movl	$0, %edi
	call	exit@PLT
.L47:
	movq	-144(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	leaq	.LC14(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %edi
	call	exit@PLT
.L33:
	movq	-144(%rbp), %rcx
	movl	-132(%rbp), %eax
	leaq	.LC15(%rip), %rdx
	movq	%rcx, %rsi
	movl	%eax, %edi
	call	getopt@PLT
	movl	%eax, -108(%rbp)
	cmpl	$-1, -108(%rbp)
	jne	.L40
	cmpl	$1, -132(%rbp)
	jg	.L41
	movq	-144(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rsi
	leaq	.LC14(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %edi
	call	exit@PLT
.L41:
	call	getpid@PLT
	movl	%eax, pid(%rip)
	leaq	.LC16(%rip), %rdi
	call	getprotobyname@PLT
	movq	%rax, proto(%rip)
	movl	-132(%rbp), %eax
	cltq
	salq	$3, %rax
	leaq	-8(%rax), %rdx
	movq	-144(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	gethostbyname@PLT
	movq	%rax, -104(%rbp)
	leaq	-80(%rbp), %rax
	movl	$16, %esi
	movq	%rax, %rdi
	call	bzero@PLT
	movq	-104(%rbp), %rax
	movl	16(%rax), %eax
	movw	%ax, -80(%rbp)
	movw	$0, -78(%rbp)
	movq	-104(%rbp), %rax
	movq	24(%rax), %rax
	movq	(%rax), %rax
	movq	(%rax), %rax
	movl	%eax, -76(%rbp)
	call	fork@PLT
	testl	%eax, %eax
	jne	.L42
	movl	-112(%rbp), %eax
	movl	%eax, %edi
	call	listener
	jmp	.L43
.L42:
	movl	-112(%rbp), %ecx
	movl	-116(%rbp), %edx
	leaq	-80(%rbp), %rax
	movl	%ecx, %esi
	movl	%edx, -136(%rbp)
	movss	-136(%rbp), %xmm0
	movq	%rax, %rdi
	call	ping
.L43:
	movl	$0, %edi
	call	wait@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rcx
	xorq	%fs:40, %rcx
	je	.L45
	call	__stack_chk_fail@PLT
.L45:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	main, .-main
	.section	.rodata
	.align 8
.LC0:
	.long	0
	.long	1083129856
	.align 4
.LC9:
	.long	1232348160
	.align 4
.LC10:
	.long	1065353216
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
