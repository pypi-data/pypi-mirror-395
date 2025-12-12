import structlog.stdlib
import os
import os.path
import psutil
import typing as t
from psutil._common import bytes2human

logger = structlog.stdlib.get_logger("async_siril.system")


def human_readable_byte_size(num):
    """
    returns a human-readable representation of a raw number of bytes

    param num: how nay bytes ?
    :return: a human-readable representation of given bytes
    :rtype: str
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.3f %sB" % (num, unit)
        num /= 1024.0
    return "%.3f %sB" % (num, "Yi")


def available_memory():
    return psutil.virtual_memory().available


def memory_used():
    return bytes2human(psutil.Process().memory_info().rss)


def process_info():
    p = psutil.Process()
    info = {
        "pid": p.pid,
        "name": p.name(),
        "status": p.status(),
        "rss": bytes2human(psutil.Process().memory_info().rss),
    }
    return info


def container_aware_memory_limit_gb() -> t.Optional[str]:
    memory_limit_paths = [
        "/sys/fs/cgroup/memory/memory.limit_in_bytes",
        "/sys/fs/cgroup/memory/memory.low",
        "/sys/fs/cgroup/memory/memory.high",
        "/sys/fs/cgroup/memory/memory.max",
        "/sys/fs/cgroup/memory.low",
        "/sys/fs/cgroup/memory.high",
        "/sys/fs/cgroup/memory.max",
    ]

    for _file in memory_limit_paths:
        raw_result = read_int(_file)
        if raw_result is not None and raw_result > 0:
            logger.debug(f"found non-zero value in: {_file} - {raw_result}")
            gb_value = raw_result / 1024 / 1024 / 1024
            return "{:.2f}".format(gb_value)
    return None


def container_aware_cpu_limit() -> t.Optional[int]:
    # cgroup v1
    cgroup1_period_file = "/sys/fs/cgroup/cpu/cpu.cfs_period_us"
    cgroup1_quota_file = "/sys/fs/cgroup/cpu/cpu.cfs_quota_us"  # k8s cpu limit
    if os.path.exists(cgroup1_quota_file) and os.path.exists(cgroup1_period_file):
        logger.debug("found cgroup1 CPU limit")
        cpu_quota_us = read_int(cgroup1_quota_file)
        cpu_period_us = read_int(cgroup1_period_file)
        if cpu_quota_us is not None and cpu_period_us is not None:
            logger.debug(f"found cgroup1 CPU limit - quota: {cpu_quota_us}, period: {cpu_period_us}")
            return int(cpu_quota_us / cpu_period_us)
        else:
            logger.debug("no valid cgroup1 quota or period found")

    # cgroup v2
    cgroup2_file = "/sys/fs/cgroup/cpu.max"
    if os.path.exists(cgroup2_file):
        logger.debug("found cgroup1 memory limit")
        with open(cgroup2_file) as f:
            try:
                combined = f.readline()
                values = combined.split(" ")
                if len(values) >= 2:
                    cpu_quota_us = int(values[0])
                    cpu_period_us = int(values[1])
                    return int(cpu_quota_us / cpu_period_us)
            except ValueError as e:  # noqa: F841
                logger.debug("no valid cgroup2 quota or period found")
                pass
    return None


def read_int(_file) -> t.Optional[int]:
    if os.path.exists(_file):
        with open(_file) as f:
            try:
                return int(f.readline())
            except ValueError as e:  # noqa: F841
                pass
    return None
