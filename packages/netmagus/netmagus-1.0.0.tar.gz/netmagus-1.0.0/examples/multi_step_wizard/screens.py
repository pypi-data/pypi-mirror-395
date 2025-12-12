"""
Screen definitions for the multi-step wizard example.

Each screen class inherits from netmagus.ScreenBase and implements:
- generate_form(): Creates the form to display
- process_user_input(): Processes data when user submits
- validate_user_input(): Validates the input data
- return_error_message(): Shows error if validation fails
- handle_back_button(): Cleanup when back is pressed
- handle_cancel_button(): Cleanup when cancel is pressed
"""

from netmagus import Form, Html, ScreenBase
from netmagus.form import DropDownMenu, RadioButton, TextInput


class WelcomeScreen(ScreenBase):
    """
    Welcome screen that introduces the wizard.
    """

    def generate_form(self):
        return Form(
            name="Server Deployment Wizard",
            description="<p>Welcome to the Server Deployment Configuration Wizard.</p>"
            "<p>This wizard will guide you through configuring a new server deployment.</p>"
            "<p>Click Next to continue.</p>",
            form=[],
            buttonName="Next",
            autoProceed=True,
            disableBackButton=True,
        )

    def process_user_input(self):
        # No input to process on welcome screen
        pass

    def validate_user_input(self):
        return True

    def return_error_message(self):
        pass

    def handle_back_button(self):
        pass

    def handle_cancel_button(self):
        pass


class ServerInfoScreen(ScreenBase):
    """
    Screen to collect basic server information.
    """

    def generate_form(self):
        hostname_input = TextInput(
            label="Hostname",
            name="hostname",
            description="Enter the server hostname",
            required=True,
        )

        os_dropdown = DropDownMenu(
            label="Operating System",
            options=["Ubuntu 22.04", "Ubuntu 20.04", "RHEL 9", "RHEL 8", "Debian 12"],
        )

        environment_radio = RadioButton(
            label="Environment",
            value=["Production", "Staging", "Development", "Testing"],
        )

        return Form(
            name="Server Information",
            description="<p>Enter basic information about the server.</p>",
            form=[hostname_input, os_dropdown, environment_radio],
            buttonName="Next",
            autoProceed=True,
            disableBackButton=False,
        )

    def process_user_input(self):
        # Store server info in session data
        self.session.session_data["hostname"] = self.user_input.get("Hostname", "")
        self.session.session_data["os"] = self.user_input.get("Operating System", "")
        self.session.session_data["environment"] = self.user_input.get(
            "Environment", ""
        )
        self.session.logger.info(f"Server info collected: {self.session.session_data}")

    def validate_user_input(self):
        hostname = self.user_input.get("Hostname", "").strip()
        if not hostname:
            return False
        # Basic hostname validation
        if len(hostname) < 3 or len(hostname) > 63:
            return False
        return True

    def return_error_message(self):
        self.session.rpc_html_clear()
        self.session.rpc_send(
            Html(
                title="Invalid Hostname",
                data="<p>Hostname must be between 3 and 63 characters.</p>",
            )
        )

    def handle_back_button(self):
        pass

    def handle_cancel_button(self):
        pass


class NetworkConfigScreen(ScreenBase):
    """
    Screen to collect network configuration.
    """

    def generate_form(self):
        ip_input = TextInput(
            label="IP Address",
            name="ip_address",
            description="Enter the server IP address (e.g., 192.168.1.100)",
            required=True,
        )

        subnet_input = TextInput(
            label="Subnet Mask",
            name="subnet_mask",
            description="Enter the subnet mask (e.g., 255.255.255.0)",
            required=True,
        )

        gateway_input = TextInput(
            label="Default Gateway",
            name="gateway",
            description="Enter the default gateway IP",
            required=True,
        )

        return Form(
            name="Network Configuration",
            description="<p>Configure network settings for the server.</p>",
            form=[ip_input, subnet_input, gateway_input],
            buttonName="Next",
            autoProceed=True,
            disableBackButton=False,
        )

    def process_user_input(self):
        # Store network config in session data
        self.session.session_data["ip_address"] = self.user_input.get("IP Address", "")
        self.session.session_data["subnet_mask"] = self.user_input.get(
            "Subnet Mask", ""
        )
        self.session.session_data["gateway"] = self.user_input.get(
            "Default Gateway", ""
        )
        self.session.logger.info(
            f"Network config collected: {self.session.session_data}"
        )

    def validate_user_input(self):
        # Simple validation - check fields are not empty
        ip = self.user_input.get("IP Address", "").strip()
        subnet = self.user_input.get("Subnet Mask", "").strip()
        gateway = self.user_input.get("Default Gateway", "").strip()

        if not all([ip, subnet, gateway]):
            return False
        return True

    def return_error_message(self):
        self.session.rpc_html_clear()
        self.session.rpc_send(
            Html(
                title="Invalid Network Configuration",
                data="<p>All network fields are required.</p>",
            )
        )

    def handle_back_button(self):
        pass

    def handle_cancel_button(self):
        pass


class ReviewScreen(ScreenBase):
    """
    Final screen to review and confirm all entered information.
    """

    def generate_form(self):
        data = self.session.session_data

        description = f"""
        <h3>Review Your Configuration</h3>
        <p>Please review the information below and click Next to complete the wizard.</p>

        <h4>Server Information</h4>
        <ul>
            <li><strong>Hostname:</strong> {data.get('hostname', 'N/A')}</li>
            <li><strong>Operating System:</strong> {data.get('os', 'N/A')}</li>
            <li><strong>Environment:</strong> {data.get('environment', 'N/A')}</li>
        </ul>

        <h4>Network Configuration</h4>
        <ul>
            <li><strong>IP Address:</strong> {data.get('ip_address', 'N/A')}</li>
            <li><strong>Subnet Mask:</strong> {data.get('subnet_mask', 'N/A')}</li>
            <li><strong>Default Gateway:</strong> {data.get('gateway', 'N/A')}</li>
        </ul>
        """

        return Form(
            name="Review Configuration",
            description=description,
            form=[],
            buttonName="Complete",
            autoProceed=True,
            disableBackButton=False,
        )

    def process_user_input(self):
        self.session.logger.info(
            f"Configuration confirmed: {self.session.session_data}"
        )
        # Here you would normally submit the configuration to a backend system

    def validate_user_input(self):
        return True

    def return_error_message(self):
        pass

    def handle_back_button(self):
        pass

    def handle_cancel_button(self):
        pass
