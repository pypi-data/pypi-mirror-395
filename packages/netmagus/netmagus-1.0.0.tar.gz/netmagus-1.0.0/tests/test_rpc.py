"""
Crossbar should not be running before running this test suite.  fixtures will
start/stop it as needed for various tests.
"""

import json
import logging
import os
import subprocess
import sys
from os import path
from time import sleep, time

import autobahn_sync
import pytest
from autobahn_sync.exceptions import (
    ApplicationError,
    ConnectionRefusedError,
)

from netmagus.form import CheckBox, DropDownMenu, Form, RadioButton, TextArea, TextInput
from netmagus.rpc import (
    Html,
    Message,
    RpcCallTimeout,
    rpc_connect,
    rpc_disconnect,
    rpc_form_query,
    rpc_send,
)


@pytest.fixture(scope="session")
def logger():
    """
    logger fixture used by all tests
    """
    return logging.getLogger(__name__)


@pytest.fixture(scope="module")
def components(request):
    """
    mock data components used for method validation
    """
    request.extrainfo = {
        "hiddenData1": "Just Some data1",
        "hiddenData2": {
            "printToUser": True,
            "outputType": "html",
            "data": "Just Some data2",
        },
        "image1": {"printToUser": True, "outputType": "img", "data": "img/image1.png"},
    }

    request.sample_form_message_dict = {
        "saveRecord": True,
        "name": "Test Form",
        "description": "Test Description",
        "buttonName": "Test Button",
        "extraInfo": request.extrainfo,
        "disableBackButton": True,
        "autoProceed": True,
        "currentStep": 2,
        "finalStep": False,
        "dataValid": False,
        "commandPath": "",
        "dynamic": False,
        "id": 0,
        "form": [
            {
                "component": "textArea",
                "editable": True,
                "index": 0,
                "id": 0,
                "label": "Label 1",
                "description": "Description 1",
                "placeholder": "Placeholder 1",
                "options": [],
                "required": True,
                "validation": "/.*/",
                "value": None,
            },
            {
                "component": "textInput",
                "editable": True,
                "index": 0,
                "id": 0,
                "label": "Label 2",
                "description": "Description 2",
                "placeholder": "Placeholder 2",
                "options": [],
                "required": True,
                "validation": "[number]",
                "value": None,
            },
            {
                "component": "checkbox",
                "editable": True,
                "index": 0,
                "id": 0,
                "label": "Label 3",
                "description": "Description 3",
                "placeholder": "",
                "options": ["Option1", "Option2"],
                "required": True,
                "validation": "/.*/",
                "value": "Option1",
            },
            {
                "component": "radio",
                "editable": True,
                "index": 0,
                "id": 0,
                "label": "Label 4",
                "description": "Description 4",
                "placeholder": "",
                "options": ["Option1", "Option2"],
                "required": True,
                "validation": "/.*/",
                "value": "Option1",
            },
            {
                "component": "select",
                "editable": True,
                "index": 0,
                "id": 0,
                "label": "Label 5",
                "description": "Description 5",
                "placeholder": "",
                "options": ["Option1", "Option2"],
                "required": True,
                "validation": "/.*/",
                "value": "Option1",
            },
        ],
    }

    request.sample_form_json = json.dumps(
        request.sample_form_message_dict, sort_keys=True
    )

    request.textarea = TextArea(
        editable=True,
        label="Label 1",
        description="Description 1",
        placeholder="Placeholder 1",
        required=True,
    )
    request.textinput = TextInput(
        editable=True,
        label="Label 2",
        description="Description 2",
        placeholder="Placeholder 2",
        required=True,
        validation="[number]",
    )
    request.checkbox = CheckBox(
        editable=True,
        label="Label 3",
        description="Description 3",
        options=["Option1", "Option2"],
        required=True,
        value="Option1",
    )
    request.radiobutton = RadioButton(
        editable=True,
        label="Label 4",
        description="Description 4",
        options=["Option1", "Option2"],
        required=True,
        value="Option1",
    )
    request.dropdown = DropDownMenu(
        editable=True,
        label="Label 5",
        description="Description 5",
        options=["Option1", "Option2"],
        required=True,
        value="Option1",
    )
    request.form = [
        request.textarea,
        request.textinput,
        request.checkbox,
        request.radiobutton,
        request.dropdown,
    ]

    request.rpcform = Form(
        name="Test Form",
        description="Test Description",
        buttonName="Test Button",
        extraInfo=request.extrainfo,
        disableBackButton=True,
        dataValid=False,
        finalStep=False,
        currentStep=2,
        autoProceed=True,
        form=[
            request.textarea,
            request.textinput,
            request.checkbox,
            request.radiobutton,
            request.dropdown,
        ],
    )

    request.emptyform = Form()

    request.sample_html_message_dict = {
        "printToUser": True,
        "outputType": "html",
        "append": True,
        "title": "Test Title",
        "data": "<p>Test html block</p>",
    }

    request.sample_html_json = json.dumps(
        request.sample_html_message_dict, sort_keys=True
    )

    request.htmlform = Html(title="Test Title", data="<p>Test html block</p>")

    request.sample_rpcmessage_html_json = json.dumps(
        {"messageType": "html", "message": request.sample_html_message_dict},
        sort_keys=True,
    )

    request.sample_rpcmessage_form_json = json.dumps(
        {"messageType": "netop", "message": request.sample_form_message_dict},
        sort_keys=True,
    )

    request.rpcmessage_html = Message(request.htmlform)
    request.rpcmessage_form = Message(request.rpcform)
    request.rpcmessage_emptyform = Message(request.emptyform)

    return request


