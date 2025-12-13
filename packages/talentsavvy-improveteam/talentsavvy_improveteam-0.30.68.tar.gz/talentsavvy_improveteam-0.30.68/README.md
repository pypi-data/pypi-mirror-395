# TalentSavvy ImproveTeam

Scripts for data extraction scripts from software development systems

## Installation

Install the package using pip:

```bash
pip install talentsavvy-improveteam
```

That's it! The package is published on PyPI, so no special index URLs or authentication is required.

This will automatically install all required dependencies:
- paramiko
- pytz
- python-dateutil
- pandas
- requests
- urllib3

### Viewing Package Information

To view package information including installation location:
```bash
pip show talentsavvy-improveteam
```

This displays:
- Package metadata (version, author, etc.)
- Installation location (Location field)
- Required dependencies
- Entry points (available commands)

### Accessing This Documentation

The full README documentation is available in several ways:

1. **PyPI Website**: View the package page at https://pypi.org/project/talentsavvy-improveteam/
   - The README content is displayed automatically on the package page

2. **Using pip**: The `pip show` command displays basic package information including location and dependencies

3. **Package Metadata**: The README is included in the package's metadata (as `long_description`)

4. **Installed Files**: After installation, the README can be found at:
   ```bash
   <site-packages>/talentsavvy_improveteam-<version>.dist-info/metadata.json
   ```
   Or view the raw README content:
   ```bash
   python -c "import pkg_resources; print(pkg_resources.get_distribution('talentsavvy-improveteam').get_metadata('DESCRIPTION.rst'))"
   ```

## Configuration

The package includes a sample `config.json` file that contains the configuration template.

### Finding the Package Location

To locate where the package files are installed, use the following command to get the Location:

```
pip show talentsavvy-improveteam
```

The `config.json` file is installed at:
```
<site-packages>/common/config.json
```

Where `<site-packages>` is typically:
- **Windows**: `C:\Python<version>\Lib\site-packages\` (system-wide) or `C:\Users\<username>\AppData\Local\Programs\Python\Python<version>\Lib\site-packages\` (user installation)
- **Linux/macOS**: `/usr/local/lib/python<version>/site-packages/` (system-wide) or `~/.local/lib/python<version>/site-packages/` (user installation)

### Setup Instructions

1. **Update `config.json`** with your specific configuration values for each data source you plan to use.

2. Refer to each extraction script's documentation for the specific configuration keys it requires.

## Usage

After installing the package, you can run the data extraction scripts from the command line.

### Running Data Extraction Scripts

Each extraction script can be run with the following syntax:

```bash
extract_<source> -s <start_date>
```

Where `<source>` is one of:
- `jira` - Jira work item events
- `gitlab` - GitLab code events
- `github` - GitHub pull request events
- `github_actions` - GitHub Actions workflow events
- `jenkins` - Jenkins build events
- `azuredevops_boards` - Azure DevOps work item events
- `azuredevops_pipelines` - Azure DevOps pipeline events
- `azuredevops_repos` - Azure DevOps repository events
- `bitbucket_repos` - Bitbucket repository events
- `bitbucket_pipelines` - Bitbucket pipeline events
- `octopus` - Octopus Deploy deployment events

And `<start_date>` is optional and should be in `YYYY-MM-DD` format.

### Examples

**Extract Jira work items:**
```bash
extract_jira -s 2025-04-01
```

**Extract GitLab code events:**
```bash
extract_gitlab -s 2025-04-01
```

**Extract Jenkins builds:**
```bash
extract_jenkins -s 2025-04-01
```

If no start date is provided, the scripts will use the last checkpoint date (if available) or a default date.

### Output

The extracted data will be saved as CSV files in the directory specified by the `EXPORT_PATH` key in your `config.json` file (default: `./export` directory).

Each script maintains a checkpoint file to track the last extraction timestamp, allowing for incremental extractions on subsequent runs.

### SFTP Upload

After extraction, you can upload the CSV files to an SFTP server:

```bash
sftp_upload
```

This will upload all CSV files from the export directory to the configured SFTP server and delete them locally after successful upload.


