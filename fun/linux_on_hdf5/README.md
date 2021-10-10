# Embedding Linux on HDF5

## Description

This demo shows how to boot a Linux kernel and run an initramfs image
each time a UDF dataset is read. Messages printed on the console are
shown on that dataset.

## Data preparation

We use the Tiny QEMU image project to automate the process of
building a kernel image and preparing an initial RAM disk. Please run
the following commands to build those files:

```
$ git clone --recursive https://github.com/reubenhwk/tiny-qemu-image.git
$ cd tiny-qemu-image
$ make
```

Next, create a new HDF5 file and store the kernel image and initramfs
images as separate datasets. The following Python script does it:

```
import h5py
import numpy as np
f = h5py.File('linux.h5', 'w')

kernel = open('bzImage', 'rb').read()
initramfs = open('initramfs-busybox-x86.cpio.gz', 'rb').read()

dset_kernel = f.create_dataset('kernel', (len(kernel),), dtype=np.uint8)
dset_initramfs = f.create_dataset('initramfs', (len(initramfs),), dtype=np.uint8)

dset_kernel[:] = [int(x) for x in kernel]
dset_initramfs[:] = [int(x) for x in initramfs]

f.close()
```

Check that the data has been produced with a call to `h5dump -H linux.h5`.
The following output is expected:

```
HDF5 "linux.h5" {
GROUP "/" {
   DATASET "initramfs" {
      DATATYPE  H5T_STD_U8LE
      DATASPACE  SIMPLE { ( 1283828 ) / ( 1283828 ) }
   }
   DATASET "kernel" {
      DATATYPE  H5T_STD_U8LE
      DATASPACE  SIMPLE { ( 1646640 ) / ( 1646640 ) }
   }
}
}
```

Finally, create the UDF dataset as a collection of 200 lines with 180 characters each:
```
hdf5-udf linux.h5 linux.py 'console:200:string(180)'
```

## Data consumption

Simply read the dataset with `h5dump -d /console linux.h5`. This is the expected output:

