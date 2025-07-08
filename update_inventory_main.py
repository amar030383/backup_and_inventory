import csv
import logging
from Initial import DeviceConnection
from Initial import InventoryManager

def main():
    """Main function to perform configuration backups and inventory export."""

    try:
        # Define the desired CSV columns and their order
        fieldnames = [
            "ip", "hostname", "device_type",
            "software_image", "version",
            "running_image", "hardware", "serial", "mac_address"
        ]


        with open('automation_inventory.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            # Initialize connection and inventory handlers
            connection_handler = DeviceConnection()
            devices = connection_handler.load_devices()
            inventory_manager = InventoryManager()

            for device in devices:
                try:
                    # Remove optional keys not needed for connection
                    device.pop("device_role", None)
                    device.pop("location", None)

                    # Establish connection and collect show version
                    connection = connection_handler.get_connection(device)
                    show_version = connection.send_command("show version", use_textfsm=True)

                    # Collect inventory data
                    data = inventory_manager.update_inventory(device, show_version)

                    mapped_data = {field: data.get(field, '') for field in fieldnames}

                    writer.writerow(mapped_data)

                except Exception as e:
                    logging.warning(f"Failed to process device {device.get('ip', 'UNKNOWN')}: {e}")
                    continue

    except Exception as e:
        logging.error(f"Main process failed: {str(e)}")

if __name__ == "__main__":
    main()
