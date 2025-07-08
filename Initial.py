import os
import csv
from datetime import datetime
from netmiko import ConnectHandler
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class DeviceConnection:
    """Class to handle device connections using Netmiko."""
    
    def __init__(self):
        # Load authentication credentials from environment variables
        self.username = os.getenv("DEVICE_USERNAME", "automation")
        self.password = os.getenv("DEVICE_PASSWORD", "automation")
        self.secret = os.getenv("DEVICE_SECRET", "automation")
        
        if not all([self.username, self.password, self.secret]):
            raise ValueError("Missing required environment variables: DEVICE_USERNAME, DEVICE_PASSWORD, DEVICE_SECRET")

    def load_devices(self, csv_file: str = "inventory.csv"):
        """Load device information from CSV file."""
        devices = []
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ip_address = row.get("IP Address", "")
                    if ip_address:  
                        device = {
                            "ip": ip_address,
                            "username": self.username,
                            "password": self.password,
                            "secret": self.secret,
                            "device_role": row.get("device_role", ""),
                            "device_type": row.get("device_type",""),
                            "conn_timeout": 30,
                            "auth_timeout": 30,
                            'location': row.get("Location", ""),
                        }
                        devices.append(device)
        except FileNotFoundError:
            logging.error(f"Inventory file {csv_file} not found")
        except Exception as e:
            logging.error(f"Error reading inventory file: {str(e)}")
        return devices

    def get_connection(self, device_info):
        """Get a Netmiko connection object for the device."""
        try:
            device = {
                "device_type": device_info["device_type"],
                "ip": device_info["ip"],
                "username": device_info["username"],
                "password": device_info["password"],
                "secret": device_info["secret"],
                "conn_timeout": device_info["conn_timeout"],
                "auth_timeout": device_info["auth_timeout"],
            }
            connection = ConnectHandler(**device)
            connection.enable()  # Enter enable mode
            return connection
        except Exception as e:
            logging.error(f"Failed to connect to {device_info['ip']}: {str(e)}")
            raise

class BackupManager:
    """Class to manage configuration backups."""
    
    def __init__(self, backup_folder: str = "network-backup"):
        self.backup_folder = backup_folder
        self._create_backup_folder()

    def _create_backup_folder(self):
        """Create backup folder if it doesn't exist."""
        os.makedirs(self.backup_folder, exist_ok=True)

    def get_daily_backup_folder(self) -> str:
        """Get the daily backup folder path."""
        current_date = datetime.now().strftime("%Y%m%d")
        daily_folder = os.path.join(self.backup_folder, current_date)
        os.makedirs(daily_folder, exist_ok=True)
        return daily_folder

    def save_backup(self, hostname: str, ip: str, config: str) -> str:
        """Save configuration backup to file."""
        try:
            daily_folder = self.get_daily_backup_folder()
            filename = f"{hostname}_{ip}.txt"
            filepath = os.path.join(daily_folder, filename)
            
            with open(filepath, 'w') as f:
                f.write(config)
            
            logging.info(f"Backup saved for {hostname} ({ip})")
            return filepath
        except Exception as e:
            logging.error(f"Failed to save backup for {hostname} ({ip}): {str(e)}")
            raise

class InventoryManager:
    """Class to manage inventory updates."""
    
    def __init__(self, inventory_file: str = "automation_inventory.csv"):
        self.inventory_file = inventory_file    

    def update_inventory(self, device, show_version):
    
        # Flatten lists into strings
        for item in show_version:
            for key, value in item.items():
                if isinstance(value, list):
                    item[key] = ','.join(value)

        # Combine both dictionaries
        combined_data = {**device, **show_version[0]}
        return combined_data
