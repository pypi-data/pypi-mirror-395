import os
import sys
import stat
import glob
import json
import logging
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.ssh_exception import SSHException, AuthenticationException

base_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(base_dir, "common")
if not os.path.isdir(common_dir):
    # go up one level to find "common" (for installed package structure)
    base_dir = os.path.dirname(base_dir)
    common_dir = os.path.join(base_dir, "common")

if os.path.isdir(common_dir) and base_dir not in sys.path:
    sys.path.insert(0, base_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Constants
SOURCE_DIR = "./export"


def check_csv_files_exist() -> list:
    csv_files = glob.glob(f"{SOURCE_DIR}/*.csv")
    if not csv_files:
        logging.info(f"No CSV files found in {SOURCE_DIR}")
        sys.exit(1)
    return csv_files

def validate_private_key(key_path: str) -> None:
    if not os.path.isfile(key_path):
        logging.error(f"SSH private key not found: {key_path}")
        sys.exit(1)
    os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)  # chmod 600

def sftp_transfer(
    host: str, port: int, username: str, remote_dir: str,
    files: list, password: str | None = None, key_path: str | None = None
) -> bool:
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())

    try:
        if password:
            logging.info(f"Using password-based authentication with username {username}")
            ssh_client.connect(hostname=host, port=port, username=username, password=password)
        else:
            logging.info(f"Using SSH key-based authentication with key {key_path}")
            validate_private_key(key_path)
            key = RSAKey.from_private_key_file(key_path)
            ssh_client.connect(hostname=host, port=port, username=username, pkey=key)

        sftp = ssh_client.open_sftp()

        try:
            sftp.chdir(remote_dir)
        except IOError:
            logging.error(f"Remote base directory {remote_dir} does not exist.")
            return False

        for file_path in files:
            filename = os.path.basename(file_path)
            logging.info(f"Uploading {filename}...")
            sftp.put(file_path, filename)

        sftp.close()
        ssh_client.close()
        return True

    except AuthenticationException:
        logging.error("Authentication failed: check credentials or key")
        return False
    except SSHException as e:
        logging.error(f"SFTP transfer failed: {e}")
        return False

def delete_local_files(files: list) -> None:
    for file in files:
        try:
            os.remove(file)
        except OSError:
            logging.warning(f"Could not delete file: {file}")

def main():
    # Load configuration from config.json
    config = json.load(open(os.path.join(common_dir, "config.json")))
    
    host = config.get("SFTP_HOST")
    if not host:
        logging.error("Missing required configuration: SFTP_HOST")
        sys.exit(1)
    
    port_str = config.get("SFTP_PORT", "22")
    try:
        port = int(port_str)
    except ValueError:
        logging.error(f"Invalid SFTP_PORT value: {port_str}")
        sys.exit(1)
    
    user = config.get("SFTP_USER")
    if not user:
        logging.error("Missing required configuration: SFTP_USER")
        sys.exit(1)
    
    remote_dir = config.get("SFTP_DIR")
    if not remote_dir:
        logging.error("Missing required configuration: SFTP_DIR")
        sys.exit(1)
    
    password = config.get("SFTP_PASSWORD")  # Optional
    key_path = config.get("SFTP_KEY_PATH")  # Optional

    csv_files = check_csv_files_exist()

    logging.info(f"Starting SFTP transfer to {host}:{port}/{remote_dir}")
    success = sftp_transfer(
        host=host,
        port=port,
        username=user,
        remote_dir=remote_dir,
        files=csv_files,
        password=password,
        key_path=None if password else key_path
    )

    if success:
        logging.info("SFTP transfer successful")
        logging.info("Deleting transferred files from export folder...")
        delete_local_files(csv_files)
        logging.info("SFTP transfer and cleanup completed successfully")
        sys.exit(0)
    else:
        logging.error("SFTP transfer failed - files retained in export folder")
        sys.exit(1)

if __name__ == "__main__":
    main()