```
HDF5 "linux.h5" {
DATASET "/console" {
   DATATYPE  H5T_STRING {
      STRSIZE 180;
      STRPAD H5T_STR_NULLTERM;
      CSET H5T_CSET_ASCII;
      CTYPE H5T_C_S1;
   }
   DATASPACE  SIMPLE { ( 200 ) / ( 200 ) }
   DATA {   DATA {
   (0): "[    0.000000] Linux version 4.20.0+ (lucasvr@Octopus) (gcc version 9.2.0 (GCC)) #1 Thu Oct 7 23:03:34 -03 2021",
   (1): "[    0.000000] Command line: ",
   (2): "[    0.000000] x86/fpu: x87 FPU will use FXSAVE",
   (3): "[    0.000000] BIOS-provided physical RAM map:",
   (4): "[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable",
   (5): "[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved",
   (6): "[    0.000000] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved",
   (7): "[    0.000000] BIOS-e820: [mem 0x0000000000100000-0x0000000007fdffff] usable",
   (8): "[    0.000000] BIOS-e820: [mem 0x0000000007fe0000-0x0000000007ffffff] reserved",
   (9): "[    0.000000] BIOS-e820: [mem 0x00000000feffc000-0x00000000feffffff] reserved",
   (10): "[    0.000000] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved",
   (11): "[    0.000000] NX (Execute Disable) protection: active",
   (12): "[    0.000000] tsc: Fast TSC calibration using PIT",
   (13): "[    0.000000] tsc: Detected 1992.107 MHz processor",
   (14): "[    0.000592] last_pfn = 0x7fe0 max_arch_pfn = 0x400000000",
   (15): "[    0.000594] x86/PAT: Configuration [0-7]: WB  WT  UC- UC  WB  WT  UC- UC  ",
   (16): "[    0.006835] found SMP MP-table at [mem 0x000f5ab0-0x000f5abf] mapped at [(____ptrval____)]",
   (17): "[    0.007109] RAMDISK: [mem 0x07ea6000-0x07fdffff]",
   (18): "[    0.007127] ACPI: Early table checksum verification disabled",
   (19): "[    0.007204] ACPI: RSDP 0x00000000000F58D0 000014 (v00 BOCHS )",
   (20): "[    0.007213] ACPI: RSDT 0x0000000007FE156F 000030 (v01 BOCHS  BXPCRSDT 00000001 BXPC 00000001)",
   (21): "[    0.007226] ACPI: FACP 0x0000000007FE144B 000074 (v01 BOCHS  BXPCFACP 00000001 BXPC 00000001)",
   (22): "[    0.007234] ACPI: DSDT 0x0000000007FE0040 00140B (v01 BOCHS  BXPCDSDT 00000001 BXPC 00000001)",
   (23): "[    0.007238] ACPI: FACS 0x0000000007FE0000 000040",
   (24): "[    0.007241] ACPI: APIC 0x0000000007FE14BF 000078 (v01 BOCHS  BXPCAPIC 00000001 BXPC 00000001)",
   (25): "[    0.007245] ACPI: HPET 0x0000000007FE1537 000038 (v01 BOCHS  BXPCHPET 00000001 BXPC 00000001)",
   (26): "[    0.007811] Zone ranges:",
   (27): "[    0.007814]   DMA32    [mem 0x0000000000001000-0x0000000007fdffff]",
   (28): "[    0.007816]   Normal   empty",
   (29): "[    0.007817] Movable zone start for each node",
   (30): "[    0.007818] Early memory node ranges",
   (31): "[    0.007819]   node   0: [mem 0x0000000000001000-0x000000000009efff]",
   (32): "[    0.007820]   node   0: [mem 0x0000000000100000-0x0000000007fdffff]",
   (33): "[    0.007827] Zeroed struct page in unavailable ranges: 98 pages",
   (34): "[    0.007828] Initmem setup node 0 [mem 0x0000000000001000-0x0000000007fdffff]",
   (35): "[    0.008712] ACPI: LAPIC_NMI (acpi_id[0xff] dfl dfl lint[0x1])",
   (36): "[    0.008746] IOAPIC[0]: apic_id 0, version 17, address 0xfec00000, GSI 0-23",
   (37): "[    0.008752] ACPI: INT_SRC_OVR (bus 0 bus_irq 0 global_irq 2 dfl dfl)",
   (38): "[    0.008754] ACPI: INT_SRC_OVR (bus 0 bus_irq 5 global_irq 5 high level)",
   (39): "[    0.008755] ACPI: INT_SRC_OVR (bus 0 bus_irq 9 global_irq 9 high level)",
   (40): "[    0.008759] ACPI: INT_SRC_OVR (bus 0 bus_irq 10 global_irq 10 high level)",
   (41): "[    0.008760] ACPI: INT_SRC_OVR (bus 0 bus_irq 11 global_irq 11 high level)",
   (42): "[    0.008765] Using ACPI (MADT) for SMP configuration information",
   (43): "[    0.008767] ACPI: HPET id: 0x8086a201 base: 0xfed00000",
   (44): "[    0.008778] [mem 0x08000000-0xfeffbfff] available for PCI devices",
   (45): "[    0.008783] clocksource: refined-jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns",
   (46): "[    0.008807] Built 1 zonelists, mobility grouping on.  Total pages: 32169",
   (47): "[    0.008809] Kernel command line: ",
   (48): "[    0.008818] Dentry cache hash table entries: 16384 (order: 5, 131072 bytes)",
   (49): "[    0.008822] Inode-cache hash table entries: 8192 (order: 4, 65536 bytes)",
   (50): "[    0.009032] Memory: 114848K/130552K available (6146K kernel code, 347K rwdata, 388K rodata, 508K init, 1188K bss, 15704K reserved, 0K cma-reserved)",
   (51): "[    0.009076] NR_IRQS: 4352, nr_irqs: 48, preallocated irqs: 16",
   (52): "[    0.057452] printk: console [ttyS0] enabled",
   (53): "[    0.057819] ACPI: Core revision 20181003",
   (54): "[    0.058368] clocksource: hpet: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604467 ns",
   (55): "[    0.059194] APIC: Switch to symmetric I/O mode setup",
   (56): "[    0.060308] ..TIMER: vector=0x30 apic1=0 pin1=2 apic2=-1 pin2=-1",
   (57): "[    0.109210] clocksource: tsc-early: mask: 0xffffffffffffffff max_cycles: 0x396e1c8066d, max_idle_ns: 881590582267 ns",
   (58): "[    0.110000] Calibrating delay loop (skipped), value calculated using timer frequency.. 3984.21 BogoMIPS (lpj=19921070)",
   (59): "[    0.110776] pid_max: default: 4096 minimum: 301",
   (60): "[    0.111177] Mount-cache hash table entries: 512 (order: 0, 4096 bytes)",
   (61): "[    0.111743] Mountpoint-cache hash table entries: 512 (order: 0, 4096 bytes)",
   (62): "[    0.112456] Last level iTLB entries: 4KB 0, 2MB 0, 4MB 0",
   (63): "[    0.112876] Last level dTLB entries: 4KB 0, 2MB 0, 4MB 0, 1GB 0",
   (64): "[    0.113327] CPU: Intel QEMU Virtual CPU version 2.5+ (family: 0x6, model: 0x6, stepping: 0x3)",
   (65): "[    0.113953] Spectre V2 : Spectre mitigation: kernel not compiled with retpoline; no mitigation available!",
   (66): "[    0.113954] Speculative Store Bypass: Vulnerable",
   (67): "[    0.115254] Performance Events: PMU not available due to virtualization, using software events only.",
   (68): "[    0.229999] devtmpfs: initialized",
   (69): "[    0.229999] clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns",
   (70): "[    0.229999] random: get_random_u32 called from 0xffffffff810c8871 with crng_init=0",
   (71): "[    0.229999] NET: Registered protocol family 16",
   (72): "[    0.229999] cpuidle: using governor ladder",
   (73): "[    0.229999] ACPI: bus type PCI registered",
   (74): "[    0.229999] PCI: Using configuration type 1 for base access",
   (75): "[    0.229999] ACPI: Added _OSI(Module Device)",
   (76): "[    0.229999] ACPI: Added _OSI(Processor Device)",
   (77): "[    0.229999] ACPI: Added _OSI(3.0 _SCP Extensions)",
   (78): "[    0.229999] ACPI: Added _OSI(Processor Aggregator Device)",
   (79): "[    0.229999] ACPI: Added _OSI(Linux-Dell-Video)",
   (80): "[    0.229999] ACPI: Added _OSI(Linux-Lenovo-NV-HDMI-Audio)",
   (81): "[    0.229999] ACPI: 1 ACPI AML tables successfully acquired and loaded",
   (82): "[    0.229999] ACPI: Interpreter enabled",
   (83): "[    0.229999] ACPI: (supports S0 S5)",
   (84): "[    0.229999] ACPI: Using IOAPIC for interrupt routing",
   (85): "[    0.229999] PCI: Using host bridge windows from ACPI; if necessary, use "pci=nocrs" and report a bug",
   (86): "[    0.229999] ACPI: Enabled 2 GPEs in block 00 to 0F",
   (87): "[    0.230660] ACPI: PCI Root Bridge [PCI0] (domain 0000 [bus 00-ff])",
   (88): "[    0.231102] acpi PNP0A03:00: _OSC: OS supports [Segments]",
   (89): "[    0.231548] PCI host bridge to bus 0000:00",
   (90): "[    0.231834] pci_bus 0000:00: root bus resource [io  0x0000-0x0cf7 window]",
   (91): "[    0.232316] pci_bus 0000:00: root bus resource [io  0x0d00-0xffff window]",
   (92): "[    0.232787] pci_bus 0000:00: root bus resource [mem 0x000a0000-0x000bffff window]",
   (93): "[    0.233329] pci_bus 0000:00: root bus resource [mem 0x08000000-0xfebfffff window]",
   (94): "[    0.233870] pci_bus 0000:00: root bus resource [mem 0x100000000-0x17fffffff window]",
   (95): "[    0.234397] pci_bus 0000:00: root bus resource [bus 00-ff]",
   (96): "[    0.237063] pci 0000:00:01.1: legacy IDE quirk: reg 0x10: [io  0x01f0-0x01f7]",
   (97): "[    0.237738] pci 0000:00:01.1: legacy IDE quirk: reg 0x14: [io  0x03f6]",
   (98): "[    0.238176] pci 0000:00:01.1: legacy IDE quirk: reg 0x18: [io  0x0170-0x0177]",
   (99): "[    0.238675] pci 0000:00:01.1: legacy IDE quirk: reg 0x1c: [io  0x0376]",
   (100): "[    0.248515] ACPI: PCI Interrupt Link [LNKA] (IRQs 5 *10 11)",
   (101): "[    0.249027] ACPI: PCI Interrupt Link [LNKB] (IRQs 5 *10 11)",
   (102): "[    0.250070] ACPI: PCI Interrupt Link [LNKC] (IRQs 5 10 *11)",
   (103): "[    0.250571] ACPI: PCI Interrupt Link [LNKD] (IRQs 5 10 *11)",
   (104): "[    0.251061] ACPI: PCI Interrupt Link [LNKS] (IRQs *9)",
   (105): "[    0.251589] PCI: Using ACPI for IRQ routing",
   (106): "[    0.252166] clocksource: Switched to clocksource tsc-early",
   (107): "[    0.252703] pnp: PnP ACPI init",
   (108): "[    0.253229] pnp: PnP ACPI: found 6 devices",
   (109): "[    0.253663] NET: Registered protocol family 2",
   (110): "[    0.254037] tcp_listen_portaddr_hash hash table entries: 256 (order: 0, 4096 bytes)",
   (111): "[    0.254781] TCP established hash table entries: 1024 (order: 1, 8192 bytes)",
   (112): "[    0.255313] TCP bind hash table entries: 1024 (order: 1, 8192 bytes)",
   (113): "[    0.255784] TCP: Hash tables configured (established 1024 bind 1024)",
   (114): "[    0.256322] UDP hash table entries: 128 (order: 0, 4096 bytes)",
   (115): "[    0.256771] UDP-Lite hash table entries: 128 (order: 0, 4096 bytes)",
   (116): "[    0.257299] Unpacking initramfs...",
   (117): "[    0.269482] Freeing initrd memory: 1256K",
   (118): "[    0.269917] workingset: timestamp_bits=62 max_order=15 bucket_order=0",
   (119): "[    0.270492] Serial: 8250/16550 driver, 1 ports, IRQ sharing disabled",
   (120): "[    0.292971] 00:05: ttyS0 at I/O 0x3f8 (irq = 4, base_baud = 115200) is a 16550A",
   (121): "[    0.293643] NET: Registered protocol family 10",
   (122): "[    0.294023] Segment Routing with IPv6",
   (123): "[    0.294305] sched_clock: Marking stable (252194947, 40771960)->(424483355, -131516448)",
   (124): "[    0.295185] Freeing unused kernel image memory: 508K",
   (125): "[    0.295564] Write protecting the kernel read-only data: 10240k",
   (126): "[    0.296722] Freeing unused kernel image memory: 2032K",
   (127): "[    0.297223] Freeing unused kernel image memory: 1660K",
   (128): "[    0.297613] Run /init as init process",
   (129): "Welcome to HDF5-UDF-Linux",
   (130): "/bin/sh: can't access tty; job control turned off", "/ # ", "",
   (133): "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
   (150): "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
   (167): "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
   (184): "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
   }
}
}
```
