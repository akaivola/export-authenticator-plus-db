import sys
import pysqlcipher3.dbapi2 as sqlite
from urllib.parse import quote
from getpass import getpass
import qrcode
from qrcode.console_scripts import main as qr_main

def generate_ascii_qr_code(data):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create a StringIO object to capture the output of qr.print_ascii
    # and return it as a string
    from io import StringIO
    buffer = StringIO()
    qr.print_ascii(out=buffer)
    return buffer.getvalue()

def get_unique_label(label, existing_labels, max_length=20):
    counter = 1
    first_word = label.split('-', 1)[0]  # Get the first word (split by dashes)
    
    if len(label) > max_length:
        label = first_word
    
    original_label = label
    while label in existing_labels:
        label = f"{original_label}-{counter}"
        counter += 1
    existing_labels.add(label)
    return label

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <database_path>")
        sys.exit(1)

    db_path = sys.argv[1]
    passphrase = getpass("Enter the passphrase: ")

    conn = sqlite.connect(db_path)
    conn.execute(f"PRAGMA key = '{passphrase}';")
    conn.execute("PRAGMA cipher_compatibility = 3;")
    conn.execute("PRAGMA kdf_iter = 64000;")
    conn.execute("PRAGMA cipher_page_size = 1024;")
    conn.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1;")
    conn.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1;")

    existing_labels = set()
    accounts = conn.execute("SELECT email, issuer, secret FROM accounts;").fetchall()

    for email, issuer, secret in accounts:
        label = email.replace(' ', '-')  # Replace spaces with dashes
        label = get_unique_label(label, existing_labels)
        label = quote(label)
        otpauth_uri = f"otpauth://totp/{label}?secret={secret}&issuer={issuer}"
        
        print(f"URI: {otpauth_uri}")
        
        ascii_qr = generate_ascii_qr_code(otpauth_uri)
        print(f"QR Code:\n{ascii_qr}")

if __name__ == "__main__":
    main()
