# Lucid Lab

This repository contains Python scripts designed to automate various tasks related to managing Lucid accounts, users, and files.

## Table of Contents
  - [Scripts Overview](#scripts-overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Scripts Overview
Here’s a list of all the scripts in this repository along with their descriptions:

1. **[lucid_license_monitor.py](lucid_license_monitor.py)**: Searches for a specific Dropbox account using criteria like email or name.

## Requirements
- **Python 3.x**: Ensure that Python 3 is installed on your system.
- **Dropbox SDK**: Install the [Dropbox Python SDK](https://www.dropbox.com/developers/documentation/python) to interact with the Dropbox API.
- **API Keys**: You will need a Dropbox API token to authenticate API requests. Make sure the token has sufficient permissions to perform the required operations.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name/dropbox-automation-scripts.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Dropbox API tokens and other necessary credentials in environment variables:
   ```bash
   export DROPBOX_API_TOKEN="your-token-here"
   ```

## Usage
Run the desired script from the command line or integrate it into your existing automation workflows.

Example:
```bash
python3 dbox_search_account.py --email "user@example.com"
```

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the functionality or add new features.

## License
This project is licensed under the MIT License.
