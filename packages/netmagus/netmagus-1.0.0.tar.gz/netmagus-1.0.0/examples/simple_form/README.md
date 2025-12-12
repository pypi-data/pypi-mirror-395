# Simple Form Example

This is a basic NetMagus formula example that demonstrates how to create a simple form with text inputs.

## What This Example Demonstrates

- Creating basic form input fields (TextInput)
- Building a Form object with name, description, and form controls
- Processing user input from the NetMagus backend
- Returning a completion screen

## Formula Structure

- `formula.json` - Metadata about the formula (name, version, dependencies)
- `simple_form.py` - The main formula code with the `run()` entry point
- `README.md` - This documentation file

## How It Works

1. The NetMagus backend calls this formula with input data
2. The `run()` function is called with a NetMagusSession object
3. If no previous input exists, it displays the initial form
4. If input exists (user submitted the form), it displays a completion screen with the entered data

## Running This Example

To run this formula, you would typically use:

```bash
uv run python -m netmagus --script simple_form --input-file /path/to/input.json --token abc123 --loglevel 1
```

However, formulas are normally executed by the NetMagus backend server, not manually.

## Key Concepts

- **session.textinput()**: Creates a text input field
- **session.form()**: Creates a Form object to be rendered in the UI
- **session.nm_input**: Contains data submitted by the user
- **finalStep=True**: Indicates this is the last screen in the wizard
