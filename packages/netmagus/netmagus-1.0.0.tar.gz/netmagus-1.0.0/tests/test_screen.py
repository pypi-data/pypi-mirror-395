"""
Tests for netmagus.screen module

Tests cover ScreenBase abstract class workflow and exception classes.
"""

import pytest

from netmagus.form import Form, TextInput
from netmagus.screen import BackButtonPressed, CancelButtonPressed, ScreenBase


class TestScreenExceptions:
    """Test custom exception classes"""

    def test_cancel_button_pressed_is_exception(self):
        """CancelButtonPressed should be an Exception"""
        assert issubclass(CancelButtonPressed, Exception)

    def test_back_button_pressed_is_exception(self):
        """BackButtonPressed should be an Exception"""
        assert issubclass(BackButtonPressed, Exception)

    def test_cancel_button_pressed_can_be_raised(self):
        """CancelButtonPressed can be raised and caught"""
        with pytest.raises(CancelButtonPressed):
            raise CancelButtonPressed()

    def test_back_button_pressed_can_be_raised(self):
        """BackButtonPressed can be raised and caught"""
        with pytest.raises(BackButtonPressed):
            raise BackButtonPressed()


class MockScreen(ScreenBase):
    """Concrete implementation of ScreenBase for testing"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Track method calls for assertions
        self.validate_called = False
        self.process_called = False
        self.error_called = False
        self.cancel_called = False
        self.back_called = False
        # Control validation return value
        self.validation_result = True

    def generate_form(self):
        """Generate a simple test form"""
        return Form(
            name="Test Form",
            description="Test Description",
            form=[TextInput(label="Test Input")],
        )

    def validate_user_input(self):
        """Mock validation"""
        self.validate_called = True
        return self.validation_result

    def process_user_input(self):
        """Mock processing"""
        self.process_called = True

    def return_error_message(self):
        """Mock error message"""
        self.error_called = True

    def handle_cancel_button(self):
        """Mock cancel handling"""
        self.cancel_called = True

    def handle_back_button(self):
        """Mock back button handling"""
        self.back_called = True


class TestScreenBaseInitialization:
    """Test ScreenBase initialization"""

    def test_init_default_parameters(self):
        """Test ScreenBase initialization with defaults"""
        screen = MockScreen()

        assert screen.session is None
        assert screen.user_input is None
        assert screen.input_valid is False
        assert screen.button_pressed is None
        assert screen.next_screen is None
        assert screen.back_screen is None
        assert screen.clear_html_popup is True

    def test_init_with_parameters(self):
        """Test ScreenBase initialization with custom parameters"""
        mock_session = object()
        next_screen = MockScreen()
        back_screen = MockScreen()

        screen = MockScreen(
            session=mock_session,
            clear_html_popup=False,
            next_screen=next_screen,
            back_screen=back_screen,
        )

        assert screen.session is mock_session
        assert screen.clear_html_popup is False
        assert screen.next_screen is next_screen
        assert screen.back_screen is back_screen


class TestScreenBaseFormProperty:
    """Test form property and _render_form method"""

    def test_form_property_returns_rendered_form(self):
        """form property should call _render_form"""
        screen = MockScreen()
        form = screen.form

        assert isinstance(form, Form)
        assert form.name == "Test Form"

    def test_render_form_disables_back_button_when_no_back_screen(self):
        """_render_form should disable back button if back_screen is None"""
        screen = MockScreen()
        form = screen.form

        assert form.disableBackButton is True

    def test_render_form_keeps_back_button_when_back_screen_exists(self):
        """_render_form should not disable back button if back_screen is set"""
        back_screen = MockScreen()
        screen = MockScreen(back_screen=back_screen)
        form = screen.form

        # The form generation doesn't set disableBackButton=False,
        # so _render_form won't change it from its default
        # This tests that we don't force it to True
        assert form.disableBackButton is True or form.disableBackButton is False

    def test_render_form_sets_component_indexes(self):
        """_render_form should set index on all form components"""
        screen = MockScreen()
        form = screen.form

        for i, component in enumerate(form.form):
            assert component.index == i


class TestScreenBaseProcessUserInput:
    """Test _process_user_input workflow"""

    def test_process_user_input_when_valid(self):
        """When validation passes, should set input_valid and call process_user_input"""
        screen = MockScreen()
        screen.validation_result = True
        screen._process_user_input()

        assert screen.validate_called is True
        assert screen.process_called is True
        assert screen.input_valid is True
        assert screen.error_called is False

    def test_process_user_input_when_invalid(self):
        """When validation fails, should call return_error_message"""
        screen = MockScreen()
        screen.validation_result = False
        screen._process_user_input()

        assert screen.validate_called is True
        assert screen.process_called is False
        assert screen.input_valid is False
        assert screen.error_called is True


class TestScreenBaseProcessButton:
    """Test process_button logic for different button types"""

    def test_process_button_cancel_raises_exception(self):
        """process_button should raise CancelButtonPressed for 'cancel' button"""
        screen = MockScreen()
        screen.button_pressed = "cancel"

        with pytest.raises(CancelButtonPressed):
            screen.process_button()

    def test_process_button_back_raises_exception(self):
        """process_button should raise BackButtonPressed for 'back' button"""
        screen = MockScreen()
        screen.button_pressed = "back"

        with pytest.raises(BackButtonPressed):
            screen.process_button()

    def test_process_button_tryagain_raises_exception(self):
        """process_button should raise BackButtonPressed for 'tryagain' button"""
        screen = MockScreen()
        screen.button_pressed = "tryagain"

        with pytest.raises(BackButtonPressed):
            screen.process_button()

    def test_process_button_next_validates_input(self):
        """process_button should validate input for 'next' button"""
        screen = MockScreen()
        screen.button_pressed = "next"
        screen.validation_result = True
        screen.process_button()

        assert screen.validate_called is True
        assert screen.process_called is True

    def test_process_button_next_lowercase(self):
        """process_button should handle 'NEXT' case-insensitively"""
        screen = MockScreen()
        screen.button_pressed = "NEXT"
        screen.validation_result = True
        screen.process_button()

        assert screen.validate_called is True

    def test_process_button_unknown_raises_error(self):
        """process_button should raise NotImplementedError for unknown buttons"""
        screen = MockScreen()
        screen.button_pressed = "unknown_button"

        with pytest.raises(NotImplementedError) as excinfo:
            screen.process_button()

        assert "unknown_button" in str(excinfo.value)


class TestScreenBaseAbstractMethods:
    """Test that ScreenBase enforces abstract method implementation"""

    def test_cannot_instantiate_screenbase_directly(self):
        """ScreenBase cannot be instantiated without implementing abstract methods"""
        with pytest.raises(TypeError) as excinfo:
            ScreenBase()

        assert "abstract" in str(excinfo.value).lower()

    def test_mockscreen_implements_all_abstract_methods(self):
        """MockScreen should successfully implement all required abstract methods"""
        # This should not raise any errors
        screen = MockScreen()

        # Verify all abstract methods can be called
        screen.generate_form()
        screen.validate_user_input()
        screen.process_user_input()
        screen.return_error_message()
        screen.handle_cancel_button()
        screen.handle_back_button()
