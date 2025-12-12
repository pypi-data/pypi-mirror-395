"""
NetMagus Python Library
Copyright (C) 2016 Intelligent Visibility, Inc.
Richard Collins <richardc@intelligentvisibility.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import copy
import json
from typing import Any


class Form:
    """
    Form objects are sent to NetMagus back-end to be rendered in the UI.
    This controls the FormComponents seen on the screen, the behavior of
    buttons, and activities performed by the backend.
    """

    def __init__(
        self,
        name: str = "",
        commandPath: str = "",
        description: str = "",
        form: list["FormComponent"] | None = None,
        extraInfo: dict[str, Any] | None = None,
        currentStep: int = 1,
        dataValid: bool = True,
        buttonName: str = "",
        saveRecord: bool = True,
        dynamic: bool = False,
        autoProceed: bool = False,
        disableBackButton: bool = False,
        finalStep: bool = False,
    ) -> None:
        """
        A NetMagus forumla typically behaves as a "wizard" style user
        interaction.  Each "step" or "screen" in in the wizard is created
        using a JSON representation of the screen atributes and controls.
        This class allows a user to wrap numerous netmagus.form controls and
        control the user interaction, shell command exeuctions, and more.

        A JSON serialized repr of this object will control the individual
        screens and interactions of the NetMagus
        HTML UI.

        :param name: The name field is displayed at the top of the NetMagus
        UI screen as a typical HTML header
        :param commandPath: this is the full path of the shell command to be
        executed when a user presses NEXT or SUBMIT
        :param description: This may be text or html and will be rendered
        appropriately in the UI.  It is displayed
        below the name field.
        :param form: a list containing one or more netmagus.form objects to
        be drawn below the description in the UI
        :param extraInfo: optional dictionary to be rendered as additional
        JSON data to be used by UI to display extra HTML messages to the
        user.  It may also be used to pass data to UI to be received in
        future commandPath executuions.
        :param currentStep: integer representing the # of this operation in
        the overall wizard (i.e. 1 for first screen, 2 for 2nd, etc.)
        :param dataValid: boolean to indicate if the data received from
        NetMagus from the user's input was valid or not
        :param buttonName: string to control the name of the button displayed
        to users when using RPC based messages
        :param saveRecord: boolean to indicate if this screen/step should be
        saved in the UI history
        :param dynamic: boolean to specify if this screen contains controls
        with dynamic data that must be refreshed when a user presses the BACK
        button.  If True, commandPath is executed again when a user revisits
        the screen
        :param autoProceed: boolean to indicate if the UI should autoproceed
        from its current screen to this new one sent to the UI.  if False,
        user must manually press the PROCEED button to advance to the next
        screen/step
        :param disableBackButton: boolean to grey out the back button in the
        NetMagus UI for a given Form inside a forumula
        :param finalStep: boolean to indicate when a screen is the last/final
        screen in an operation.  This is used by NetMagus UI to understand
        when a task is finished and that it no longer needs to have its
        execution tracked by the execution engine
        """
        self.id = 0
        self.name = name
        self.description = description
        self.currentStep = currentStep
        self.commandPath = commandPath
        self.form = form or []
        self.extraInfo = extraInfo or {}
        self.dataValid = dataValid
        self.buttonName = buttonName
        self.saveRecord = saveRecord
        self.dynamic = dynamic
        self.autoProceed = autoProceed
        self.disableBackButton = disableBackButton
        self.finalStep = finalStep

    def __repr__(self) -> str:
        return json.dumps(self, sort_keys=True, default=lambda o: o.__dict__)

    @property
    def as_dict(self) -> dict[str, Any]:
        """
        return a dictionary representation of the Form object an all of its
        FormComponent objects inside the self.form attribute
        :return: dict(self) where self.form=list(dict(FormComponent))
        """
        return_dictionary = copy.copy(self.__dict__)
        return_dictionary["form"] = [
            component.as_dict_transformed for component in self.form
        ]
        return return_dictionary


class FormComponent:
    """
    Parent class for all valid types of form elements.  This should be
    subclassed for each new type of component created in NetMagus forms.
    This class is not intended for direct instantiation.

    The NetMagus app may choose to use or ignore values depending upon type
    of control.  The base class is set to provide all current attributes with
    a default value.  Sub-classes should over-ride defaults as necessary for
    each control type implemented.

    :param component:  Valid form component string value
    :param editable: Boolean to control if form component may be edited by user
    :param label: String rendered to left of the form component
    :param description: String rendered below the form component
    :param placeholder: String rendered inside the component before user
        inputs their own data
    :param options: List containing choices for checkboxes, dropdowns, etc.
    :param required: Boolean that controls if user must provide a value for
        this form component
    :param validation: String passed to NetMagus for certain component types
        to enforce user input validation validation examples: number=[number],
        email=[email], url=[url],  none=/.*/
    :param value: The value to be rendered inside the component

    """

    def __init__(
        self,
        component: str = "",
        editable: bool = True,
        label: str = "",
        description: str = "",
        placeholder: str = "",
        options: list[Any] | None = None,
        required: bool = False,
        validation: str = "/.*/",
        value: Any = None,
    ) -> None:
        # common attrs for all components
        self.component = component
        self.editable = editable
        self.index = 0
        self.id = self.index
        self.label = label
        self.description = description
        self.required = required
        if options is None:
            self.options = []
        else:
            self.options = options
        self.placeholder = placeholder
        self.validation = validation
        self.value = value

    def __repr__(self) -> str:
        return json.dumps(self, sort_keys=True, default=lambda o: o.__dict__)

    @property
    def as_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary view of the object and filters internal/private keys
        """
        return {k: v for k, v in self.__dict__.items() if k[0] != "_"}

    @property
    def as_dict_transformed(self) -> dict[str, Any]:
        """
        Returns self.as_dict with keys transformed to match those expected
        by the NetMagus java backend
        """
        keymap = {
            "options_left": "options",
            "options_right": "selectedoptions",
            "label_left": "optionslabel",
            "label_right": "selectedlabel",
        }
        result = {}
        for k, v in self.as_dict.items():
            if k in keymap.keys():
                result[keymap[k]] = v
            else:
                result[k] = v
        return result

    @property
    def to_json(self) -> str:
        """
        returns a JSON string representation of the object which is valid to pass to
        the NetMagus backend
        """
        return json.dumps(self.as_dict_transformed, sort_keys=True)


