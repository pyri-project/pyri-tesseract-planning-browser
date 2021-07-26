from typing import List, Dict, Callable, Any
from pyri.webui_browser.plugins.panel import PyriWebUIBrowserPanelBase
from pyri.webui_browser import PyriWebUIBrowser
import importlib_resources
import js
import traceback
from RobotRaconteur.Client import *

class PyriVirtualPanel(PyriWebUIBrowserPanelBase):
    def __init__(self, device_manager, core):
        self.vue = None
        self.device_manager = device_manager
        self.core = core

    def init_vue(self,vue):
        self.vue = vue

    def refresh(self, *args):
        iframe = js.document.getElementById("tesseract_viewer_iframe")
        iframe.contentWindow.location.reload()

    def iframe_loaded(self, *args):
        pass

    def set_iframe_src(self, url = None):
        iframe = js.document.getElementById("tesseract_viewer_iframe")
        if url is not None:
            iframe.src = url
        else:

            #TODO: Assume tesseract viewer is at same hostname as server on port 8001

            hostname = js.window.location.hostname

            iframe.src = f"http://{hostname}:8001"

async def add_virtual_panel(panel_type: str, core: PyriWebUIBrowser, parent_element: Any):

    assert panel_type == "virtual"

    virtual_panel_html = importlib_resources.read_text(__package__,"virtual_panel.html")

    panel_config = {
        "type": "component",
        "componentName": "virtual",
        "componentState": {},
        "title": "Virtual",
        "id": "virtual",
        "isClosable": False
    }

    def register_virtual_panel(container, state):
        container.getElement().html(virtual_panel_html)

    core.layout.register_component("virtual", register_virtual_panel)

    core.layout.add_panel(panel_config)

    virtual_panel_obj = PyriVirtualPanel(core.device_manager, core)

    virtual_panel = js.Vue.new(js.python_to_js({
        "el": "#tesseract_virtual_panel",
        "data":
        {

        },
        "methods":
        {
            "refresh": virtual_panel_obj.refresh,
            "iframe_load": virtual_panel_obj.iframe_loaded
        }

    }))

    virtual_panel_obj.init_vue(virtual_panel)
    virtual_panel_obj.set_iframe_src()   
    
    return virtual_panel_obj
