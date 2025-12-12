"""
RPC Interaction Example
========================

This example demonstrates real-time communication with the NetMagus UI using
RPC (Remote Procedure Call) via WAMP websockets.

It shows how to:
- Send HTML messages to the UI
- Display progress updates during long-running tasks
- Use interactive prompts via RPC
- Update the UI in real-time

Usage:
    uv run python -m netmagus --script formula --input-file /path/to/input.json \\
        --token abc123 --loglevel 1
"""

import time

import netmagus


def run(nm_session: netmagus.NetMagusSession) -> netmagus.form.Form:
    """
    Entry point for the RPC interaction example.

    This demonstrates various RPC communication patterns with the NetMagus UI.

    :param nm_session: The NetMagus session object
    :return: A Form object to display in the NetMagus UI
    """
    # Connect to the NetMagus WAMP server for RPC communication
    nm_session.rpc_connect()

    # Create the completion screen
    finish_screen = nm_session.form(
        name="RPC Demo Complete",
        description="<p>The RPC interaction demonstration has completed.</p>",
        form=[],
        currentStep=99,
        autoProceed=True,
        finalStep=True,
    )

    # Example 1: Send a welcome HTML message
    nm_session.logger.info("Sending welcome message to UI")
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Welcome to RPC Demo",
            data="<h3>Starting RPC Interaction Demo</h3>"
            "<p>This demo will show you various ways to interact with the UI in real-time.</p>",
            append=False,  # Replace any existing content
        )
    )
    time.sleep(2)

    # Example 2: Simulate a task with progress updates
    nm_session.logger.info("Starting simulated task with progress updates")
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Task",
            data="<p><strong>Step 1 of 3:</strong> Initializing...</p>",
            append=True,  # Append to existing content
        )
    )
    time.sleep(1)

    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Task",
            data="<p><strong>Step 2 of 3:</strong> Processing data...</p>",
            append=True,
        )
    )
    time.sleep(1)

    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Task",
            data="<p><strong>Step 3 of 3:</strong> Finalizing...</p>",
            append=True,
        )
    )
    time.sleep(1)

    # Example 3: Interactive prompt using rpc_form_query
    nm_session.logger.info("Sending interactive form prompt")

    # Create a simple form to ask user a question
    user_choice = nm_session.radiobutton(
        label="Choose an action",
        value=["Continue with Demo", "Skip to End", "Show More Details"],
    )

    action_form = nm_session.form(
        name="User Choice",
        description="<p>What would you like to do next?</p>",
        form=[user_choice],
        buttonName="Submit",
    )

    # Send the form and wait for user response
    response = nm_session.rpc_form_query(action_form, poll=0.5, timeout=60)
    selected_action = response.get("wellFormatedInput", {}).get("Choose an action", "")

    nm_session.logger.info(f"User selected: {selected_action}")

    # Example 4: React to user choice
    if selected_action == "Continue with Demo":
        nm_session.rpc_html_clear()  # Clear previous HTML
        nm_session.rpc_send(
            nm_session.rpc_html(
                title="Continuing Demo",
                data="<p>Great! Continuing with the demonstration...</p>"
                "<p>RPC allows for dynamic, real-time updates to the UI.</p>"
                "<p>You can use it to show progress, warnings, or any HTML content.</p>",
                append=False,
            )
        )
        time.sleep(2)

    elif selected_action == "Show More Details":
        nm_session.rpc_html_clear()
        nm_session.rpc_send(
            nm_session.rpc_html(
                title="RPC Details",
                data="<h3>About NetMagus RPC</h3>"
                "<ul>"
                "<li>Uses WAMP (Web Application Messaging Protocol)</li>"
                "<li>Supports real-time bidirectional communication</li>"
                "<li>Can send HTML, forms, and other data types</li>"
                "<li>Allows formulas to update UI during long operations</li>"
                "</ul>",
                append=False,
            )
        )
        time.sleep(3)

    else:  # Skip to End
        nm_session.rpc_html_clear()
        nm_session.rpc_send(
            nm_session.rpc_html(
                title="Skipping",
                data="<p>Skipping to the end of the demo...</p>",
                append=False,
            )
        )
        time.sleep(1)

    # Final message
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Demo Complete",
            data="<p><strong>RPC Demonstration Complete!</strong></p>"
            "<p>You can now click Next to finish.</p>",
            append=True,
        )
    )

    # Disconnect from RPC
    nm_session.rpc_disconnect()

    return finish_screen
