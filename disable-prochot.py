#!/usr/bin/env python3

import daemon
import glob
import lockfile
import os
import signal
import struct
import sys
import syslog
import time

PROCHOT_MSR = 0x1FC
NO_PROCHOT = 262236

# Borrowed code from https://github.com/andikleen/pmu-tools/blob/master/msr.py

def writemsr(msr, val):
    n = glob.glob('/dev/cpu/[0-9]*/msr')
    for c in n:
        f = os.open(c, os.O_WRONLY)
        os.lseek(f, msr, os.SEEK_SET)
        os.write(f, struct.pack('Q', val))
        os.close(f)
    if not n:
        raise OSError("msr module not loaded (run modprobe msr)")
    
def readmsr(msr, cpu = 0):
    f = os.open('/dev/cpu/%d/msr' % (cpu,), os.O_RDONLY)
    os.lseek(f, msr, os.SEEK_SET)
    val = struct.unpack('Q', os.read(f, 8))[0]
    os.close(f)
    return val

def main():
    syslog.syslog(syslog.LOG_INFO, "Started monitoring for BD_PROCHOT status.")
    while(1):
        rmsr = readmsr(PROCHOT_MSR)
        if rmsr != NO_PROCHOT:
            syslog.syslog(syslog.LOG_INFO, "BD_PROCHOT is on for some reason, status: {}. Resetting to {}.".format(rmsr, NO_PROCHOT))
            writemsr(PROCHOT_MSR, NO_PROCHOT)
        time.sleep(5)

def shutdown(signum, frame):
    syslog.syslog(syslog.LOG_INFO, "Stopped monitoring; shutdown signal received.")
    sys.exit(0)

with daemon.DaemonContext(
    pidfile=lockfile.FileLock('/var/run/disable-prochot.pid'),
    signal_map={
        signal.SIGTERM: shutdown,
        signal.SIGTSTP: shutdown
    },
    stderr=sys.stderr
):
    main()