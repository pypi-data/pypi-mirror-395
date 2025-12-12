import json

import pytest

from netmagus.form import (
    CheckBox,
    DropDownMenu,
    PasswordInput,
    RadioButton,
    TextArea,
    TextInput,
)
from netmagus.netop import NetOpStep


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,
# PyAttributeOutsideInit
# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,
# PyAttributeOutsideInit
# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit,
# PyAttributeOutsideInit
# noinspection PyAttributeOutsideInit
class TestNetMagusNetOp:
    @pytest.fixture(scope="class")
    def components(self):
        self.sample_netop = json.dumps(
            {
                "id": 0,
                "name": "My Network Operation",
                "commandPath": "python -u /tmp/myfile.py",
                "description": "My Description",
                "currentStep": 2,
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
                    {
                        "component": "password",
                        "editable": True,
                        "id": 0,
                        "index": 0,
                        "label": "Label 6",
                        "description": "Description 6",
                        "placeholder": "Placeholder 6",
                        "options": [],
                        "required": True,
                        "validation": "/.*/",
                        "value": None,
                    },
                ],
                "extraInfo": {
                    "hiddenData1": "Just Some data1",
                    "hiddenData2": {
                        "printToUser": True,
                        "outputType": "html",
                        "data": "Just Some data2",
                    },
                    "image1": {
                        "printToUser": True,
                        "outputType": "img",
                        "data": "img/image1.png",
                    },
                },
                "dataValid": False,
                "buttonName": "Next",
                "saveRecord": True,
                "dynamic": True,
                "autoProceed": True,
                "disableBackButton": True,
                "finalStep": True,
            },
            sort_keys=True,
        )

        self.extrainfo = {
            "hiddenData1": "Just Some data1",
            "hiddenData2": {
                "data": "Just Some data2",
                "outputType": "html",
                "printToUser": True,
            },
            "image1": {
                "printToUser": True,
                "outputType": "img",
                "data": "img/image1.png",
            },
        }

        self.textarea = TextArea(
            editable=True,
            label="Label 1",
            description="Description 1",
            placeholder="Placeholder 1",
            required=True,
        )
        self.textinput = TextInput(
            editable=True,
            label="Label 2",
            description="Description 2",
            placeholder="Placeholder 2",
            required=True,
            validation="[number]",
        )
        self.checkbox = CheckBox(
            editable=True,
            label="Label 3",
            description="Description 3",
            options=["Option1", "Option2"],
            required=True,
            value="Option1",
        )
        self.radiobutton = RadioButton(
            editable=True,
            label="Label 4",
            description="Description 4",
            options=["Option1", "Option2"],
            required=True,
            value="Option1",
        )
        self.dropdown = DropDownMenu(
            editable=True,
            label="Label 5",
            description="Description 5",
            options=["Option1", "Option2"],
            required=True,
            value="Option1",
        )
        self.password = PasswordInput(
            editable=True,
            label="Label 6",
            description="Description 6",
            placeholder="Placeholder 6",
            required=True,
        )
        self.form = [
            self.textarea,
            self.textinput,
            self.checkbox,
            self.radiobutton,
            self.dropdown,
            self.password,
        ]

        self.netopstep = NetOpStep(
            name="My Network Operation",
            commandPath="python -u /tmp/myfile.py",
            description="My Description",
            form=self.form,
            extraInfo=self.extrainfo,
            currentStep=2,
            dataValid=False,
            buttonName="Next",
            saveRecord=True,
            dynamic=True,
            autoProceed=True,
            disableBackButton=True,
            finalStep=True,
        )
        return self

    def test_netop_obj(self, components):
        assert components.sample_netop == repr(components.netopstep)
        assert (
            json.dumps(components.netopstep.as_dict, sort_keys=True)
            == components.sample_netop
        )
        assert repr(components.netopstep) == json.dumps(
            components.netopstep.as_dict, sort_keys=True
        )
