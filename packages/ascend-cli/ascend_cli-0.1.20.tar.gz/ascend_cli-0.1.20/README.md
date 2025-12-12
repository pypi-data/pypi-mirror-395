# Ascend CLI

Ascend is a command-line interface (CLI) tool designed for robust and efficient data management tasks, including large-scale file migrations and database backups to Google Cloud Storage (GCS).

## Features

- **Files Module**:
  - Scan massive directories to create a file index.
  - Migrate files to GCS with stateful progress tracking, ensuring resumability.
  - High-performance parallel processing for fast uploads.
- **SQL Module**:
  - Backup and restore MySQL databases using `mydumper`/`myloader`.
  - Seamlessly compress and upload database backups to GCS.
- **Unified Configuration**:
  - Manage all settings through a central `config.conf` file.
  - Override any configuration setting with command-line flags for maximum flexibility.

## Installation

1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd <repo-directory>
    ```

2.  Install the tool in editable mode. It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -e .
    ```

## Configuration

The tool uses a `config.conf` file in the project root for configuration. You can use the provided `config.conf` as a template.

```ini
[files]
source_dir = /path/to/your/large/disk
gcs_bucket_name = your-file-migration-bucket
gcs_target_prefix = optional/path/in/bucket

# Number of parallel processes for the 'scan' command. Defaults to the number of CPU cores.
scan_workers = 4

# Max concurrent tasks for the 'migrate' command (I/O-bound).
max_concurrency = 1000

[sql]
gcs_bucket_name = your-db-backup-bucket
gcs_target_prefix = optional/path/in/bucket/for/sql
host = 127.0.0.1
user = db_user
password = db_password
db_name = your_database

# Number of threads for mydumper to use during backup.
threads = 4
```

Any setting in this file can be overridden by a corresponding command-line flag (e.g., `--source`, `--gcs-target-prefix`).

## Usage

### Files Migration

1.  **Scan a directory:**
    ```bash
    ascend files scan --source /path/to/data
    ```
    *(This will create an index file at `logs/migration_index.txt`)*

2.  **Migrate the files to GCS:**
    ```bash
    ascend files migrate --bucket your-gcs-bucket
    ```
    *(This will read the index and progress files from the `logs/` directory)*

---

### Running Long-Lived Processes (Detached Mode with `tmux`)

For long-running tasks like `files migrate`, it is critical to ensure the process continues even if you disconnect from your SSH session. The recommended way to achieve this is by using a terminal multiplexer like `tmux`.

`tmux` creates a persistent session on your server that you can safely detach from and reattach to later.

**1. Start a New `tmux` Session:**

Give your session a descriptive name.

```bash
tmux new -s ascend_migration
```

Your terminal will now be inside the new `tmux` session.

**2. Run the Command:**

Start the migration process as you normally would.

```bash
ascend files migrate
```

The migration will start, and you will see the live output and progress bar.

**3. Detach from the Session:**

You can now safely detach, leaving the process running in the background. Press the key combination:

**`Ctrl+b`** then **`d`**

You will be returned to your normal shell, and you will see a `[detached (from session ascend_migration)]` message. You can now safely log out of your SSH connection.

**4. Reattach to the Session:**

To check on the progress of your migration, SSH back into your server and reattach to the session:

```bash
tmux attach -t ascend_migration
```

You will be dropped right back into the session, viewing the live output of your command as if you never left. 