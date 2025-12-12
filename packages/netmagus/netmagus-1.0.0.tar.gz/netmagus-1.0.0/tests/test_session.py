"""
Tests for netmagus.session module

Tests cover NetMagusSession initialization, RPC methods, file operations,
script execution, and screen display workflow.
"""

import hashlib
import hmac
import json
import os
import pickle
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from netmagus.form import Form, TextInput
from netmagus.rpc import Html
from netmagus.screen import CancelButtonPressed, ScreenBase
from netmagus.session import NetMagusSession, StateFileSecurityError


class MockScreen(ScreenBase):
    """Concrete Screen implementation for testing"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validation_passes = True

    def generate_form(self):
        return Form(name="Test", form=[TextInput(label="input")])

    def validate_user_input(self):
        return self.validation_passes

    def process_user_input(self):
        pass

    def return_error_message(self):
        pass

    def handle_cancel_button(self):
        pass

    def handle_back_button(self):
        pass


class TestNetMagusSessionInit:
    """Test NetMagusSession initialization"""

    def test_init_sets_all_attributes(self):
        """Test that __init__ sets all expected attributes"""
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        assert session.token == "test_token"
        assert session.input_file == "/tmp/test.json"
        assert session.loglevel == 10
        assert session.script == "test_script"
        assert session.nm_input is None
        assert session.session_data is None
        assert session.user_state is None

    def test_init_sets_convenience_methods(self):
        """Test that convenience method references are set"""
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        # Verify convenience references exist
        assert session.rpc_connect is not None
        assert session.rpc_disconnect is not None
        assert session.rpc_form is not None
        assert session.rpc_html is not None
        assert session.form is not None
        assert session.textarea is not None
        assert session.textinput is not None
        assert session.radiobutton is not None
        assert session.passwordinput is not None
        assert session.dropdownmenu is not None
        assert session.checkbox is not None

    def test_init_creates_screens_namespace(self):
        """Test that screens SimpleNamespace is created"""
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        from types import SimpleNamespace

        assert isinstance(session.screens, SimpleNamespace)

    def test_user_state_property_aliases_session_data(self):
        """Test user_state property is a true alias for session_data"""
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        # Initially both are None
        assert session.session_data is None
        assert session.user_state is None

        # Setting via session_data updates user_state
        test_data = {"key": "value", "count": 42}
        session.session_data = test_data
        assert session.user_state is test_data
        assert session.user_state == test_data

        # Setting via user_state updates session_data
        new_data = {"different": "data"}
        session.user_state = new_data
        assert session.session_data is new_data
        assert session.session_data == new_data

        # Both refer to the same object
        session.session_data["added"] = "key"
        assert "added" in session.user_state
        assert session.user_state["added"] == "key"


class TestNetMagusSessionRPCMethods:
    """Test RPC wrapper convenience methods"""

    @patch("netmagus.rpc.rpc_send")
    def test_rpc_send_calls_with_token(self, mock_rpc_send):
        """Test rpc_send passes token to netmagus.rpc.rpc_send"""
        mock_rpc_send.return_value = "ok"
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )
        test_form = Form(name="Test")

        result = session.rpc_send(test_form)

        mock_rpc_send.assert_called_once_with("test_token", test_form)
        assert result == "ok"

    @patch("netmagus.rpc.rpc_receive")
    def test_rpc_receive_calls_with_token(self, mock_rpc_receive):
        """Test rpc_receive passes token to netmagus.rpc.rpc_receive"""
        mock_rpc_receive.return_value = {"data": "test"}
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        result = session.rpc_receive()

        mock_rpc_receive.assert_called_once_with("test_token")
        assert result == {"data": "test"}

    @patch("netmagus.rpc.rpc_form_query")
    def test_rpc_form_query_calls_with_token(self, mock_rpc_form_query):
        """Test rpc_form_query passes token and kwargs"""
        mock_rpc_form_query.return_value = {"wellFormatedInput": {}}
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )
        test_form = Form(name="Test")

        result = session.rpc_form_query(test_form, poll=0.5, timeout=10)

        mock_rpc_form_query.assert_called_once_with(
            "test_token", test_form, poll=0.5, timeout=10
        )
        assert result == {"wellFormatedInput": {}}

    @patch("netmagus.rpc.rpc_send")
    def test_rpc_html_clear_sends_html_with_append_false(self, mock_rpc_send):
        """Test rpc_html_clear sends Html with append=False"""
        mock_rpc_send.return_value = "ok"
        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        session.rpc_html_clear()

        # Verify rpc_send was called
        assert mock_rpc_send.called
        # Get the Html object that was passed
        html_arg = mock_rpc_send.call_args[0][1]
        assert isinstance(html_arg, Html)
        assert html_arg.append is False


class TestNetMagusSessionFileOperations:
    """Test file I/O operations using temporary files"""

    def test_read_response_file_loads_json(self, tmp_path):
        """Test __read_response_file reads and parses JSON"""
        # Create a temporary JSON file
        test_file = tmp_path / "test_input.json"
        test_data = {"test": "data", "value": 123}
        test_file.write_text(json.dumps(test_data))

        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        # Call the private method (note: this is internal testing)
        session._NetMagusSession__read_response_file()

        assert session.nm_input == test_data
        assert not test_file.exists()  # File should be deleted

    def test_read_response_file_handles_missing_file(self, tmp_path):
        """Test __read_response_file handles missing file gracefully"""
        test_file = tmp_path / "nonexistent.json"

        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        # Should not raise exception
        session._NetMagusSession__read_response_file()
        assert session.nm_input is None

    def test_write_response_file_writes_json(self, tmp_path):
        """Test __write_response_file writes Form as JSON"""
        test_file = tmp_path / "test_input.json"
        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        test_form = Form(name="Test Form", description="Test")
        response_file = Path(str(test_file) + "Response")

        session._NetMagusSession__write_response_file(test_form)

        assert response_file.exists()
        # The file should contain the string representation of the form
        content = response_file.read_text()
        assert "Test Form" in content

    def test_read_state_file_loads_signed_state(self, tmp_path):
        """Test __read_state_file loads signed pickled state"""
        test_file = tmp_path / "test_input.json"
        test_state = {"session_data": "test", "count": 42}

        # Create session to write signed state
        session1 = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )
        session1._NetMagusSession__write_state_file(test_state)

        # Create new session to read the state
        session2 = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )
        session2._NetMagusSession__read_state_file()

        # session_data is loaded from the state file
        assert session2.session_data == test_state
        # user_state property returns the same value
        assert session2.user_state == test_state
        assert session2.user_state is session2.session_data

    def test_read_state_file_handles_missing_file(self, tmp_path):
        """Test __read_state_file handles missing file"""
        test_file = tmp_path / "test_input.json"

        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        session._NetMagusSession__read_state_file()

        assert session.user_state is None

    def test_write_state_file_pickles_state(self, tmp_path):
        """Test __write_state_file pickles state object"""
        test_file = tmp_path / "test_input.json"
        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        test_state = {"data": "test", "values": [1, 2, 3]}
        state_file = Path(str(test_file) + "_State")

        session._NetMagusSession__write_state_file(test_state)

        assert state_file.exists()
        # File is now signed, so load it properly (skip signature)
        with open(state_file, "rb") as f:
            file_data = f.read()
        # Skip 32-byte signature and load pickle data
        pickle_data = file_data[32:]
        loaded_state = pickle.loads(pickle_data)
        assert loaded_state == test_state

    def test_write_state_file_creates_signed_file(self, tmp_path):
        """Test __write_state_file creates HMAC-signed state file"""
        test_file = tmp_path / "test_input.json"
        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        test_state = {"data": "test", "signed": True}
        state_file = Path(str(test_file) + "_State")

        session._NetMagusSession__write_state_file(test_state)

        assert state_file.exists()

        # Read the file and verify format: signature (32 bytes) + pickle data
        with open(state_file, "rb") as f:
            file_data = f.read()

        assert len(file_data) > 32
        signature = file_data[:32]
        pickle_data = file_data[32:]

        # Verify the signature is correct
        key = hashlib.sha256(session.token.encode("utf-8")).digest()
        expected_signature = hmac.new(key, pickle_data, hashlib.sha256).digest()
        assert hmac.compare_digest(signature, expected_signature)

        # Verify the pickle data is correct
        loaded_state = pickle.loads(pickle_data)
        assert loaded_state == test_state

    def test_write_state_file_sets_permissions(self, tmp_path):
        """Test __write_state_file sets file permissions to 0o600"""
        test_file = tmp_path / "test_input.json"
        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        test_state = {"data": "test"}
        state_file = Path(str(test_file) + "_State")

        session._NetMagusSession__write_state_file(test_state)

        # Check file permissions (owner read/write only)
        file_mode = os.stat(state_file).st_mode & 0o777
        assert file_mode == 0o600

    def test_read_state_file_verifies_signed_file(self, tmp_path):
        """Test __read_state_file verifies and loads signed state file"""
        test_file = tmp_path / "test_input.json"
        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        # Create a signed state file
        test_state = {"data": "secure", "verified": True}

        # Write signed state
        session._NetMagusSession__write_state_file(test_state)

        # Create new session to read the state
        session2 = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        session2._NetMagusSession__read_state_file()

        assert session2.session_data == test_state

    def test_read_state_file_rejects_tampered_file(self, tmp_path):
        """Test __read_state_file raises error for tampered signed file"""
        test_file = tmp_path / "test_input.json"
        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        # Create a signed state file
        test_state = {"data": "original"}
        state_file = Path(str(test_file) + "_State")
        session._NetMagusSession__write_state_file(test_state)

        # Tamper with the file (modify pickle data but keep signature)
        with open(state_file, "rb") as f:
            file_data = f.read()

        signature = file_data[:32]
        # Create different pickle data
        tampered_data = pickle.dumps({"data": "tampered"}, protocol=-1)

        # Write back: original signature + tampered pickle data
        with open(state_file, "wb") as f:
            f.write(signature)
            f.write(tampered_data)

        # Create new session to read the tampered state
        session2 = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        # Should raise StateFileSecurityError because HMAC verification fails
        with pytest.raises(StateFileSecurityError):
            session2._NetMagusSession__read_state_file()

    def test_read_state_file_rejects_unsigned_file(self, tmp_path):
        """Test __read_state_file rejects unsigned pickle files"""
        test_file = tmp_path / "test_input.json"
        state_file = Path(str(test_file) + "_State")

        # Create an unsigned pickled state file (old format)
        test_state = {"unsigned": True}
        with open(state_file, "wb") as f:
            pickle.dump(test_state, f, protocol=-1)

        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        # Should raise StateFileSecurityError (invalid signature)
        with pytest.raises(StateFileSecurityError):
            session._NetMagusSession__read_state_file()

    def test_read_state_file_rejects_invalid_signature_and_invalid_pickle(
        self, tmp_path
    ):
        """Test __read_state_file raises StateFileSecurityError for corrupt files"""
        test_file = tmp_path / "test_input.json"
        state_file = Path(str(test_file) + "_State")

        # Write a file with invalid signature and invalid pickle data
        with open(state_file, "wb") as f:
            f.write(b"X" * 32)  # Invalid signature
            f.write(b"not a pickle")  # Invalid pickle data

        session = NetMagusSession(
            token="test_token",
            input_file=str(test_file),
            loglevel=10,
            script="test_script",
        )

        # Should raise StateFileSecurityError
        with pytest.raises(StateFileSecurityError):
            session._NetMagusSession__read_state_file()


class TestNetMagusSessionScriptExecution:
    """Test user script loading and execution"""

    @patch("netmagus.session.importlib.import_module")
    def test_run_user_script_imports_and_executes(self, mock_import):
        """Test __run_user_script imports module and calls run()"""
        # Create a mock module with a run function
        mock_module = Mock()
        mock_form = Form(name="Result")
        mock_module.run.return_value = mock_form
        mock_import.return_value = mock_module

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        result = session._NetMagusSession__run_user_script()

        mock_import.assert_called_once_with("test_script")
        mock_module.run.assert_called_once_with(session)
        assert result == mock_form

    @patch("netmagus.session.importlib.import_module")
    def test_run_user_script_handles_tuple_return(self, mock_import):
        """Test __run_user_script handles tuple (Form, state) for backward compatibility"""
        mock_module = Mock()
        mock_form = Form(name="Result")
        mock_state = {"data": "state"}
        mock_module.run.return_value = (mock_form, mock_state)
        mock_import.return_value = mock_module

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        # Mock the write_state_file method
        with patch.object(
            session, "_NetMagusSession__write_state_file"
        ) as mock_write_state:
            result = session._NetMagusSession__run_user_script()

            mock_write_state.assert_called_once_with(mock_state)
            assert result == mock_form

    @patch("netmagus.session.importlib.import_module")
    def test_run_user_script_handles_import_error(self, mock_import):
        """Test __run_user_script handles ImportError"""
        mock_import.side_effect = ImportError("Module not found")

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        with pytest.raises(ImportError):
            session._NetMagusSession__run_user_script()

    @patch("netmagus.session.importlib.import_module")
    def test_run_user_script_handles_execution_error(self, mock_import):
        """Test __run_user_script returns error form on execution failure"""
        mock_module = Mock()
        mock_module.run.side_effect = RuntimeError("Script failed")
        mock_import.return_value = mock_module

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        result = session._NetMagusSession__run_user_script()

        # Should return an error form
        assert isinstance(result, Form)
        assert result.finalStep is True
        assert result.dataValid is False
        assert "html" in result.extraInfo


class TestNetMagusSessionDisplayScreen:
    """Test display_screen workflow"""

    @patch("netmagus.session.netmagus.rpc.rpc_send")
    @patch("netmagus.session.netmagus.rpc.rpc_form_query")
    def test_display_screen_sets_screen_session(self, mock_rpc_query, mock_rpc_send):
        """Test display_screen sets screen.session"""
        mock_rpc_send.return_value = "ok"
        mock_rpc_query.return_value = {
            "wellFormatedInput": {"input": "test"},
            "pressedButton": "next",
        }

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        screen = MockScreen()
        screen.validation_passes = True

        session.display_screen(screen)

        assert screen.session is session

    @patch("netmagus.session.netmagus.rpc.rpc_send")
    @patch("netmagus.session.netmagus.rpc.rpc_form_query")
    def test_display_screen_executes_callable(self, mock_rpc_query, mock_rpc_send):
        """Test display_screen executes callable to get screen"""
        mock_rpc_send.return_value = "ok"
        mock_rpc_query.return_value = {
            "wellFormatedInput": {"input": "test"},
            "pressedButton": "next",
        }

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        # Use a callable that returns a screen
        screen_callable_called = []

        def screen_callable():
            screen_callable_called.append(True)
            screen = MockScreen()
            screen.validation_passes = True
            return screen

        session.display_screen(screen_callable)

        assert screen_callable_called == [True]

    @patch("netmagus.session.netmagus.rpc.rpc_send")
    @patch("netmagus.session.netmagus.rpc.rpc_form_query")
    def test_display_screen_loops_until_valid_input(
        self, mock_rpc_query, mock_rpc_send
    ):
        """Test display_screen loops until input is valid"""
        mock_rpc_send.return_value = "ok"
        # Return invalid twice, then valid
        mock_rpc_query.side_effect = [
            {"wellFormatedInput": {}, "pressedButton": "next"},
            {"wellFormatedInput": {}, "pressedButton": "next"},
            {"wellFormatedInput": {"input": "valid"}, "pressedButton": "next"},
        ]

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        screen = MockScreen()
        validation_attempts = []

        def validate():
            validation_attempts.append(True)
            return len(validation_attempts) >= 3

        screen.validate_user_input = validate

        session.display_screen(screen)

        assert len(validation_attempts) == 3
        assert mock_rpc_query.call_count == 3

    @patch("netmagus.rpc.rpc_form_query")
    @patch("netmagus.rpc.rpc_send")
    def test_display_screen_clears_html_after_valid_input(
        self, mock_rpc_send, mock_rpc_query
    ):
        """Test display_screen clears HTML popup after valid input"""
        mock_rpc_query.return_value = {
            "wellFormatedInput": {"input": "test"},
            "pressedButton": "next",
        }

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        screen = MockScreen()
        screen.validation_passes = True
        screen.clear_html_popup = True

        session.display_screen(screen)

        # Should call rpc_send to clear HTML
        assert mock_rpc_send.called

    @patch("netmagus.session.netmagus.rpc.rpc_send")
    @patch("netmagus.session.netmagus.rpc.rpc_form_query")
    def test_display_screen_navigates_to_next_screen(
        self, mock_rpc_query, mock_rpc_send
    ):
        """Test display_screen recursively displays next_screen"""
        mock_rpc_send.return_value = "ok"
        mock_rpc_query.return_value = {
            "wellFormatedInput": {"input": "test"},
            "pressedButton": "next",
        }

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        # Create two screens
        screen1 = MockScreen()
        screen2 = MockScreen()
        screen1.validation_passes = True
        screen2.validation_passes = True
        screen1.next_screen = screen2

        session.display_screen(screen1)

        # Both screens should have session set
        assert screen1.session is session
        assert screen2.session is session

    @patch("netmagus.rpc.rpc_form_query")
    @patch("netmagus.rpc.rpc_send")
    def test_display_screen_handles_cancel_button(self, mock_rpc_send, mock_rpc_query):
        """Test display_screen handles CancelButtonPressed"""
        mock_rpc_query.return_value = {
            "wellFormatedInput": {},
            "pressedButton": "cancel",
        }

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        screen = MockScreen()

        with pytest.raises(CancelButtonPressed):
            session.display_screen(screen)

        # Should clear HTML and call handle_cancel_button
        assert mock_rpc_send.called

    @patch("netmagus.session.netmagus.rpc.rpc_send")
    @patch("netmagus.session.netmagus.rpc.rpc_form_query")
    def test_display_screen_handles_back_button(self, mock_rpc_query, mock_rpc_send):
        """Test display_screen handles BackButtonPressed and navigates back"""
        mock_rpc_send.return_value = "ok"
        # First call: return back button
        # Second call: return next button for back screen
        mock_rpc_query.side_effect = [
            {"wellFormatedInput": {}, "pressedButton": "back"},
            {"wellFormatedInput": {"input": "test"}, "pressedButton": "next"},
        ]

        session = NetMagusSession(
            token="test_token",
            input_file="/tmp/test.json",
            loglevel=10,
            script="test_script",
        )

        back_screen = MockScreen()
        back_screen.validation_passes = True
        current_screen = MockScreen()
        current_screen.back_screen = back_screen

        session.display_screen(current_screen)

        # Back screen should have been displayed
        assert back_screen.session is session
        assert mock_rpc_query.call_count == 2
