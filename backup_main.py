from Initial import DeviceConnection
from Initial import BackupManager

def main():
    """Main function to perform configuration backups."""
    try:
        # Initialize connection handler
        connection_handler = DeviceConnection()
        devices = connection_handler.load_devices()
        backup_manager = BackupManager()
        
        # Process each device
        for device in devices:
            try:
                if device["device_type"] == "cisco_ios":
                    device.pop("device_role", None)
                    device.pop("location", None)
                    connection = connection_handler.get_connection(device)
                    response = connection.send_command("show run")
                    hostname = connection.send_command("show version", use_textfsm=True)
                    device["hostname"] = hostname[0]["hostname"]   

                elif device["device_type"] == "arubo_os":
                    device.pop("device_role", None)
                    device.pop("location", None)
                    connection = connection_handler.get_connection(device)
                    response = connection.send_command("show run")
                    hostname = connection.send_command("show version", use_textfsm=True)
                    device["hostname"] = hostname[0]["hostname"]  
                     
                backup_manager.save_backup(device["hostname"], device["ip"], response)
                
            except Exception as e:
                continue

    except Exception as e:
        logging.error(f"Main process failed: {str(e)}")

if __name__ == "__main__":
    main()
