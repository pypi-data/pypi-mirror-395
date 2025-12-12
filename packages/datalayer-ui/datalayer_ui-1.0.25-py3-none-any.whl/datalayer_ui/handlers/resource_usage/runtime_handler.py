# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

import json
import zmq.asyncio

from inspect import isawaitable
from packaging import version

from tornado import web

from jupyter_client.jsonutil import date_default
from jupyter_server.base.handlers import APIHandler


try:
    import ipykernel
    IPYKERNEL_VERSION = ipykernel.__version__
    USAGE_IS_SUPPORTED = version.parse("6.9.0") <= version.parse(IPYKERNEL_VERSION)
except ImportError:
    USAGE_IS_SUPPORTED = False
    IPYKERNEL_VERSION = None


class RuntimeUsageHandler(APIHandler):

    @web.authenticated
    async def get(self, matched_part=None, *args, **kwargs):
        if not USAGE_IS_SUPPORTED:
            self.write(
                json.dumps(
                    {
                        "content": {
                            "reason": "not_supported",
                            "kernel_version": IPYKERNEL_VERSION,
                        }
                    }
                )
            )
            return
        config = self.settings["jupyter_resource_usage_display_config"]
        kernel_id = matched_part
        km = self.kernel_manager
        lkm = km.pinned_superclass.get_kernel(km, kernel_id)
        session = lkm.session
        client = lkm.client()
        control_channel = client.control_channel
        usage_request = session.msg("usage_request", {})
        control_channel.send(usage_request)
        poller = zmq.asyncio.Poller()
        control_socket = control_channel.socket
        poller.register(control_socket, zmq.POLLIN)
        timeout_ms = 10_000
        events = dict(await poller.poll(timeout_ms))
        if control_socket not in events:
            out = json.dumps(
                {
                    "content": {"reason": "timeout", "timeout_ms": timeout_ms},
                    "kernel_id": kernel_id,
                }
            )
        else:
            res = client.control_channel.get_msg(timeout=0)
            if isawaitable(res):
                # control_channel.get_msg may return a Future, depending on configured KernelManager class.
                res = await res
            if res:
                res["kernel_id"] = kernel_id
            res["content"].update({"host_usage_flag": config.show_host_usage})
            out = json.dumps(res, default=date_default)
        client.stop_channels()
        self.write(out)
