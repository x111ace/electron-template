import os, json, time, shutil, argparse, subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(SCRIPT_DIR, ".pids.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "build.log")

# Colorama for colored terminal output
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    RRR = Style.RESET_ALL
    BRT = Style.BRIGHT
    DIM = Style.DIM
    RED = Fore.RED
    GRN = Fore.GREEN
    YLW = Fore.YELLOW
    BLU = Fore.BLUE
    MGN = Fore.MAGENTA
    CYN = Fore.CYAN
except ImportError:
    # Fallback for systems without colorama
    RRR = BRT = DIM = RED = GRN = YLW = BLU = MGN = CYN = ""

# Files and folders to exclude during cleaning and tree views
JSPROJECT_EXCLUDE = {".svelte-kit", "dist", "node_modules", "package-lock.json"}
PYPROJECT_EXCLUDE = {"__pycache__", "venv"}
RSPROJECT_EXCLUDE = {"target", "Cargo.lock"}
EXCLUDE_ALL = {"build.log", ".vscode", "dox"} | PYPROJECT_EXCLUDE | JSPROJECT_EXCLUDE | RSPROJECT_EXCLUDE

# Language extensions for project tree statistics
PROG_LANG_EXTS = {
    ".py": "Python", 
    ".ipynb": "Jupyter Notebook",
    ".rs": "Rust", 
    ".js": "JavaScript", 
    ".ts": "TypeScript", 
    ".c": "C",
    ".cpp": "C++", 
    ".h": "C/C++ Header", 
    ".java": "Java", 
    ".html": "HTML",
    ".css": "CSS", 
    ".sh": "Shell Script",
    ".svelte": "Svelte",
}

# --- Helper Functions ---

def _run_command(command: list[str], cwd: str, log_file_path: str, show_output: bool = True):
    """A centralized helper to run subprocess commands with real-time logging to console and file."""
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"\n--- Running Command: {' '.join(command)} ---\n")
            if show_output:
                print(f"{DIM}--- Running Command: {' '.join(command)} ---{RRR}")

            while True:
                line = process.stdout.readline()
                if not line:
                    break
                if show_output:
                    print(line, end='')
                log_file.write(line)
        
        return_code = process.wait()
        
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)

    except FileNotFoundError:
        print(f"{RED}Error: Command '{command[0]}' not found. Is it in your PATH?{RRR}")
        raise
    except subprocess.CalledProcessError as e:
        print(f"\n{RED}Error running command: {' '.join(command)}. Return code: {e.returncode}.{RRR}")
        print(f"{YLW}Check '{log_file_path}' for the complete log.{RRR}")
        raise e

# --- Core Functions ---

def project_tree(root_dir: str, output: bool = False) -> str:
    """Generates and optionally prints a complete file tree with statistics."""
    tree_lines = []
    stats = {"folders": 0, "files": {"total": 0, "by_type": {}}}

    def count_lines(path: str) -> int:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except (IOError, OSError):
            return 0

    def process_directory(dir_path: str, prefix: str = ""):
        """Recursively process a directory to build the tree."""
        try:
            entries = sorted(os.listdir(dir_path), key=lambda e: (os.path.isfile(os.path.join(dir_path, e)), e.lower()))
        except OSError:
            return
        
        entries = [e for e in entries if e not in EXCLUDE_ALL]
        
        for i, entry in enumerate(entries):
            path = os.path.join(dir_path, entry)
            connector = "└── " if i == len(entries) - 1 else "├── "
            
            if os.path.isdir(path):
                stats["folders"] += 1
                tree_lines.append(f"{prefix}{connector}{BRT}{BLU}{entry}{RRR}/")
                extension = "    " if i == len(entries) - 1 else "│   "
                process_directory(path, prefix + extension)
            else:
                stats["files"]["total"] += 1
                ext = os.path.splitext(entry)[1]
                lang = PROG_LANG_EXTS.get(ext)
                lines = count_lines(path)
                
                if lang:
                    lang_stats = stats["files"]["by_type"].setdefault(lang, {'files': 0, 'lines': 0})
                    lang_stats['files'] += 1
                    lang_stats['lines'] += lines
                
                tree_lines.append(f"{prefix}{connector}{entry} :: {GRN}{lines}{RRR} lines")

    abs_root = os.path.abspath(root_dir)
    root_label = f"{BLU}{os.path.basename(abs_root.rstrip(os.sep))}{RRR}/"
    tree_lines.append(root_label)
    process_directory(abs_root)
    
    file_tree_str = "\n".join(tree_lines)
    if output:
        print(json.dumps(stats, indent=4))
        print(file_tree_str)
    
    return file_tree_str

