# File Upload and Download Example

This example demonstrates a two-screen workflow using `FilesUpload` and `FileDownloadLink` components in NetMagus.

## Overview

This formula shows a complete file processing workflow with two screens:

**Screen 1: File Upload**
- User uploads files using the `FilesUpload` component
- Accepts multiple files for processing

**Screen 2: Download Results**
- Shows RPC progress updates during file processing
- Presents `FileDownloadLink` components for generated results
- Provides organized download links grouped by category

## Key Features

### FilesUpload Component (Screen 1)
- **Multiple File Support**: Upload one or more files
- **Validation**: Configure file type validation
- **Required Fields**: Enforce file upload requirement

### FileDownloadLink Component (Screen 2)
- **RPC Communication**: Real-time progress updates during file generation
- **Relative Paths**: File paths specified relative to NetMagus server (e.g., `output/results.csv`)
- **Customizable Link Text**: Set custom text for each download link
- **Group Organization**: Group related download links together (e.g., "Generated Reports" vs "System Files")
- **Descriptive Messages**: Provide helpful descriptions and messages for each download

## Component Parameters

### FilesUpload
```python
FilesUpload(
    label="Upload Files",            # Label displayed to the left of the component
    description="Upload files...",   # Text shown below the component
    placeholder="Choose files...",   # Placeholder text
    required=True,                   # Whether upload is required
    validation="/.*/",               # Validation pattern
)
```

### FileDownloadLink
```python
FileDownloadLink(
    label="Download Link",           # Label displayed to the left of the component
    description="Click to download", # Text shown below the component
    linkUrl="path/to/file.ext",     # Path to the file (relative or absolute)
    linkText="Download File",        # Text shown for the clickable link
    required=False,                  # Whether user must interact with this
    group="Default",                 # Group name for organizing components
    message="Download message"       # Additional message or tooltip
)
```

## Formula Workflow

1. **Screen 1 - File Upload**:
   - Display FilesUpload component
   - User selects and uploads files
   - Submits form to proceed

2. **Screen 2 - Processing & Download**:
   - Connect to RPC for real-time updates
   - Show processing progress:
     - Analyzing uploaded files
     - Generating CSV results
     - Creating PDF report
     - Saving execution log
   - Create FileDownloadLink components for each generated file
   - Present download form with organized links
   - Disconnect from RPC

## Example Files Demonstrated

The formula creates download links for three types of files:

1. **CSV Results** (`output/analysis_results.csv`)
   - Analysis results in comma-separated format
   - Group: "Generated Reports"

2. **PDF Report** (`reports/full_analysis.pdf`)
   - Comprehensive report with charts and graphs
   - Group: "Generated Reports"

3. **Execution Log** (`logs/execution.log`)
   - Detailed processing log for troubleshooting
   - Group: "System Files"

## Running the Example

```bash
cd examples/file_download
uv run python -m netmagus --script formula --input-file input.json \
    --token your_token --loglevel 1
```

## Files in This Example

- **formula.py**: Main formula logic with two-screen workflow
- **formula.json**: NetMagus formula metadata and configuration
- **pyproject.toml**: Python project dependencies
- **README.md**: This documentation file
