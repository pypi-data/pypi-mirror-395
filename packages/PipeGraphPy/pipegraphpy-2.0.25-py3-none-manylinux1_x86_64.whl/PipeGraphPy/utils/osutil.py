import psutil
import time

def get_disk_mbps(interval=1):
    disk_io_prev = psutil.disk_io_counters()
    time.sleep(interval)
    disk_io_now = psutil.disk_io_counters()
    bytes_read = disk_io_now.read_bytes - disk_io_prev.read_bytes
    bytes_written = disk_io_now.write_bytes - disk_io_prev.write_bytes
    mbps_read = bytes_read / interval / 1024 / 1024
    mbps_written = bytes_written / interval / 1024 / 1024
    mbps = mbps_read + mbps_written
    return int(mbps)


def get_cpu_usage():
    return psutil.cpu_percent()


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_disk_usage(path="/"):
    return psutil.disk_usage(path).percent


def get_load():
    return psutil.getloadavg()