def clean_project(root_dir: str, output: bool = False):
    """Walks the root directory and removes files/folders with an optimized strategy."""
    if output:
        print(f"{CYN}Preparing to clean project...{RRR}")
    
    stop_dev_servers(root_dir, output)
    
    # Efficiently find all items to be cleaned, without descending into excluded directories.
    paths_to_remove = []
    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Prune the directories list in-place to prevent os.walk from descending into them.
        # We iterate over a copy of dirs `list(dirs)` because we modify it.
        for d in list(dirs):
            if d in EXCLUDE_ALL:
                full_path = os.path.join(root, d)
                paths_to_remove.append(full_path)
                dirs.remove(d)  # This is the key optimization

        # Add any matching files from the current directory.
        for f in files:
            if f in EXCLUDE_ALL:
                paths_to_remove.append(os.path.join(root, f))

    if not paths_to_remove:
        if output:
            print(f"{GRN}Project is already clean. No items to remove.{RRR}")
        return

    # Separate paths into files and directories
    files_to_delete = []
    dirs_to_delete = []
    for p in paths_to_remove:
        if os.path.isfile(p):
            try:
                files_to_delete.append({'path': p, 'size': os.path.getsize(p)})
            except OSError:
                continue 
        elif os.path.isdir(p):
            dirs_to_delete.append({'path': p})

    # As requested, sort files by size (smallest to largest)
    files_to_delete.sort(key=lambda f: f['size'])
    
    # The final list for deletion: files first, then directories.
    items_to_clean = [f['path'] for f in files_to_delete] + [d['path'] for d in dirs_to_delete]

    if output:
        print(f"{YLW}The following items will be removed (files first, then folders):{RRR}")
        for item in items_to_clean:
            if os.path.exists(item):
                print(f"  - {item}")
            
    for item_path in items_to_clean:
        if not os.path.exists(item_path):
            continue
        for attempt in range(3):
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                elif os.path.isfile(item_path):
                    os.remove(item_path)
                if output:
                    print(f"{GRN}Removed: {item_path}{RRR}")
                break
            except OSError as e:
                if attempt < 2:
                    if output:
                        print(f"{YLW}Could not remove {item_path}, retrying... ({e}){RRR}")
                    time.sleep(2)
                else:
                    if output:
                        print(f"{RED}Failed to remove {item_path}: {e}{RRR}")

def stop_dev_servers(root_dir: str, output: bool = False):
    """Stops running development servers by aggressively cleaning up lingering processes."""
    if output:
        print(f"{CYN}Stopping any running development servers...{RRR}")

    # Aggressive cleanup of common lingering processes by name
    lingering_processes = ["electron.exe", "node.exe", "electronmon.exe", "vite.exe"]
    for proc_name in lingering_processes:
        try:
            # Use capture_output=True to prevent taskkill from printing to console
            subprocess.run(["taskkill", "/F", "/IM", proc_name], check=False, capture_output=True)
            if output:
                print(f"{DIM}Attempted graceful shutdown of {proc_name}{RRR}")
        except FileNotFoundError:
            # This handles non-Windows environments where taskkill doesn't exist.
            break 
    
    if os.path.exists(PID_FILE):
        try:
            os.remove(PID_FILE)
        except OSError:
            pass # Not critical if it fails.
    
    if output:
        print(f"{CYN}Waiting for processes to terminate fully...{RRR}")
    time.sleep(3) # A brief pause to allow OS to release file handles.

# --- Project Lifecycle Functions ---

def install_dependencies(root_dir: str, output: bool = False):
    """Installs npm dependencies if the node_modules directory is not present."""
    node_modules_path = os.path.join(root_dir, 'node_modules')
    if os.path.exists(node_modules_path):
        if output:
            print(f"{GRN}Dependencies already exist. Skipping 'npm install'.{RRR}")
        return

    if output:
        print(f"{CYN}Dependencies not found. Installing... (this may take a moment){RRR}")
    # Don't show verbose output for npm install by default. The log file has it.
    _run_command(["npm.cmd", "install"], root_dir, LOG_FILE, show_output=False)
    if output:
        print(f"{GRN}Dependencies installed successfully.{RRR}")