class TextArea(FormComponent):
    def __init__(
        self,
        editable: bool = True,
        label: str = "",
        description: str = "",
        placeholder: str = "",
        required: bool = False,
        value: str | None = None,
    ) -> None:
        super().__init__(
            component="textArea",
            editable=editable,
            label=label,
            description=description,
            required=required,
            placeholder=placeholder,
            value=value,
        )


class TextInput(FormComponent):
    def __init__(
        self,
        editable: bool = True,
        label: str = "",
        description: str = "",
        placeholder: str = "",
        required: bool = False,
        validation: str = "/.*/",
        value: str | None = None,
    ) -> None:
        super().__init__(
            component="textInput",
            editable=editable,
            label=label,
            description=description,
            required=required,
            placeholder=placeholder,
            validation=validation,
            value=value,
        )


class CheckBox(FormComponent):
    def __init__(
        self,
        editable: bool = True,
        label: str = "",
        description: str = "",
        options: list[str] | None = None,
        required: bool = False,
        value: str | list[str] | None = None,
    ) -> None:
        super().__init__(
            component="checkbox",
            editable=editable,
            label=label,
            description=description,
            options=options,
            required=required,
            value=value,
        )


class RadioButton(FormComponent):
    def __init__(
        self,
        editable: bool = True,
        label: str = "",
        description: str = "",
        options: list[str] | None = None,
        required: bool = False,
        value: str | None = None,
    ) -> None:
        super().__init__(
            component="radio",
            editable=editable,
            label=label,
            description=description,
            options=options,
            value=value,
            required=required,
        )


class DropDownMenu(FormComponent):
    def __init__(
        self,
        editable: bool = True,
        label: str = "",
        description: str = "",
        options: list[str] | None = None,
        value: str | None = None,
        required: bool = False,
    ) -> None:
        super().__init__(
            component="select",
            editable=editable,
            label=label,
            description=description,
            options=options,
            value=value,
            required=required,
        )


class PasswordInput(FormComponent):
    def __init__(
        self,
        editable: bool = True,
        label: str = "",
        description: str = "",
        placeholder: str = "",
        required: bool = False,
        value: str | None = None,
    ) -> None:
        super().__init__(
            component="password",
            editable=editable,
            label=label,
            description=description,
            required=required,
            placeholder=placeholder,
            value=value,
        )


class SelectDrop(FormComponent):
    def __init__(
        self,
        editable: bool = True,
        label: str = "",
        description: str = "",
        required: bool = False,
        label_left: str = "",
        label_right: str = "",
        options_left: list[Any] | None = None,
        options_right: list[Any] | None = None,
    ) -> None:
        super().__init__(
            component="selectdrop",
            editable=editable,
            label=label,
            description=description,
            required=required,
        )
        self.label_left = label_left
        self.label_right = label_right
        if options_left is not None:
            self.options_left = options_left
        else:
            self.options_left = []
        if options_right is not None:
            self.options_right = options_right
        else:
            self.options_right = []


class FilesUpload(FormComponent):
    """
    File upload component for selecting and uploading files.

    Uploaded files overwrite any existing files with the same path/filename.
    Formula developers should process and relocate uploaded files to different
    paths to preserve them and enable additional workflow screens.

    Args:
        label: Text displayed above the file upload control
        description: Text displayed below the file upload control
        buttonlabel: Text displayed on the button that triggers the file upload dialog
    """

    def __init__(
        self,
        label: str = "",  # label text above the control
        description: str = "",  # text under the control
        buttonlabel: str = "",  # label on the button to pop the file upload dialog
    ) -> None:
        super().__init__(
            component="filesUpload",
            label=label,
            description=description,
            placeholder=buttonlabel,
            required=False,
            validation="/.*/",
            value=None,
        )

    @property
    def buttonlabel(self) -> str:
        return self.placeholder

    @buttonlabel.setter
    def buttonlabel(self, value: str) -> None:
        self.placeholder = value


class FileDownloadLink(FormComponent):
    """
    Form component that renders a clickable download link in the NetMagus UI.
    The backend will serve the file specified by linkUrl when the link is clicked.
    """

    def __init__(
        self,
        label: str = "Download Link Label",
        description: str = "Download Link Description",
        linkUrl: str = "",
        linkText: str = "Download Link Text",
        message: str = "Download Link Message",
    ) -> None:
        """
        Create a file download link component.

        :param label: String rendered to left of the form component
        :param description: String rendered below the form component
        :param linkUrl: Relative or absolute file path to the downloadable file (e.g., 'foldername/filename.ext')
        :param linkText: Text displayed for the clickable link
        :param message: Additional message or tooltip text
        """
        super().__init__(
            component="fileDownloadLink",
            label=label,
            description=description,
        )
        # Custom attributes specific to file download links
        self.linkUrl = linkUrl
        self.linkText = linkText
        self.message = message
