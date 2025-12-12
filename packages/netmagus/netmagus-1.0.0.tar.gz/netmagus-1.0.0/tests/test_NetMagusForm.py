import json

import pytest

from netmagus.form import (
    CheckBox,
    DropDownMenu,
    FileDownloadLink,
    FilesUpload,
    PasswordInput,
    RadioButton,
    SelectDrop,
    TextArea,
    TextInput,
)


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusFormTextArea:
    @pytest.fixture(scope="class")
    def components(self):
        self.ta = TextArea(
            editable=True,
            label="My Label",
            description="My Description",
            placeholder="My Placeholder",
            required=True,
        )
        # sample form element as created in the NetMagus Form Designer UI
        self.ta_fd = json.loads(
            '{"component": "textArea", "editable": true, "index": 0, "id": 0, '
            '"label": "My Label", '
            '"description": "My Description", "placeholder": "My Placeholder", '
            '"options": [], '
            '"required": true, "validation": "/.*/", "value": null}'
        )
        return self

    def test_textarea_obj(self, components):
        assert components.ta.__dict__ == components.ta_fd

    def test_textarea_json(self, components):
        assert components.ta.to_json == json.dumps(components.ta_fd, sort_keys=True)
        assert json.dumps(components.ta.as_dict, sort_keys=True) == json.dumps(
            components.ta_fd, sort_keys=True
        )


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusFormTextInput:
    @pytest.fixture(scope="class")
    def components(self):
        self.ti = TextInput(
            editable=True,
            label="My Label",
            description="My Description",
            placeholder="My Placeholder",
            required=True,
            validation="[number]",
        )
        # sample form element as created in the NetMagus Form Designer UI
        self.ti_fd = json.loads(
            '{"component":"textInput","editable":true,"index":0, "id": 0,'
            '"label":"My '
            'Label",'
            '"description":"My Description","placeholder":"My Placeholder",'
            '"options":[],'
            '"required":true,"validation":"[number]", "value": null}'
        )
        return self

    def test_textinput_json(self, components):
        assert components.ti.to_json == json.dumps(components.ti_fd, sort_keys=True)

    def test_textinput_obj(self, components):
        assert components.ti.__dict__ == components.ti_fd
        assert json.dumps(components.ti.as_dict, sort_keys=True) == json.dumps(
            components.ti_fd, sort_keys=True
        )


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusFormCheckbox:
    @pytest.fixture(scope="class")
    def components(self):
        self.cb = CheckBox(
            editable=True,
            label="My Label",
            description="My Description",
            options=["Option 1", "Option 2"],
            required=True,
            value="test",
        )

        self.cb_fd = json.loads(
            '{"component":"checkbox","editable":true,"index":0, "id": 0, "label":"My '
            'Label",'
            '"description":"My Description","placeholder":"","options":['
            '"Option 1","Option 2"],"required":true,"validation":"/.*/", '
            '"value":"test"}'
        )
        return self

    def test_checkbox_json(self, components):
        assert components.cb.to_json == json.dumps(components.cb_fd, sort_keys=True)

    def test_checkbox_obj(self, components):
        assert components.cb.__dict__ == components.cb_fd
        assert json.dumps(components.cb.as_dict, sort_keys=True) == json.dumps(
            components.cb_fd, sort_keys=True
        )


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusRadioButton:
    @pytest.fixture(scope="class")
    def components(self):
        self.rb = RadioButton(
            editable=True,
            label="My Label",
            description="My Description",
            options=["Option 1", "Option 2"],
            value="test",
        )

        self.rb_fd = json.loads(
            '{"component":"radio","editable":true,"index":0, "id":0, "label":"My '
            'Label",'
            '"description":"My Description","placeholder":"","options":['
            '"Option 1","Option 2"],"required":false,"validation":"/.*/", '
            '"value":"test"}'
        )
        return self

    def test_checkbox_json(self, components):
        assert components.rb.to_json == json.dumps(components.rb_fd, sort_keys=True)

    def test_checkbox_obj(self, components):
        assert components.rb.__dict__ == components.rb_fd
        assert json.dumps(components.rb.as_dict, sort_keys=True) == json.dumps(
            components.rb_fd, sort_keys=True
        )


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusDropDownMenu:
    @pytest.fixture(scope="class")
    def components(self):
        self.dd = DropDownMenu(
            editable=True,
            label="My Label",
            description="My Description",
            options=["Option 1", "Option 2"],
            value="test",
        )

        self.dd_fd = json.loads(
            '{"component":"select","description":"My '
            'Description","editable":true,"index":0, "id": 0,'
            '"label":"My Label","placeholder":"",'
            '"options":["Option 1","Option 2"],'
            '"required":false,"validation":"/.*/",'
            '"value":"test"}'
        )
        return self

    def test_dropdown_json(self, components):
        assert components.dd.to_json == json.dumps(components.dd_fd, sort_keys=True)
        assert json.dumps(components.dd.as_dict, sort_keys=True) == json.dumps(
            components.dd_fd, sort_keys=True
        )

    def test_dropdown_obj(self, components):
        assert components.dd.__dict__ == components.dd_fd


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusPasswordInput:
    @pytest.fixture(scope="class")
    def components(self):
        self.pi = PasswordInput(
            editable=True,
            label="My Label",
            description="My Description",
            placeholder="My Placeholder",
            required=True,
        )

        self.pi_fd = json.loads(
            '{"component":"password","editable":true,"index":0, "id": 0, "label":"My '
            'Label",'
            '"description":"My Description","placeholder":"My Placeholder",'
            '"options":[],'
            '"required":true,"validation":"/.*/", "value": null}'
        )
        return self

    def test_password_json(self, components):
        assert components.pi.to_json == json.dumps(components.pi_fd, sort_keys=True)
        assert json.dumps(components.pi.as_dict, sort_keys=True) == json.dumps(
            components.pi_fd, sort_keys=True
        )

    def test_password_obj(self, components):
        assert components.pi.__dict__ == components.pi_fd