def build_project(root_dir: str, output: bool = False):
    """Builds the project for production."""
    if output:
        print(f"{CYN}Building project for production...{RRR}")
    # Clear log file only if it gets too big
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 5 * 1024 * 1024: # 5MB
        with open(LOG_FILE, 'w') as f:
            f.write("Log file cleared due to size.\n")
            
    _run_command(["npm.cmd", "run", "build"], root_dir, LOG_FILE, show_output=output)

    # --- Verification Step ---
    preload_path = os.path.join(root_dir, 'dist', 'main', 'preload.js')
    if not os.path.exists(preload_path):
        if output:
            print(f"{RED}CRITICAL ERROR: 'preload.js' was not created by the build process.{RRR}")
            print(f"{YLW}Please check '{LOG_FILE}' for TypeScript compilation errors for 'preload.ts'.{RRR}")
        raise FileNotFoundError("Build process failed to create critical file: preload.js")

    if output:
        print(f"{GRN}Production build completed successfully.{RRR}")


def start_dev_servers(root_dir: str, output: bool = False):
    """Launches the development server and keeps the script running."""
    if output:
        print(f"\n{BRT}{CYN}--- Starting Development Environment ---{RRR}")
        print(f"{YLW}The server is now running and watching for file changes.{RRR}")
        print(f"{YLW}Press Ctrl+C in this terminal to stop the server.{RRR}")
    
    _run_command(["npm.cmd", "run", "dev"], root_dir, LOG_FILE, show_output=output)
    
    if output:
        print(f"\n{GRN}Development server process ended.{RRR}")


def init_project(ROOT, output=False):
    """
    Initializes the project fully by ensuring servers are stopped,
    installing dependencies, running an initial build, and then 
    starting the live development servers.
    """
    if output:
        print(f"{BRT}{MGN}--- Initiating Full Project Setup ---{RRR}")
    
    # 0. Stop any lingering dev servers to ensure a clean start.
    stop_dev_servers(ROOT, output)
    
    # 1. Install dependencies if needed.
    install_dependencies(ROOT, output)
    
    # 2. Run a one-time build to generate initial dist files.
    build_project(ROOT, output)
    
    # 3. Start the live development servers for hot reloading.
    start_dev_servers(ROOT, output)

    if output:
        print(f"{BRT}{GRN}--- Project setup complete. Happy coding! ---{RRR}")

# --- Main Execution Block ---

def main():
    """Parses command-line arguments and executes the corresponding function."""
    parser = argparse.ArgumentParser(
        description="A utility script for managing your Electron/SvelteKit project.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-t", "--tree", action="store_true", help="Display the project's file tree with statistics.")
    parser.add_argument("-c", "--clean", action="store_true", help="Clean all build artifacts and dependencies.")
    parser.add_argument("-x", "--stop", action="store_true", help="Stop any running development servers.")
    parser.add_argument("-f", "--deps", action="store_true", help="Clean and reinstall all npm dependencies.")
    parser.add_argument("-b", "--build", action="store_true", help="Build the project for production.")
    parser.add_argument("-d", "--dev", action="store_true", help="Start the live development server.")
    parser.add_argument("-i", "--init", action="store_true", help="Initialize the project fully (clean, deps, build, dev).")
    
    args = parser.parse_args()

    if args.tree:
        project_tree(SCRIPT_DIR, output=True)
    elif args.clean:
        clean_project(SCRIPT_DIR, output=True)
    elif args.stop:
        stop_dev_servers(SCRIPT_DIR, output=True)
    elif args.deps:
        print(f"{BRT}{CYN}--- Force Reinstalling Dependencies ---{RRR}")
        clean_project(SCRIPT_DIR, output=True)
        install_dependencies(SCRIPT_DIR, output=True)
    elif args.build:
        build_project(SCRIPT_DIR, output=True)
    elif args.dev:
        start_dev_servers(SCRIPT_DIR, output=True)
    elif args.init:
        try:
            init_project(SCRIPT_DIR, output=True)
        except KeyboardInterrupt:
            print(f"\n{YLW}KeyboardInterrupt detected. Stopping development servers...{RRR}")
            stop_dev_servers(SCRIPT_DIR, output=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print(f"\n{RED}Project initialization failed: {e}{RRR}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()