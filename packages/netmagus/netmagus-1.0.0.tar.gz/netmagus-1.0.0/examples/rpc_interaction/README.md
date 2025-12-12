# RPC Interaction Example

This example demonstrates real-time communication with the NetMagus UI using RPC (Remote Procedure Call) via WAMP websockets.

## What This Example Demonstrates

- Connecting to the NetMagus WAMP server
- Sending HTML messages to update the UI in real-time
- Displaying progress updates during long-running tasks
- Using `rpc_form_query()` for interactive user prompts
- Clearing and appending HTML content
- Disconnecting from RPC when done

## Formula Structure

- `formula.json` - Metadata about the formula
- `formula.py` - Main formula code demonstrating RPC patterns
- `README.md` - This documentation file

## RPC Communication Flow

1. **Connect**: Establish connection to WAMP server
2. **Send Messages**: Send HTML updates to the UI
3. **Interactive Prompts**: Ask user questions and wait for responses
4. **Progress Updates**: Show real-time progress during tasks
5. **Disconnect**: Close the RPC connection

## Running This Example

```bash
uv run python -m netmagus --script formula --input-file /path/to/input.json --token abc123 --loglevel 1
```

## Key RPC Methods

### session.rpc_connect()
Establishes connection to the NetMagus WAMP server:
```python
session.rpc_connect()
```

### session.rpc_send()
Sends an HTML message to the UI:
```python
session.rpc_send(
    session.rpc_html(
        title='My Title',
        data='<p>HTML content here</p>',
        append=True  # Append to existing content
    )
)
```

### session.rpc_form_query()
Sends a form and waits for user response:
```python
response = session.rpc_form_query(
    form_object,
    poll=0.5,    # Poll every 0.5 seconds
    timeout=60   # Timeout after 60 seconds
)
```

### session.rpc_html_clear()
Clears the HTML popup in the UI:
```python
session.rpc_html_clear()
```

### session.rpc_disconnect()
Closes the RPC connection:
```python
session.rpc_disconnect()
```

## Use Cases for RPC

- **Long-running tasks**: Show progress updates during operations that take time
- **User confirmations**: Ask for confirmation before critical operations
- **Status updates**: Display real-time status information
- **Error notifications**: Show warnings or errors immediately
- **Interactive workflows**: Create dynamic user experiences

## Important Notes

- RPC requires a running NetMagus backend with WAMP support
- Always call `rpc_connect()` before using RPC methods
- Remember to call `rpc_disconnect()` when done
- Use `append=True` to add to existing HTML, `append=False` to replace it
