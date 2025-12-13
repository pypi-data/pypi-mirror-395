# mambo/cli.py
from pathlib import Path
from importlib import resources
from shutil import copytree
import sys
import json
import os
import runpy

def init_project(target: Path):
    """Initialize a MAMBOFRAME project in the target directory."""
    mambo_template = resources.files("mambo")
    print(f'\n\t\t- Installing MAMBOFRAME template to "{target}"...')
    copytree(mambo_template, target)
    actual_path = Path.cwd() # Obtener el directorio actual de trabajo. 
    
    # Generamos el JSON de configuración y metadatos.
    config = {
        "project_name": target.name,
        "project_path": str(target.resolve()),
        "version": "0.1.0-prealpha",
        "author": "Fernando Leguizamo (ElHaban3ro)",
        "description": "A MAMBOFRAME project.",
        "settings": {
        }
    }
    
    with open(target / "mambo_config.json", "w+") as config_file:
        config_file.write(json.dumps(config, indent=4))
    
    print('\n\t\t- MAMBOFRAME project initialized successfully.')

def load_config() -> dict:
    """Load the MAMBOFRAME project configuration from mambo_config.json."""
    config_path = Path.cwd() / "mambo_config.json"
    if not config_path.exists():
        print("Error: mambo_config.json not found in the current directory.")
        print(f"\n{'='*50}\n{'='*50}")
        sys.exit(1)
    
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    
    return config
    
def main():
    print(f"{'='*50}\n{'='*50}\n\tMAMBOFRAME (pre-alpha)\n{'='*50}\n{'='*50}\n")
    # Ejemplo sencillo: mamboframe --init
    args = sys.argv[1:] # Obtenemos los argumentos de la línea de comandos.
    if not args:
        print("To start a MAMBOFRAME project, use: mamboframe --init {OPTIONAL_PATH}")
        print(f"\n{'='*50}\n{'='*50}")
        sys.exit(1)

    # Si el argumento n1 es "--init", inicializamos el proyecto.
    if args[0] == "--init":
        if len(args) >= 2:
            target = Path.cwd() / Path(args[1]).name
        else:
            target = Path.cwd() / "my_mambo"
        
        init_project(target)
        print(f"\n{'='*50}\n{'='*50}")
        
    elif args[0] == "--start":
        print("Starting MAMBOFRAME Project...")
        configs = load_config()
        if 'project_path' in configs:
            project_path = configs['project_path']
            main_py_script = Path(project_path) / "main.py"
            
            if not main_py_script.exists():
                print(f"Error: main.py not found at {main_py_script}")
                sys.exit(1)

            runpy.run_path(str(main_py_script), run_name="__main__")
            print(f"\n{'='*50}\n{'='*50}")
            
        else:
            print("Error: 'project_path' not found in configuration.")
            print(f"\n{'='*50}\n{'='*50}")
            sys.exit(1)
    
    elif args[0] == "--help":
        print("MAMBOFRAME Help:\n--init {OPTIONAL_PATH}: Initialize a new MAMBOFRAME project.\n--start: Start the MAMBOFRAME project.\n--help: Show this help message.")
        print(f"\n{'='*50}\n{'='*50}")
    
    else:
        print(f"Unknown parameter: {args[0]}")
        print(f"{'='*50}\n{'='*50}")
        sys.exit(1)