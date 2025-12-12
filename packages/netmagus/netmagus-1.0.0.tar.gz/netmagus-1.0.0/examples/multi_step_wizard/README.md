# Multi-Step Wizard Example

This example demonstrates how to create a multi-step wizard using NetMagus Screen objects. The wizard guides users through a server deployment configuration process.

## What This Example Demonstrates

- Creating multiple Screen objects that inherit from ScreenBase
- Navigating between screens using next_screen and back_screen
- Using session_data to persist information across screens
- Input validation and error messages
- Processing user input in each screen
- Creating a complete wizard workflow

## Formula Structure

- `formula.json` - Metadata about the formula
- `formula.py` - Main entry point that sets up the wizard flow
- `screens.py` - Screen class definitions
- `README.md` - This documentation file

## Wizard Flow

1. **WelcomeScreen** - Introduction to the wizard
2. **ServerInfoScreen** - Collects hostname, OS, and environment
3. **NetworkConfigScreen** - Collects IP address, subnet mask, and gateway
4. **ReviewScreen** - Shows summary of all collected information

Users can navigate forward and backward through the screens, and data is preserved in `session.session_data`.

## Screen Structure

Each screen implements the ScreenBase interface:

```python
class MyScreen(ScreenBase):
    def generate_form(self):
        # Create and return a Form object
        pass

    def process_user_input(self):
        # Process the user's input data
        pass

    def validate_user_input(self):
        # Validate input, return True/False
        pass

    def return_error_message(self):
        # Show error if validation fails
        pass

    def handle_back_button(self):
        # Cleanup when back is pressed
        pass

    def handle_cancel_button(self):
        # Cleanup when cancel is pressed
        pass
```

## Running This Example

```bash
uv run python -m netmagus --script formula --input-file /path/to/input.json --token abc123 --loglevel 1
```

## Key Concepts

- **ScreenBase**: Base class for creating interactive screens
- **session.display_screen()**: Displays a screen and handles navigation
- **session.session_data**: Persistent storage across screens
- **next_screen/back_screen**: Define navigation flow
- **validate_user_input()**: Ensures data quality before proceeding