class TestNetMagusSelectDrop:
    @pytest.fixture(scope="class")
    def components(self):
        self.sd = SelectDrop(
            editable=True,
            required=True,
            label="Select Drop Form Label",
            description="My Description",
            label_left="Available Options",
            options_left=["Option 1", 2],
            label_right="Selected Options",
            options_right=["Option 3", False],
        )
        self.sd_fd = json.loads(
            """
                {
                    "index": 0,
                    "component": "selectdrop",
                    "editable": true,
                    "index": 0,
                    "id": 0,
                    "label": "Select Drop Form Label",
                    "optionslabel": "Available Options",
                    "selectedlabel": "Selected Options",
                    "description": "My Description",
                    "options": ["Option 1",2],
                    "selectedoptions": ["Option 3", false],
                    "required": true,
                    "placeholder": "",
                    "value": null,
                    "validation": "/.*/"
                }
                """
        )
        return self

    def test_selectdrop_json(self, components):
        assert components.sd.to_json == json.dumps(components.sd_fd, sort_keys=True)
        assert json.dumps(
            components.sd.as_dict_transformed, sort_keys=True
        ) == json.dumps(components.sd_fd, sort_keys=True)

    def test_selectdrop_obj(self, components):
        assert components.sd.as_dict_transformed == components.sd_fd


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusFilesUpload:
    @pytest.fixture(scope="class")
    def components(self):
        self.fu = FilesUpload(
            label="Files Uploader",
            description="Upload multiple files",
            buttonlabel="Choose files",
        )
        # Expected JSON format for files upload component
        self.fu_fd = json.loads(
            '{"component":"filesUpload","editable":true,"index":0,"id":0,'
            '"label":"Files Uploader",'
            '"description":"Upload multiple files","placeholder":"Choose files",'
            '"options":[],'
            '"required":false,"validation":"/.*/","value":null}'
        )
        return self

    def test_filesupload_json(self, components):
        assert components.fu.to_json == json.dumps(components.fu_fd, sort_keys=True)
        assert json.dumps(components.fu.as_dict, sort_keys=True) == json.dumps(
            components.fu_fd, sort_keys=True
        )

    def test_filesupload_obj(self, components):
        assert components.fu.__dict__ == components.fu_fd


# noinspection PyAttributeOutsideInit,PyAttributeOutsideInit
class TestNetMagusFileDownloadLink:
    @pytest.fixture(scope="class")
    def components(self):
        self.fdl = FileDownloadLink(
            label="Download Link",
            description="Click to download results",
            linkUrl="output/results.csv",
            linkText="Download Results",
            message="Results Download Link",
        )
        # Expected JSON format for file download link component
        self.fdl_fd = json.loads(
            '{"component":"fileDownloadLink","editable":true,"index":0,"id":0,'
            '"label":"Download Link",'
            '"description":"Click to download results",'
            '"placeholder":"",'
            '"options":[],'
            '"required":false,"validation":"/.*/","value":null,'
            '"linkUrl":"output/results.csv","linkText":"Download Results",'
            '"message":"Results Download Link"}'
        )
        return self

    def test_filedownloadlink_json(self, components):
        assert components.fdl.to_json == json.dumps(components.fdl_fd, sort_keys=True)
        assert json.dumps(components.fdl.as_dict, sort_keys=True) == json.dumps(
            components.fdl_fd, sort_keys=True
        )

    def test_filedownloadlink_obj(self, components):
        assert components.fdl.__dict__ == components.fdl_fd
