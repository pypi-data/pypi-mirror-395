import os
import json
import subprocess
import shutil
import sys
from pathlib import Path
home = Path.home()

# --- Configuration ---
# These files will be created in the directory where the user
# runs the command.
CONFIG_FILE = './build_config.json'
BUILD_ROOT_DIR = f"{home}/builds"  # Root directory where builds will be copied

# Map of software choices
SOFTWARE_MAP = {
    "1": "NDTkit UT",
    "2": "NDTkit RT",
    "3": "NDTkit ET",
    "4": "NDTkit IRT"
}
# ---------------------


def load_config():
    """Loads configuration from the JSON file if it exists."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Error: Config file '{CONFIG_FILE}' is corrupted. It will be reset.")
            os.remove(CONFIG_FILE)
            return None
    return None


def save_config(config):
    """Saves the configuration to the JSON file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        config_path = os.path.abspath(CONFIG_FILE)
        print(f"\nConfiguration successfully saved to: {config_path}")
        print("Please delete/edit this file if any configuration has changed")
    except IOError as e:
        print(f"Error saving configuration file: {e}")


def prompt_for_config():
    """Asks the user questions to generate the configuration."""
    print("Build configuration not found or incomplete. Please provide details.")

    # 1. Plugin Name
    default_plugin_name = os.path.basename(os.getcwd())
    plugin_name = input(f"\n1 - What's the plugin name (default=\"{default_plugin_name}\"): ")
    if not plugin_name:
        plugin_name = default_plugin_name

    # 2. Menu Name (optional)
    menu_name = input("\n2 - In which menu do you want to add this action? (leave empty if none): ").strip()
    menu_position = ""
    if menu_name:
        menu_position = input(f"   At which position in {menu_name} do you want to add this new action?: ").strip()

    # 3. Target Script
    target_script = input("\n4 - What is the main .py entry file? (default=\"./main.py\"): ")
    if not target_script:
        target_script = "./main.py"

    # 3. Target Software
    print("\n3 - Choose the target software:")
    for key, value in SOFTWARE_MAP.items():
        print(f"   {key} - {value}")

    software_choice = ""
    while software_choice not in SOFTWARE_MAP:
        software_choice = input(f"   Your choice (1-{len(SOFTWARE_MAP)}): ")
        if software_choice not in SOFTWARE_MAP:
            print(f"Error: Please choose a valid number.")

    target_software = SOFTWARE_MAP[software_choice]

    # 4. Version
    version = input("\n4 - Type the two first digit of the NDTkit version (default=\"4.1\"): ")
    if not version:
        version = "4.1"
    version = version[:3]  # recover only the three first characters

    config = {
        "plugin_name": plugin_name,
        "menu_name": menu_name,
        "menu_position": menu_position,
        "target_script": target_script,
        "target_software": target_software,
        "version": version
    }

    # Save the new configuration
    save_config(config)
    return config


def get_config():
    """
    Gets the configuration.
    Loads from file if it exists and is valid,
    otherwise prompts the user.
    """
    config = load_config()
    if config:
        # Check if all required keys are present
        required_keys = ['plugin_name', 'target_software', 'version', 'target_script']

        if all(key in config for key in required_keys):
            print(f"Configuration loaded from '{CONFIG_FILE}'.")
            print(f"  - Plugin: {config['plugin_name']}")
            menu_info = ""
            if config.get('menu_name') and config.get('menu_position'):
                menu_info = f" (Menu: {config['menu_name']}, Position: {config['menu_position']})"
            print(f"  - Menu Settings:{menu_info if menu_info else ' None'}")
            print(f"  - Target Script: {config['target_script']}")
            print(f"  - Software: {config['target_software']}")
            print(f"  - Version: {config['version']}")
            return config
        else:
            print(f"Configuration file '{CONFIG_FILE}' is incomplete or outdated.")
            # Fall through to prompt for new config

    return prompt_for_config()


def run_pyinstaller(plugin_name, target_script):
    """Runs PyInstaller to build the executable."""
    print("\n--- Running PyInstaller ---")

    # Check if the target script exists
    if not os.path.exists(target_script):
        print(f"ERROR: The target script '{target_script}' was not found.", file=sys.stderr)
        print(f"Please run this command in the same directory as your '{target_script}'.", file=sys.stderr)
        sys.exit(1)

    # PyInstaller command arguments:
    # --onefile: Create a single .exe file
    # --clean: Clean PyInstaller cache before building
    # --noconsole: (Optional) Don't open a console window.
    #              Remove this if your app is a console application.
    # --name: Set the name of the executable
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',
        '--clean',
        '--noconsole',
        '--hidden-import=py4j.java_collections',
        f'--name={plugin_name}',
        target_script
    ]

    print(f"Command: {' '.join(pyinstaller_cmd)}")

    try:
        # We use subprocess.run, and check=True ensures it
        # raises an error if PyInstaller fails
        subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        print("PyInstaller finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: PyInstaller failed.", file=sys.stderr)
        print(e.stdout)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("ERROR: 'pyinstaller' command not found.", file=sys.stderr)
        print("Please install it with: pip install pyinstaller", file=sys.stderr)
        sys.exit(1)


def copy_build(config):
    """Copies the generated executable to the destination folder."""
    print("\n--- Copying Build ---")

    plugin_name = config['plugin_name']
    target_software = config['target_software']
    version = config['version']

    # Build the final plugin name with menu information if provided
    if config.get('menu_name'):
        plugin_name = f"{plugin_name}__{config['menu_name']}"
    if config.get('menu_position'):
        plugin_name = f"{plugin_name}_{config['menu_position']}"

    # Path to the .exe generated by PyInstaller
    source_exe = os.path.join('dist', f"{config['plugin_name']}.exe")

    if not os.path.exists(source_exe):
        print(f"ERROR: Executable '{source_exe}' not found after build.", file=sys.stderr)
        sys.exit(1)

    version_suffix = target_software.split()[1]
    version_suffix = f"_{version_suffix}" if version_suffix != "UT" else ""
    # Create the destination path
    dest_dir = os.path.join(home, ".ndtkit", f"Conf_{version}{version_suffix}", "plugins")

    # Ensure the destination directory exists
    try:
        os.makedirs(dest_dir, exist_ok=True)
    except OSError as e:
        print(f"ERROR: Could not create destination directory "
              f"'{dest_dir}': {e}", file=sys.stderr)
        sys.exit(1)

    dest_file = os.path.join(dest_dir, f"{plugin_name}.exe")

    # Copy the file
    try:
        shutil.copy2(source_exe, dest_file)
        dest_path = os.path.abspath(dest_file)
        print(f"\nBuild complete and copied successfully to:")
        print(f"{dest_path}")
    except (shutil.Error, IOError) as e:
        print(f"ERROR: Could not copy file to destination: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function for the build script."""
    try:
        # 1. Get configuration
        config = get_config()

        # 2. Run the PyInstaller build
        run_pyinstaller(config['plugin_name'], config['target_script'])

        # 3. Copy the final build
        copy_build(config)

        print("\nBuild process completed.")

    except KeyboardInterrupt:
        print("\nBuild process cancelled by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
