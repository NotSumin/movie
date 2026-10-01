import os
import subprocess
import sys

# --- CONFIGURATION ---
SUBFOLDER_NAME = "scripts"

# Define your exact execution order here
SCRIPT_ORDER = [
    "seed_movies.py",
    "seed_movies_extra.py",
    "fetch_movies_tmdb.py",
    "fetch_stills_tmdb.py",
    "update_posters.py",
    "seed_stills.py",
    "seed_trailers.py",
    "update_trailers.py",
    "seed_reviews.py",
    "seed_theaters.py",
    "notice_seed.py",
    "seed_question.py"
]


# ---------------------

def run_command(command, cwd=None, env=None):
    """Runs a CLI command and returns True if successful, False otherwise."""
    print(f"Running: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, text=True, cwd=cwd, env=env)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error occurred while executing: {' '.join(command)}")
        return False


def main():
    root_dir = os.getcwd()  # Top-level 'movie/' folder
    print("🚀 Starting Pipeline...")
    print("--------------------------------------------------")

    # 1. Install dependencies from requirements.txt
    requirements_path = os.path.join(root_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        print("📦 Found requirements.txt. Installing dependencies...")
        # sys.executable ensures it installs packages to the active virtual environment
        if not run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=root_dir):
            print("❌ Dependency installation failed. Aborting pipeline.")
            sys.exit(1)
    else:
        print("ℹ️ No requirements.txt found in the root folder. Skipping installation.")

    print("\n--------------------------------------------------\n")

    # 2. Run 'flask db migrate' with an automatic fallback mechanism
    print("🔄 Attempting to generate database migration...")
    migrate_cmd = ["flask", "db", "migrate", "-m", "Auto-migration via script"]
    upgrade_cmd = ["flask", "db", "upgrade"]

    if not run_command(migrate_cmd):
        print("\n⚠️ Migration generation failed. Running fallback recovery sequence...")
        print("🔧 Step A: Syncing database with existing migrations first (flask db upgrade)...")

        if not run_command(upgrade_cmd):
            print("❌ Fallback Step A failed. Database upgrade broke. Aborting pipeline.")
            sys.exit(1)

        print("\n🔧 Step B: Retrying migration generation (flask db migrate)...")
        if not run_command(migrate_cmd):
            print("❌ Fallback Step B failed. Migration still cannot be generated. Aborting pipeline.")
            sys.exit(1)

        print("\n🔧 Step C: Applying the newly generated migration (flask db upgrade)...")
        if not run_command(upgrade_cmd):
            print("❌ Fallback Step C failed. New upgrade broke. Aborting pipeline.")
            sys.exit(1)

        print("✨ Fallback recovery successful! Database is fully up to date.")
    else:
        # If the very first migrate command succeeded, we still need to run the normal upgrade
        print("\n✨ Migration generated successfully. Applying schema updates...")
        if not run_command(upgrade_cmd):
            print("❌ Database upgrade failed. Aborting pipeline.")
            sys.exit(1)

    print("\n--------------------------------------------------\n")

    # 3. Locate and execute scripts in the subfolder
    root_dir = os.getcwd()  # This is the top-level 'movie/' folder
    subfolder_path = os.path.join(root_dir, SUBFOLDER_NAME)

    if not os.path.exists(subfolder_path) or not os.path.isdir(subfolder_path):
        print(f"❌ Subfolder '{SUBFOLDER_NAME}' not found. Pipeline finished early.")
        sys.exit(1)

    if not SCRIPT_ORDER:
        print("ℹ️ The SCRIPT_ORDER list is empty. No additional scripts to run.")
        return

    # --- THE FIX ---
    # Copy the current environment and add the root folder to PYTHONPATH.
    # This allows the subfolder scripts to successfully do: from movie import my_function
    script_env = os.environ.copy()
    existing_pythonpath = script_env.get("PYTHONPATH", "")
    script_env["PYTHONPATH"] = f"{root_dir}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else root_dir
    # ---------------

    print(f"📂 Executing {len(SCRIPT_ORDER)} script(s) in your defined order...")

    for file_name in SCRIPT_ORDER:
        file_path = os.path.join(subfolder_path, file_name)

        if not os.path.exists(file_path):
            print(f"❌ Error: Script '{file_name}' listed in SCRIPT_ORDER was not found in '{SUBFOLDER_NAME}'.")
            sys.exit(1)

        print(f"\n▶️ Starting: {file_name}")

        # We pass 'script_env' here so the script knows where to find the 'movie' module
        if not run_command([sys.executable, file_name], cwd=subfolder_path, env=script_env):
            print(f"❌ Pipeline halted because {file_name} failed.")
            sys.exit(1)

    print("\n✅ Migration, upgrade, and all specified scripts completed successfully!")


if __name__ == "__main__":
    main()