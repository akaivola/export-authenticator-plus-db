# Encrypted SQLite Database Exporter

This script exports TOTP entries from an encrypted SQLite database (created by Authenticator Plus or a similar app) to individual OTPAuth URIs and ASCII QR codes.

## Requirements

- Python 3.6 or higher
- The required Python packages listed in `requirements.txt`
- SQLCipher library

## Installation

### General

1. Clone the repository or download the script.
2. Install the required Python packages:

pip install -r requirements.txt


### Mac M1 Users

1. Install the SQLCipher and SQLite libraries using Homebrew:
   `brew install sqlcipher sqlite`

2. Run the following command to install the required Python packages with the proper paths for SQLCipher:
`
SQLCIPHER_PATH=$(brew --prefix sqlcipher) LIBRARY_PATH=/lib C_INCLUDE_PATH=/include pip install -r requirements.txt
`

## Usage

1. Run the script:

`python decrypt.py <path_to_your_encrypted_database>`

2. Enter the passphrase for the encrypted database when prompted.
3. The script will display the OTPAuth URIs and corresponding ASCII QR codes for each TOTP entry.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


