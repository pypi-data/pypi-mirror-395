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

import hashlib
import hmac
import importlib
import json
import logging
import os
import pickle
import traceback
from types import SimpleNamespace
from typing import Any

import netmagus.form
import netmagus.rpc
import netmagus.screen


class StateFileSecurityError(Exception):
    """
    Exception raised when state file HMAC verification fails.

    This indicates the state file has been tampered with or corrupted
    and cannot be safely loaded.
    """

    pass


class NetMagusSession:
    """
    This class is a wrapper to handle an interactive session between the
    NetMagus backend and a user script.  It serves as a unifed API for user
    script operations to send/receive data with the NetMagus backend.  It
    also serves as a unified API for the NetMagus backend to call and execute
    user scripts.

    The NetMagus backend will call the module as (ex.):
        ``python -m netmagus --script user.py --token aBcDeF --input-file
        /some/path/to/aBcDeF.json --loglevel 10``

    The "token" is used by NM to desginate all file and RPC interactions tied
    to a given execution.

    This class will be called by the module's __main__.py to:
     - read JSON from the NetMagus backend via the input-file if it exists
     - read in any previous state tied to the token/session
     - import the user's script/module and execute it's run() method
        - run() method must receive a NetMagusSession object as only arg
        - run() method may return Form or (Form, anyobject)
     - receive a Form (and a state object) as a return from the user's
       run() method
     - store any state object and send JSON response back to NetMagus backend


     :meth:`._start` is used to initiate the execution of the user's code
     in the formula.

     The user's code can use various attributes and methods of this session
     object to interact with the NetMagus server and its UI.

     The following attributes exist within each session object:
     * :attr:`nm_input`:  holds the data entered by end-user on the NM ui
     * :attr:`session_data`: holds any state data from previous formula steps
     * :attr:`user_state`: deprecated alias for session_data (use session_data instead)

    """

    def __init__(self, token: str, input_file: str, loglevel: int, script: str) -> None:
        """
        The netmagus package's main method will parse the CLI args passed from
        the NetMagus backend and instantiate a new NetMagusSession object used
        to manage the connection and data passing to/from the NetMagus backend.

        :param token: a randomized token used to associate with a given
                      formula execution, provided from NM
        :type token: str
        :param input_file: the abs path to an input JSON file from NM backend
        :type input_file: str
        :param loglevel: a value from 0-5 indicating the log level to use
                         for the debugger passed from NM backend
        :type loglevel: int
        :param script: the name of the user python module to import and call
                       the run() entry point method
        :type script: str
        :returns: The next operation to be executed when this one completes
        :rtype: netmagus.netop.NetOpStep
        """
        # the NM "token" used to differntiate every commandPath execution
        self.token = token
        # the JSON file sent from NM back-end as input to this execution
        self.input_file = input_file
        # the logging level set in the NM UI formula admin screen
        self.loglevel = loglevel
        # the name of the Python module in the formula's directory
        self.script = script
        # the session logger setup when self._start() is called
        self.logger = logging.getLogger(__name__)
        # nm_input stores the JSON file input from NetMagus backend
        self.nm_input = None
        # session state data to be used by multiple screen.Screen objects
        # if they need to store/pass persistent data between multiple screens
        self.session_data = None
        # Convenience methods for user script writers
        self.rpc_connect = netmagus.rpc.rpc_connect
        self.rpc_disconnect = netmagus.rpc.rpc_disconnect
        self.rpc_form = netmagus.form.Form
        self.rpc_html = netmagus.rpc.Html
        self.netopstep = netmagus.form.Form  # for legacy <v0.6.0 compatability
        self.form = netmagus.form.Form
        self.textarea = netmagus.form.TextArea
        self.textinput = netmagus.form.TextInput
        self.radiobutton = netmagus.form.RadioButton
        self.passwordinput = netmagus.form.PasswordInput
        self.dropdownmenu = netmagus.form.DropDownMenu
        self.checkbox = netmagus.form.CheckBox
        self.filesupload = netmagus.form.FilesUpload
        self.filedownloadlink = netmagus.form.FileDownloadLink
        self.screens = SimpleNamespace()

    @property
    def user_state(self) -> Any:
        """
        Legacy alias for session_data. Use session_data instead.

        This property provides backwards compatibility for formulas written
        before v0.11.0 that used user_state to store persistent data.

        .. deprecated:: 0.11.0
           Use :attr:`session_data` instead

        :return: The session's persistent data
        """
        self.logger.debug(
            "Accessing deprecated 'user_state' attribute - use 'session_data' instead"
        )
        return self.session_data

    @user_state.setter
    def user_state(self, value: Any) -> None:
        """
        Legacy alias for session_data. Use session_data instead.

        :param value: The value to store in session data
        """
        self.logger.debug(
            "Setting deprecated 'user_state' attribute - use 'session_data' instead"
        )
        self.session_data = value

    def rpc_send(self, message: netmagus.form.Form | netmagus.rpc.Html) -> str:
        """
        Send a message to the NetMagus backend via WAMP to the session's RPC
        target.

        This is a convenience method to handle the token manipulation for the
        session. See :meth:`netmagus.rpc.rpc_send` method for full args
        """
        return netmagus.rpc.rpc_send(self.token, message)

    def rpc_receive(self) -> Any:
        """
        Retrieve a message via WAMP from the session's RPC target on the
        NetMagus backend service.

        This is a convenience method to handle the token manipulation for the
        session.  See :meth:`netmagus.rpc.rpc_receive` method for full args

        :returns: Any response message currently available at the RPC target
            for this session
        """
        return netmagus.rpc.rpc_receive(self.token)

    def rpc_form_query(
        self, message: netmagus.form.Form, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Send a message to the NetMagus backend via WAMP to the session's RPC
        target, then poll the target for response data.

        This is a convenience method to handle token manipulation for the
        session.  See :meth:`netmagus.rpc.rpc_form_query` for a full set of args

        :param message: an rpc.Message object to be sent to NetMagus backend
        :param kwargs: see rpc.rpc_form_query for full arg list
        :returns: the response messsage at the target RPC target for
            this session

        """
        return netmagus.rpc.rpc_form_query(self.token, message, **kwargs)

    def rpc_html_clear(self) -> None:
        """
        Send a message to the NM backend to clear the UI's HTML pop-up
        display area.
        """
        self.rpc_send(netmagus.rpc.Html(append=False))

    def _start(self) -> None:
        """
        Method to start the execution of user python module for the session

        :returns:  a JSON result file and a Shelve to store a user state object
        """
        self.logger.setLevel(self.loglevel)
        self.__read_response_file()
        self.__read_state_file()
        formula_return = self.__run_user_script()
        self.__write_response_file(formula_return)
        self.__write_state_file(self.session_data)

    def __run_user_script(self):
        """
        Used by the _start method to import and execute the user's Python module
        containing the formula logic

        :return: the netmagus.form.Form object returned by the user's module.
        """
        try:
            self.logger.debug(f"Attempting to import user module: {self.script}")
            user_module = importlib.import_module(self.script)
            self.logger.debug(f"User module imported: {user_module}")
            self.logger.debug("Attempting to execute user module run() method")
            formula_return = user_module.run(self)
            if isinstance(formula_return, netmagus.form.Form):
                self.logger.debug("User module returned a form only")
                self.__fix_formcomponent_indexes(formula_return)
                return formula_return
            # allow for old formula format <v0.6.0 with tuple
            elif isinstance(formula_return, tuple):
                if isinstance(formula_return[0], netmagus.form.Form):
                    self.__write_state_file(formula_return[1])
                    return formula_return[0]
            else:
                raise TypeError(
                    "Formula files should return a netmagus.form.Form object"
                )
        except ImportError:
            self.logger.exception(f"Unable to load user module {self.script}")
            raise
        except (OSError, Exception, NameError) as ex:
            self.logger.critical(
                f"Error calling run() method defined in the target file: {self.script}"
            )
            tb = traceback.format_exc()
            logging.exception(ex)
            htmlextrainfo = {
                "html": {
                    "printToUser": True,
                    "outputType": "html",
                    "title": "ERROR IN FORMULA",
                    "data": "<h3>This formula has encountered a critical error "
                    "and can not continue.  Please review the "
                    "traceback info and/or contact support for "
                    "assistance.</h3><br><br>Traceback info was: "
                    f"<pre>{tb}</pre>",
                }
            }
            next_step = netmagus.form.Form(
                currentStep=999,
                dataValid=False,
                extraInfo=htmlextrainfo,
                disableBackButton=True,
                finalStep=True,
            )
            return next_step

    def __read_response_file(self):
        """
        Read in the JSON response file from the NetMagus back-end.  These files
        are generated each time the NetMagus backend executes a commandPath to
        launch a task defined in a formula.  Examples would be when a user
        presses the SUBMIT button in the UI, a JSON file is generated by
        NetMagus and stored in a temp file to pass data to the Formula.
        """
        self.logger.debug("Reading JSON data from NetMagus request")
        try:
            with open(self.input_file) as data_file:
                self.nm_input = json.load(data_file)
            os.remove(self.input_file)  # remove file after reading it
        except OSError:
            self.logger.warning(f"Unable to access input JSON file {self.input_file}")
        except TypeError:
            self.logger.error(f"Unable to decode JSON data in {self.input_file}")

    def __derive_signing_key(self) -> bytes:
        """
        Derive a signing key from the session token.

        Uses SHA256 to derive a consistent key from the token for HMAC signing.

        :return: 32-byte signing key
        """
        return hashlib.sha256(self.token.encode("utf-8")).digest()

    def __compute_state_hmac(self, pickle_data: bytes) -> bytes:
        """
        Compute HMAC-SHA256 signature for pickle data.

        :param pickle_data: The pickled state data to sign
        :return: 32-byte HMAC signature
        """
        key = self.__derive_signing_key()
        return hmac.new(key, pickle_data, hashlib.sha256).digest()

    def __read_state_file(self):
        """
        This method will retrieve any previous state data saved during this
        formula execution and store it internally as self.session_data where it
        can be used throughout the formula execution and serve as a target
        for persistent data storage throughout the formula's multiple
        execution steps.

        State files must be HMAC-signed. Files with invalid signatures are
        rejected to prevent tampering.
        """
        state_file = self.input_file + "_State"
        try:
            with open(state_file, "rb") as picklefile:
                file_data = picklefile.read()

            # Verify minimum size: 32 bytes signature + at least some pickle data
            if len(file_data) < 33:
                raise StateFileSecurityError(
                    f"State file {state_file} is too small to be a valid signed state file"
                )

            # Parse signed file format: signature (32 bytes) + pickle data
            stored_signature = file_data[:32]
            pickle_data = file_data[32:]

            # Compute expected signature
            expected_signature = self.__compute_state_hmac(pickle_data)

            # Verify signature using constant-time comparison
            if not hmac.compare_digest(stored_signature, expected_signature):
                raise StateFileSecurityError(
                    f"State file {state_file} has invalid HMAC signature - "
                    "file may be corrupted or tampered with"
                )

            # Signature valid, unpickle the data
            self.session_data = pickle.loads(pickle_data)
            self.logger.debug(
                f"Verified signed formula state retrieved from {state_file}"
            )

        except pickle.UnpicklingError as exc:
            raise StateFileSecurityError(
                f"State file {state_file} has valid signature but contains "
                f"invalid pickle data: {exc}"
            )
        except OSError:
            self.logger.info(
                "No _State file found from previous formula "
                "execution steps. Setting state to NONE."
            )
            self.session_data = None

    def __write_response_file(self, response):
        """
        Store the returned Form into a Response file for NetMagus to read and
        process for execution of the next formula step
        """
        response_file = self.input_file + "Response"
        self.logger.debug(f"Target output JSON file will be: {response_file}")
        try:
            with open(response_file, "w") as outfile:
                outfile.write(str(response))
        except OSError:
            self.logger.error(
                f"Unable to open target JSON Response file: {response_file}"
            )
            raise

    def __write_state_file(self, stateobject):
        """
        Store the returned state object into a signed file for future operation
        steps to retrieve.  Formula creators can store an object in the
        sessions user_state attribute to have any object saved to disk and
        passed to the next formula execution step where it will be retrieved
        and stored in NetMagusSession.user_state for use by other formula code.

        The state file is protected with HMAC-SHA256 signature to detect tampering
        and has restricted file permissions (0o600) to prevent unauthorized access.
        """
        state_file = self.input_file + "_State"
        self.logger.debug(f"Target output state file will be: {state_file}")
        try:
            # Pickle the state object to bytes
            pickle_data = pickle.dumps(stateobject, protocol=-1)

            # Compute HMAC signature
            signature = self.__compute_state_hmac(pickle_data)

            # Write signature followed by pickle data
            with open(state_file, "wb") as picklefile:
                picklefile.write(signature)
                picklefile.write(pickle_data)

            # Set file permissions to owner read/write only
            os.chmod(state_file, 0o600)

            self.logger.debug(f"Signed formula state stored in {state_file}")
        except pickle.PickleError:
            self.logger.error("Error pickling state object")
            raise
        except OSError:
            self.logger.error(f"Unable to open target state file: {state_file}")
            raise

    @staticmethod
    def __fix_formcomponent_indexes(form_obj):
        """
        This method is a temporary fix to append an index attribute to each
        form component to be sent to NetMagus as JSON.  Eventually this will
        be done in the NetMagus back-end upon receipt according to the order
        of the list of form controls.  For now these are being added here in
        the same fashion before being sent to the NetMagus back-end.
        :param form_obj: a netmagus.NetOpStep object to be serialized and
        sent to NetMagus
        """
        # TODO: Manual index assignment workaround for NetMagus backend
        # The NetMagus Java backend should automatically assign form component
        # indexes based on list order, but currently requires them to be set
        # explicitly. Remove this loop once the backend handles indexing.
        # Tracked by: probert100's NetMagus backend fix
        index_counter = 0
        for item in form_obj.form:
            setattr(item, "index", index_counter)
            index_counter += 1

    def display_screen(
        self, screen: netmagus.screen.ScreenBase | Any
    ) -> netmagus.form.Form | None:
        """
        Render a :class:`netmagus.screen.ScreenBase` object to the NetMagus UI
        for this session.

        You may optionally also pass in a callable that returns a
        :class:`netmagus.screen.ScreenBase` object.
        The passed function will be called and if it returns a valid instance
        it will be used.

        :param screen: the screen to activate in the UI
        :type screen: netmagus.screen.ScreenBase
        :return: a final form to be shown at session completion
        :rtype: netmagus.form.Form
        """
        # validate type of screen
        if callable(screen):
            self.logger.debug(
                f"display_screen executing callable {screen} to generate Screen"
            )
            screen = screen()
        if not isinstance(screen, netmagus.screen.ScreenBase):
            raise TypeError("session.display argument is not a valid Screen object")
        self.logger.debug(f"displaying screen {screen}")
        # set the screen's session attribute to this session
        screen.session = self
        try:
            # reset flag each time screen is displayed
            screen.input_valid = False
            while not screen.input_valid:
                self.logger.debug("sending form to UI")
                response = screen.session.rpc_form_query(screen.form)
                screen.user_input = response["wellFormatedInput"]  # store user input
                # don't log actual user input since it may contain sensative
                # data that could be viewd in debug output or formula history
                # in the UI
                self.logger.debug(
                    f"{screen.__class__.__name__} user input received with length {len(screen.user_input)}"
                )
                screen.button_pressed = response.get("pressedButton")
                # handle the button press to apply next/back/cancel logic
                screen.process_button()
            # clear HTML pop-up screen once valid data received
            if screen.clear_html_popup:
                screen.session.rpc_html_clear()
            if screen.next_screen:
                self.logger.debug("Data validation passed, processing next screen")
                self.display_screen(screen.next_screen)
            else:
                self.logger.debug("No next_screen set, returning")
        except netmagus.screen.CancelButtonPressed:
            self.rpc_html_clear()
            screen.handle_cancel_button()
            raise
        except netmagus.screen.BackButtonPressed:
            screen.handle_back_button()
            self.display_screen(screen.back_screen)
