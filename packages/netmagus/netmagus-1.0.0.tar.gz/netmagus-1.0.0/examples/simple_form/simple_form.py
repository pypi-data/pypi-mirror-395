"""
Simple Form Example
====================

This example demonstrates the basics of creating a NetMagus formula with
a simple form containing text inputs. It shows:
- Creating form input fields
- Building a basic Form object
- Returning a completion screen

Usage:
    uv run python -m netmagus --script simple_form --input-file /path/to/input.json \\
        --token abc123 --loglevel 1
"""

import netmagus


def run(session: netmagus.NetMagusSession) -> netmagus.form.Form:
    """
    Entry point for the simple form formula.

    This function creates a basic form with name and email inputs,
    then returns a completion screen.

    :param session: The NetMagus session object
    :return: A Form object to display in the NetMagus UI
    """
    # Create form input components
    name_input = session.textinput(
        label="Your Name",
        name="user_name",
        description="Please enter your full name",
        required=True,
    )

    email_input = session.textinput(
        label="Email Address",
        name="user_email",
        description="Please enter your email address",
        required=True,
    )

    # Build the form
    form = session.form(
        name="Simple User Information Form",
        description="<p>This is a basic example form that collects user information.</p>"
        "<p>Please fill in the fields below and click Submit.</p>",
        form=[name_input, email_input],
        currentStep=1,
        finalStep=True,
    )

    # Log the received input if this is a subsequent call
    if session.nm_input:
        session.logger.info(f"Received input from user: {session.nm_input}")

        # Extract the user input
        user_data = session.nm_input.get("wellFormatedInput", {})
        name = user_data.get("user_name", "")
        email = user_data.get("user_email", "")

        # Create a completion message
        completion_form = session.form(
            name="Form Submission Complete",
            description=f"<p>Thank you for submitting the form!</p>"
            f"<p><strong>Name:</strong> {name}</p>"
            f"<p><strong>Email:</strong> {email}</p>"
            f"<p>This information has been recorded.</p>",
            currentStep=2,
            finalStep=True,
        )

        return completion_form

    # Return the initial form
    return form
