#!/usr/bin/env python3

def dynamic_dataset():
    import subprocess, os
    from telnetlib import Telnet

    # Read the initramfs dataset
    initramfs = lib.getData("initramfs")
    initramfs_size = lib.getDims("initramfs")[0]
    with open(".initramfs", "wb") as f:
        f.write(bytes(initramfs[0:initramfs_size]))

    # Read the kernel dataset
    kernel = lib.getData("kernel")
    kernel_size = lib.getDims("kernel")[0]
    with open(".kernel", "wb") as f:
        f.write(bytes(kernel[0:kernel_size]))

    # Launch QEMU with a telnet-based console
    cmd = [
        "qemu-system-x86_64",
        "-nographic",
        "-enable-kvm",
        "-kernel", ".kernel",
        "-initrd", ".initramfs",
        "-monitor", "/dev/null",
        "-serial", "telnet:localhost:4321,server,wait",
    ]
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE)

    # Wait until the telnet service is up
    while True:
        try:
            tn = Telnet("localhost", 4321)
            break
        except ConnectionRefusedError:
            pass

    # Write each line retrieved from telnet to the console dataset
    line_nr = 0
    console = lib.getData("console")
    console_size = lib.getDims("console")[0]

    while line_nr < console_size:
        lines = tn.read_until(b"\r\n", 0.5)
        if len(lines) == 0:
            break
        for line in lines.split(b"\r\n"):
            # Skip early messages printed by QEMU
            if line_nr == 0 and not b"Linux version" in line:
                continue
            elif line.find(b"\033[2J") >= 0:
                line = line.split(b"\033[2J")[1]
            if len(line):
                lib.setString(console[line_nr], line)
                line_nr += 1

    p.terminate()
    os.unlink(".kernel")
    os.unlink(".initramfs")
