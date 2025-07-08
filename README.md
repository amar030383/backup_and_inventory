# Network Device Backup & Inventory Automation

This project automates configuration backups and inventory collection for network devices (e.g., Cisco IOS). It uses Netmiko for device connections and supports exporting inventory data to CSV.

## Folder Structure

```
backup_main.py                # Script to back up device configurations
update_inventory_main.py      # Script to export device inventory to CSV
Initial.py                    # Core classes for device connection, backup, and inventory
inventory.csv                 # Source inventory of devices (input)
automation_inventory.csv      # Generated inventory export (output)
network-backup/               # Folder for daily configuration backups
requirements.txt              # Python dependencies
.gitignore                    # Files/folders to ignore in git
```

## Requirements

- Python 3.8+
- See [requirements.txt](requirements.txt) for dependencies

Install dependencies:
```sh
pip install -r requirements.txt
```

## Usage

### 1. Prepare Device Inventory

Edit [inventory.csv](inventory.csv) with your device details (IP, type, etc.).

### 2. Set Environment Variables

Set credentials (or use defaults: `automation`):

```sh
export DEVICE_USERNAME=youruser
export DEVICE_PASSWORD=yourpass
export DEVICE_SECRET=yoursecret
```

### 3. Back Up Configurations

Run:
```sh
python backup_main.py
```
Backups are saved in `network-backup/YYYYMMDD/`.

### 4. Export Inventory

Run:
```sh
python update_inventory_main.py
```
Inventory is exported to `automation_inventory.csv`.

## Core Components

- [`DeviceConnection`](Initial.py): Loads devices from CSV and manages Netmiko connections.
- [`BackupManager`](Initial.py): Handles backup folder creation and saving configs.
- [`InventoryManager`](Initial.py): Merges device and show version data for inventory export.

## Notes

- Only devices with `device_type` set to `cisco_ios` or `arubo_os` are supported.
- Logging is enabled for troubleshooting.
- Example backup files are in `network-backup/YYYYMMDD/`.