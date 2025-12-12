# NetMagus Formula Examples

This directory contains example NetMagus formulas demonstrating various features and patterns for creating interactive network automation workflows.

## Available Examples

### 1. Simple Form (`simple_form/`)
A basic example showing how to create a simple form with text inputs.

**Demonstrates:**
- Creating basic form input fields
- Building Form objects
- Processing user input
- Displaying completion screens

**Best for:** Getting started with NetMagus formulas

### 2. Multi-Step Wizard (`multi_step_wizard/`)
A comprehensive example showing how to create a multi-step wizard using Screen objects.

**Demonstrates:**
- Creating multiple Screen classes
- Screen navigation (next/back)
- Persistent data with session_data
- Input validation
- Error handling

**Best for:** Complex workflows requiring multiple user interaction steps

### 3. RPC Interaction (`rpc_interaction/`)
An example demonstrating real-time communication with the NetMagus UI.

**Demonstrates:**
- WAMP RPC connections
- Sending HTML messages to UI
- Progress updates during tasks
- Interactive user prompts
- Real-time UI updates

**Best for:** Long-running tasks that need user feedback or progress updates

## Formula Structure

Each example formula contains:

- `formula.json` - Metadata and configuration for the formula
- `formula.py` or `{module}.py` - Main Python code with `run()` entry point
- `screens.py` (optional) - Screen class definitions for multi-step wizards
- `README.md` - Documentation specific to that example

## Formula.json Schema

The `formula.json` file defines metadata about your formula:

```json
{
  "id": -1,
  "uuid": "unique-uuid-here",
  "name": "Formula Display Name",
  "commandPath": "uv run python -u -m netmagus --script module_name",
  "jsonPath": null,
  "form": "[]",
  "description": "<p>HTML description shown in UI</p>",
  "categoryID": 1,
  "numberOfSteps": 1,
  "currentStep": 1,
  "enabled": true,
  "accessLevel": 1,
  "logLevel": 1,
  "dataValid": false,
  "saveRecord": false,
  "buttonName": "",
  "dynamic": false,
  "autoProceed": false,
  "disableBackButton": false,
  "singleton": false,
  "uidDate": null,
  "finalStep": false,
  "timeSaved": 0,
  "history": [],
  "extraInfo": {},
  "formulaPath": null,
  "installationScript": "",
  "nameNoSpaces": "Formula_Name_No_Spaces",
  "md5": ""
}
```

## Running Examples

Examples use `uv` for Python environment management. To run an example:

```bash
cd examples/simple_form
uv run python -m netmagus --script simple_form --input-file input.json --token test123 --loglevel 1
```

However, formulas are typically executed by the NetMagus backend server, not manually.

## Key Concepts

### Entry Point
Every formula must have a `run()` function that accepts a `NetMagusSession` object:

```python
def run(session: netmagus.NetMagusSession) -> netmagus.form.Form:
    # Your formula logic here
    return form_object
```

### Session Object
The session object provides access to:
- `session.nm_input` - Input data from NetMagus backend
- `session.session_data` - Persistent storage across formula steps
- `session.logger` - Logging interface
- `session.form()` - Create Form objects
- `session.textinput()`, `session.dropdown()`, etc. - Create form controls
- `session.rpc_connect()`, `session.rpc_send()` - RPC communication methods

### Form Controls
Available form input types:
- `TextInput` - Single-line text input
- `TextArea` - Multi-line text input
- `PasswordInput` - Masked password input
- `DropDownMenu` - Dropdown selection
- `RadioButton` - Radio button group
- `CheckBox` - Checkbox group
- `SelectDrop` - Dual-list drag-and-drop selector

### Screen-Based Formulas
For multi-step wizards, use `ScreenBase` classes:

```python
class MyScreen(ScreenBase):
    def generate_form(self):
        return Form(...)

    def process_user_input(self):
        # Process input
        pass

    def validate_user_input(self):
        return True

    def return_error_message(self):
        # Show error
        pass
```

## Best Practices

1. **Always validate user input** - Use `validate_user_input()` in screens
2. **Use session_data for persistence** - Store data between steps
3. **Provide clear descriptions** - Help users understand what to enter
4. **Log appropriately** - Use `session.logger` for debugging
5. **Handle errors gracefully** - Show clear error messages to users
6. **Use RPC for long tasks** - Keep users informed of progress
7. **Test thoroughly** - Validate with various input scenarios

## Dependencies

All examples require the `netmagus` Python package:

```bash
pip install netmagus
```

Or with uv:

```bash
uv pip install netmagus
```

## Further Reading

- NetMagus Documentation: See official NetMagus docs
- Python API Reference: Check `netmagus` module docstrings
- WAMP Protocol: https://wamp-proto.org/ for RPC details

## Contributing

When creating new examples:
1. Follow the existing structure
2. Include a unique UUID in formula.json
3. Provide clear documentation in README.md
4. Use meaningful variable and function names
5. Add comments explaining complex logic
