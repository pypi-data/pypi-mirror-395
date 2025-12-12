# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

import json
import psutil

from concurrent.futures import ThreadPoolExecutor
from packaging import version

from tornado import web
from tornado.concurrent import run_on_executor

from jupyter_server.base.handlers import APIHandler

try:
    import ipykernel
    IPYKERNEL_VERSION = ipykernel.__version__
    USAGE_IS_SUPPORTED = version.parse("6.9.0") <= version.parse(IPYKERNEL_VERSION)
except ImportError:
    USAGE_IS_SUPPORTED = False
    IPYKERNEL_VERSION = None


class ApiHandler(APIHandler):

    EXECUTOR = ThreadPoolExecutor(max_workers=5)

    @run_on_executor
    def _get_cpu_percent(self, all_processes):
        def get_cpu_percent(p):
            try:
                return p.cpu_percent(interval=0.05)
            # Avoid littering logs with stack traces complaining
            # about dead processes having no CPU usage
            except:
                return 0
        return sum([get_cpu_percent(p) for p in all_processes])


    @web.authenticated
    async def get(self):
        """
        Calculate and return current resource usage metrics
        """
        config = self.settings["jupyter_resource_usage_display_config"]
        cur_process = psutil.Process()
        all_processes = [cur_process] + cur_process.children(recursive=True)
        # Get memory information
        rss = 0
        pss = None
        for p in all_processes:
            try:
                info = p.memory_full_info()
                if hasattr(info, "pss"):
                    pss = (pss or 0) + info.pss
                rss += info.rss
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                pass
        if callable(config.mem_limit):
            mem_limit = config.mem_limit(rss=rss, pss=pss)
        else:  # mem_limit is an Int
            mem_limit = config.mem_limit
        limits = {"memory": {"rss": mem_limit, "pss": mem_limit}}
        if config.mem_limit and config.mem_warning_threshold != 0:
            limits["memory"]["warn"] = (mem_limit - rss) < (
                mem_limit * config.mem_warning_threshold
            )
        metrics = {"rss": rss, "limits": limits}
        if pss is not None:
            metrics["pss"] = pss
        # Optionally get CPU information
        if config.track_cpu_percent:
            cpu_count = psutil.cpu_count()
            cpu_percent = await self._get_cpu_percent(all_processes)
            if config.cpu_limit != 0:
                limits["cpu"] = {"cpu": config.cpu_limit}
                if config.cpu_warning_threshold != 0:
                    limits["cpu"]["warn"] = (config.cpu_limit - cpu_percent) < (
                        config.cpu_limit * config.cpu_warning_threshold
                    )
            metrics.update(cpu_percent=cpu_percent, cpu_count=cpu_count)
        # Optionally get Disk information
        if config.track_disk_usage:
            try:
                disk_info = psutil.disk_usage(config.disk_path)
            except Exception:
                pass
            else:
                metrics.update(disk_used=disk_info.used, disk_total=disk_info.total)
                limits["disk"] = {"disk": disk_info.total}
                if config.disk_warning_threshold != 0:
                    limits["disk"]["warn"] = (disk_info.total - disk_info.used) < (
                        disk_info.total * config.disk_warning_threshold
                    )
        self.write(json.dumps(metrics))