class TestNetMagusRPCForm:
    """
    This class of tests verify the rpc.Form and rpc.Html data objects to ensure
    their JSON representations are as expected
    """

    def test_rpcform_json(self, components):
        assert (
            json.dumps(components.rpcform.as_dict, sort_keys=True)
            == components.sample_form_json
        )
        assert repr(components.rpcform) == json.dumps(
            components.rpcform.as_dict, sort_keys=True
        )

    def test_htmlform_json(self, components):
        assert (
            json.dumps(components.htmlform.as_dict, sort_keys=True)
            == components.sample_html_json
        )
        assert repr(components.htmlform) == str(components.htmlform.as_dict)

    def test_rpcmessages_json(self, components):
        assert (
            json.dumps(components.rpcmessage_html.as_dict, sort_keys=True)
            == components.sample_rpcmessage_html_json
        )
        assert (
            json.dumps(components.rpcmessage_form.as_dict, sort_keys=True)
            == components.sample_rpcmessage_form_json
        )
        assert repr(components.rpcmessage_form) == str(
            components.rpcmessage_form.as_dict
        )


class TestRPCMethodsWithoutCrossbar:
    """
    This class is for tests where we do NOT want the Crossbar.io backend running
    to respond to any tests
    """

    @pytest.fixture(autouse=True)
    def reset_autobahn_singleton(self):
        """
        Reset the autobahn_sync singleton state before and after each test
        to ensure test isolation. The singleton persists across tests and
        can cause AlreadyRunningError if not properly reset.
        """
        # Reset before test
        autobahn_sync.app._started = False
        autobahn_sync.app._session = None
        yield
        # Reset after test to clean up for subsequent tests
        autobahn_sync.app._started = False
        autobahn_sync.app._session = None

    def test_rpc_connect_failure(self):
        """
        Ensure that if Crossbar.io is not running, a proper exception is raised
        """
        with pytest.raises(ConnectionRefusedError):
            rpc_connect(url="ws://127.0.0.1:8088/ws", realm="netmagus")


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,
# PyAttributeOutsideInit
# noinspection PyAttributeOutsideInit
@pytest.mark.requires_crossbar
@pytest.mark.skipif(
    sys.version_info >= (3, 12),
    reason="crossbar not compatible with Python 3.12+",
)
class TestRPCMethodsWithCrossbar:
    """
    This class should hold any tests that require Crossbar.io to run
    """

    @pytest.fixture(scope="module")
    def crossbar(self, request):
        """make sure a crossbar router is reachable on default url/realm,
        if not start one up.  stop it upon teardown"""
        crossbar_conf_dir = path.abspath(path.dirname(__file__)) + "/.crossbar"
        print("crossbar setup")
        print("current path is: {}".format(os.environ["PATH"]))
        running = False

        self.userdata = None
        self.received_timestamp = None
        self.ack_timestamp = 0
        self.ack_userdata = None
        # Use the global autobahn_sync.app singleton so that rpc_connect/rpc_disconnect
        # work correctly with the same instance used for registering test RPC methods
        test_app = autobahn_sync.app

        @test_app.register("com.intelligentvisibility.a1b2c3.browser.sendform")
        def sendform(msg):
            """
            Register a fake rpc method similar to that used by NetMagus for
            clients to send data to be rendered.
            """
            self.userdata = msg
            self.received_timestamp = time()
            return "ok"

        @test_app.register("com.intelligentvisibility.a1b2c3.browser.getformresponse")
        def getformresponse():
            """
            Register a fake RPC method to simualte NetMagus responding to a
            client request for data after a user has entered it in the NetMagus
            UI.  only return data if it's been > 2 seconds since we received it
            to simulate processing time by user.  2 second time point allows to
            test cases where we do not wait long enough and get not data due to
            timeout, cases where we wait till end of our client-side timeout and
            raise exception on client side to handle or retry, and cases where
            we block forever with no timeout and the data finally returns at 2s.
            """
            if time() >= self.received_timestamp + 1:
                return self.userdata
            else:
                return False

        @test_app.register("com.intelligentvisibility.a1b2c3.browser.displaymessage")
        def displaymessage(msg):
            """
            Register a fake RPC method to receive Html update messages
            """
            self.userdata = msg
            self.received_timestamp = time()
            return "ok"

        @test_app.register("com.intelligentvisibility.d4e5f6.browser.sendform")
        def no_valid_ui_target(test_app):
            """
            Simulate case where NM backend is online with valid reg, but
            browser UI has not registered its corresponding method yet. In this
            case today NM passes on the exception to us and we should see it.
            """
            return autobahn_sync.call(
                "com.intelligentvisibility.d4e5f6.ui.browser.sendform"
            )

        @test_app.register("com.intelligentvisibility.123456.browser.sendform")
        def sendform_ack_test(msg):
            """
            Register a fake rpc method similar to that used by NetMagus for
            clients to send data to be rendered.  This endpoint should simulate
            case where backend is not responding for a period to the request and
            will induce retry behavior in the rpc_send method
            """
            self.userdata = msg
            self.received_timestamp = time()
            if self.ack_timestamp == 0:
                self.ack_timestamp = time()
            # only return ACK if it's been 1 second since the request to
            # this method
            if time() >= self.ack_timestamp + 1:
                self.ack_timestamp = 0
                return "ok"

        @test_app.register("com.intelligentvisibility.123456.browser.getformresponse")
        def getformresponse_ack_test():
            """
            Register a fake RPC method to simualte NetMagus responding to a
            client request for data after a user has entered it in the NetMagus
            UI.  only return data if it's been > 2 seconds since we received it
            to simulate processing time by user.  2 second time point allows to
            test cases where we do not wait long enough and get not data due to
            timeout, cases where we wait till end of our client-side timeout and
            raise exception on client side to handle or retry, and cases where
            we block forever with no timeout and the data finally returns at 2s.
            """
            if time() >= self.received_timestamp + 1:
                return self.userdata
            else:
                return False

        # start up the crossbar service
        for _ in range(20):
            sleep(1)
            try:
                test_app.run(url="ws://127.0.0.1:8088/ws", realm="netmagus")
            except ConnectionRefusedError:
                subprocess.Popen(
                    ["uv", "run", "crossbar", "start", "--cbdir", crossbar_conf_dir]
                )
                continue
            else:
                running = True
                break
        if not running:
            raise RuntimeError("Couldn't connect to crossbar router")

        def finalizer():
            """
            tear down Crossbar.io when we are done
            """
            print("crossbar teardown")
            rpc_disconnect()
            p = subprocess.Popen(["crossbar", "stop", "--cbdir", crossbar_conf_dir])
            p.wait()

        request.addfinalizer(finalizer)
        return self

    def test_rpc_connect_success(self, crossbar):
        """
        verify that when crossbar is online, we can connect to it.
        The crossbar fixture already establishes the connection using the
        global autobahn_sync.app singleton, so we verify it's connected.
        """
        assert autobahn_sync.app._started is True

    def test_formquery_failure_message_html(self, crossbar, components):
        """
        when crossbar.io is not online, verify we get a proper exception raised
        """
        with pytest.raises(TypeError):
            rpc_form_query("a1b2c3", components.htmlform, poll=0.5, timeout=5)

    def test_formquery_success_message_form(self, crossbar, components):
        """
        send rpc.Form to mock RPC method via Crossbar, wait for up to 5s, mock
        method will return back the data sent to it after 2s delay
        """
        assert (
            rpc_form_query("a1b2c3", components.rpcform, poll=0.5, timeout=5)
            == components.rpcmessage_form.as_dict
        )

    def test_formquery_success_emptyform(self, crossbar, components):
        """
        send rpc.Form to mock RPC method via Crossbar, wait for up to 5s, mock
        method will return back the data sent to it after 2s delay
        """
        assert (
            rpc_form_query("a1b2c3", components.emptyform, poll=0.5, timeout=5)
            == components.rpcmessage_emptyform.as_dict
        )

    def test_formquery_failure_dictd(self, crossbar, components):
        """
        Verify we raise proper exception for unexpected data types
        Only Form and Html objects should be allowed as inputs
        """
        with pytest.raises(TypeError):
            rpc_form_query("a1b2c3", dict(x=1, y="123"), poll=0.5, timeout=5)

    def test_rpc_send_failure_dictd(self, crossbar, components):
        """
        only Form and Html objects should be allowed as inputs
        """
        with pytest.raises(TypeError):
            rpc_send("a1b2c3", dict(x=1, y="123"))

    def test_formquery_timeout(self, crossbar, components):
        """
        mock RPC method won't return data until 2s delay.  Verify we get proper
        exception raise when our self-imposed timout is exceeded before
        receiving a response
        """
        with pytest.raises(RpcCallTimeout):
            assert (
                rpc_form_query("a1b2c3", components.rpcform, poll=0.5, timeout=1)
                == components.rpcmessage_form
            )

    def test_formquery_timeout_disabled(self, crossbar, components):
        """
        rpc target will return False if there is no return value from the call.
        for browser.getformresponse this will mean no user has completed the
        last form sent to the UI yet.
        If have zero timeout, we will send and immediately check for response
        and no data will be available yet resulting in None as final return
        """
        assert (
            rpc_form_query("a1b2c3", components.rpcform, poll=0.5, timeout=0) is False
        )

    def test_formquery_timeout_forever(self, crossbar, components):
        """
        Block call forever and response should be returned at 2s delay
        """
        assert (
            rpc_form_query("a1b2c3", components.rpcform, poll=0.5, timeout=-1)
            == components.rpcmessage_form.as_dict
        )

    def test_formquery_invalid_target(self, crossbar, components):
        """
        If we call an invalid RPC target, verify proper exception is raised
        """
        with pytest.raises(ApplicationError):
            assert (
                rpc_form_query("xyz", components.rpcform, poll=0.5, timeout=2) == "asdf"
            )

    def test_rpc_displaymessage(self, crossbar, components):
        """
        When we send an RPC HTML message, the response back is "ok" from
        NetMagus backend.
        """
        assert rpc_send("a1b2c3", components.htmlform) == "ok"
        assert crossbar.userdata == components.rpcmessage_html.as_dict

    def test_invalid_ui_browser_method(self, crossbar, components):
        """
        Test case where object is sent to NM backend, but browser ui has not
        registered its RPC method yet and we receive exception
        """
        with pytest.raises(ApplicationError):
            assert (
                rpc_send("d4e5f6", components.rpcform)
                == components.rpcmessage_form.as_dict
            )

    def test_formquery_slow_ack(self, crossbar, components):
        """
        test the case where NM backend doesn't ACK our transmission until 1
        second, causing rpc_send to retransmit
        """
        assert (
            rpc_form_query("123456", components.rpcform, poll=0.5, timeout=-1)
            == components.rpcmessage_form.as_dict
        )

    def test_output_json_examples(self, crossbar, components):
        print(json.dumps(components.rpcmessage_form.as_dict))
        print(json.dumps(components.rpcmessage_html.as_dict))
