"""
File Upload and Download Example
=================================

This example demonstrates a two-screen workflow using FilesUpload and FileDownloadLink components.

Screen 1: File Upload
- Shows a FilesUpload component for users to upload input files
- Collects files from the user

Screen 2: File Download
- Processes the uploaded files (simulated with RPC progress updates)
- Provides FileDownloadLink components to download generated results

Usage:
    uv run python -m netmagus --script formula --input-file /path/to/input.json \
        --token abc123 --loglevel 1
"""

import time

import netmagus


def run(nm_session: netmagus.NetMagusSession) -> netmagus.form.Form:
    """
    Entry point for the file upload and download example formula.

    This formula demonstrates a complete workflow:
    1. Upload files using FilesUpload component
    2. Process the files (with progress shown via RPC)
    3. Download results using FileDownloadLink components

    :param nm_session: The NetMagus session object
    :return: A Form object to display in the NetMagus UI
    """
    # Check if this is the first run (no input from user yet)
    if not nm_session.nm_input:
        # SCREEN 1: File Upload Form
        nm_session.logger.info("Displaying file upload form")

        # Create file upload component
        file_upload = netmagus.FilesUpload(
            editable=True,
            label="Upload Data Files",
            description="Upload one or more files for processing (CSV, Excel, or text files)",
            placeholder="Choose files to upload...",
            required=True,
            validation="/.*/",
        )

        # Build the upload form
        upload_form = nm_session.form(
            name="Upload Files for Processing",
            description="<h3>File Upload and Processing</h3>"
            "<p>This example demonstrates uploading files and then downloading processed results.</p>"
            "<p><strong>Step 1:</strong> Please select and upload your data files below.</p>"
            "<p>After uploading, we will process your files and generate downloadable reports.</p>",
            form=[file_upload],
            currentStep=1,
            finalStep=False,
        )

        return upload_form

    # SCREEN 2: Process files and show download links
    nm_session.logger.info("Processing uploaded files")

    # Get uploaded files info from the input
    user_input = nm_session.nm_input.get("wellFormatedInput", {})
    uploaded_files = user_input.get("Upload Data Files", [])

    nm_session.logger.info(
        f"Received {len(uploaded_files) if uploaded_files else 0} uploaded files"
    )

    # Connect to NetMagus server for RPC communication
    nm_session.rpc_connect()

    # Show initial processing message
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Uploaded Files",
            data="<h3>Processing Your Files</h3>"
            f"<p>Received {len(uploaded_files) if uploaded_files else 0} file(s) for processing.</p>"
            "<p>Please wait while we analyze your data and generate reports...</p>",
            append=False,
        )
    )
    time.sleep(1)

    # Simulate CSV generation
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Progress",
            data="<p><strong>Step 1 of 3:</strong> Analyzing uploaded files and generating CSV results...</p>",
            append=True,
        )
    )
    time.sleep(1.5)

    # Simulate PDF generation
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Progress",
            data="<p><strong>Step 2 of 3:</strong> Creating comprehensive PDF report...</p>",
            append=True,
        )
    )
    time.sleep(1.5)

    # Simulate log file creation
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Progress",
            data="<p><strong>Step 3 of 3:</strong> Generating execution log...</p>",
            append=True,
        )
    )
    time.sleep(1)

    # Show completion message
    nm_session.rpc_send(
        nm_session.rpc_html(
            title="Processing Complete",
            data="<p><strong style='color: green;'>✓ All files processed successfully!</strong></p>"
            "<p>Your reports are ready for download on the next screen.</p>",
            append=True,
        )
    )
    time.sleep(2)

    # Disconnect from RPC
    nm_session.rpc_disconnect()

    # Create file download link components for the generated files
    csv_download = netmagus.FileDownloadLink(
        label="CSV Results",
        description="Download the analysis results in CSV format",
        linkUrl="output/analysis_results.csv",
        linkText="Download CSV File",
        required=False,
        group="Generated Reports",
        message="Analysis results in comma-separated values format",
    )

    pdf_download = netmagus.FileDownloadLink(
        label="PDF Report",
        description="Download the full analysis report in PDF format",
        linkUrl="reports/full_analysis.pdf",
        linkText="Download PDF Report",
        required=False,
        group="Generated Reports",
        message="Complete analysis report with charts and graphs",
    )

    log_download = netmagus.FileDownloadLink(
        label="Execution Log",
        description="Download the processing execution log",
        linkUrl="logs/execution.log",
        linkText="Download Log File",
        required=False,
        group="System Files",
        message="Detailed execution log for troubleshooting",
    )

    # Build the download form
    download_form = nm_session.form(
        name="Download Generated Files",
        description="<h3>Your Reports Are Ready!</h3>"
        "<p>All requested files have been processed successfully.</p>"
        "<p><strong>Step 2:</strong> Click on the links below to download your results:</p>",
        form=[csv_download, pdf_download, log_download],
        currentStep=2,
        finalStep=True,
    )

    return download_form
