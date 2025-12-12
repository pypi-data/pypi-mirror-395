# Copyright (c) 2021-2024 Datalayer, Inc.
#
# Datalayer License

"""The Datalayer UI Server application."""

import os

# from tornado import ioloop

from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin

from datalayer_ui.handlers.index.handler import IndexHandler
from datalayer_ui.handlers.resource_usage.api_handler import ApiHandler
from datalayer_ui.handlers.resource_usage.runtime_handler import RuntimeUsageHandler
from datalayer_ui.handlers.resource_usage.config import ResourceUseDisplay
# from datalayer_ui.handlers.resource_usage.metrics import PSUtilMetricsLoader
# from datalayer_ui.handlers.resource_usage.prometheus import PrometheusHandler

from datalayer_ui._version import __version__


DEFAULT_STATIC_FILES_PATH = os.path.join(os.path.dirname(__file__), "./static")

DEFAULT_TEMPLATE_FILES_PATH = os.path.join(os.path.dirname(__file__), "./templates")


class DatalayerUIExtensionApp(ExtensionAppJinjaMixin, ExtensionApp):
    """The Datalayer UI Server extension."""

    name = "datalayer_ui"

    extension_url = "/datalayer_ui"

    load_other_extensions = True

    static_paths = [DEFAULT_STATIC_FILES_PATH]

    template_paths = [DEFAULT_TEMPLATE_FILES_PATH]


    def initialize_settings(self):
        resuseconfig = ResourceUseDisplay(parent=self.serverapp)
        self.serverapp.web_app.settings["jupyter_resource_usage_display_config"] = resuseconfig
        """
        if resuseconfig.enable_prometheus_metrics:
            callback = ioloop.PeriodicCallback(PrometheusHandler(PSUtilMetricsLoader(server_app)), 1000)
            callback.start()
        else:
            self.serverapp.log.info("Prometheus metrics reporting disabled in datalayer_ui.handlers.resource_usage.")
        """

    def initialize_templates(self):
#        self.serverapp.jinja_template_vars.update({"jupyter_ui_version" : __version__})
        pass

    def initialize_handlers(self):
        handlers = [
            ("/", IndexHandler),
            (self.name, IndexHandler),
            (url_path_join(self.name, "/metrics/v1"), ApiHandler),
            (url_path_join(self.name, "/metrics/v1/kernel_usage", r"get_usage/(.+)$"), RuntimeUsageHandler),
        ]
        self.handlers.extend(handlers)


# -----------------------------------------------------------------------------
# Main entry point
# -----------------------------------------------------------------------------

main = launch_new_instance = DatalayerUIExtensionApp.launch_instance
