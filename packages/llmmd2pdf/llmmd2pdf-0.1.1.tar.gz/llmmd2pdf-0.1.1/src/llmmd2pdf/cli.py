import subprocess
import sys
from pathlib import Path
import toml

def get_config_path():
    """
    Determines the standard configuration path for the current OS.
    Duplicate of logic in app.py to avoid complex imports before launch.
    """
    home = Path.home()
    if sys.platform == "darwin":
        return home / "Library" / "Application Support" / "llmmd2pdf" / "config.toml"
    elif sys.platform == "win32":
        return home / "AppData" / "Roaming" / "llmmd2pdf" / "config.toml"
    else:
        return home / ".config" / "llmmd2pdf" / "config.toml"

def main():
    """
    Entry point for the llmmd2pdf command.
    Launches the Shiny app using the installed package files.
    """
    # Locate the app.py relative to this file
    package_dir = Path(__file__).parent
    app_path = package_dir / "app.py"

    if not app_path.exists():
        print(f"Error: Could not find app.py at {app_path}")
        sys.exit(1)

    # --- Config / Port Loading ---
    config_file = get_config_path()
    port = 8000 # Default Shiny port
    
    if config_file.exists():
        try:
            config = toml.load(config_file)
            # CLI arguments override config, config overrides default
            port = config.get("port", 8000)
        except Exception as e:
            print(f"Warning: Could not read config for port setting: {e}")

    print(f"Starting llmmd2pdf on port {port}...")
    
    # Construct the shiny run command
    # We explicitly pass the port from the config
    cmd = ["shiny", "run", "--port", str(port), str(app_path)] + sys.argv[1:]

    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nStopping llmmd2pdf...")
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
