"""
Multi-Step Wizard Example
==========================

This example demonstrates creating a multi-step wizard using NetMagus Screen objects.
The wizard collects server deployment information across multiple screens.

Usage:
    uv run python -m netmagus --script formula --input-file /path/to/input.json \\
        --token abc123 --loglevel 1
"""

from screens import NetworkConfigScreen, ReviewScreen, ServerInfoScreen, WelcomeScreen

import netmagus


def run(nm_session: netmagus.NetMagusSession) -> netmagus.form.Form:
    """
    Entry point for the multi-step wizard formula.

    This creates a wizard with multiple screens that guide the user through
    a server deployment configuration process.

    :param nm_session: The NetMagus session object
    :return: A Form object to display in the NetMagus UI
    """
    # Initialize session data to store information across screens
    if not nm_session.session_data:
        nm_session.session_data = {}

    # Create the finish screen shown when complete or cancelled
    finish_screen = nm_session.form(
        name="Wizard Complete",
        description="<p>The server deployment configuration wizard has completed.</p>",
        form=[],
        currentStep=99,
        autoProceed=True,
        finalStep=True,
    )

    # Connect to NetMagus server for RPC communication
    nm_session.rpc_connect()

    # Create screen instances
    welcome = WelcomeScreen()
    server_info = ServerInfoScreen()
    network_config = NetworkConfigScreen()
    review = ReviewScreen()

    # Set up screen navigation flow
    welcome.next_screen = server_info
    welcome.back_screen = None

    server_info.next_screen = network_config
    server_info.back_screen = welcome

    network_config.next_screen = review
    network_config.back_screen = server_info

    review.next_screen = None
    review.back_screen = network_config

    # Start the wizard with the first screen
    try:
        nm_session.display_screen(welcome)
        return finish_screen
    except netmagus.CancelButtonPressed:
        return finish_screen
