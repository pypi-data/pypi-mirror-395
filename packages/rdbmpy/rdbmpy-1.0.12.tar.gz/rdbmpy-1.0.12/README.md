# rdbmpy — Database migrations for Python

rdbmpy is a lightweight CLI tool to create, apply and rollback SQL migration files across multiple databases (PostgreSQL, MySQL, SQLite and SQL Server).

It works with plain SQL files (no ORM required). Each migration file should contain an UP section (applied) and a DOWN section (rollback), separated by the marker `=====DOWN`.

## Python compatibility

- **Tested with:** Python 3.10, 3.9
- **Compatibility:** Python 3.8 may work, but packages that require compilation (e.g. `pymssql`) might need additional build steps.
- **Recommendation:** use Python >= 3.9 to avoid build and dependency issues.

Note for builds on Python 3.8 (when necessary):

Before installing dependencies, create and activate a virtualenv and pre-install compatible build dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools wheel
# pre-install a compatible setuptools_scm required by some build backends
pip install "setuptools_scm[toml]>=5.0,<9.0"
pip install -r requirements.txt
```

This step avoids conflicts such as `setuptools_scm==9.2.2 is incompatible with setuptools_scm[toml]>=5.0,<9.0` that can occur when building packages from sdist.

## Quickstart

Install from PyPI:

```sh
pip install rdbmpy
```

Initialize a project (creates `migrations/` and the migrations table in the DB):

```sh
rdbmpy setup --driver pgsql --dbstring="user:password@localhost:5432/mydb"
```

Create a migration:

```sh
rdbmpy create --driver pgsql --migration_name add_users_table
```

Edit the file under `migrations/` and add your UP SQL, then `=====DOWN` and the rollback SQL.

Apply pending migrations:

```sh
rdbmpy exec --driver pgsql --dbstring="user:password@localhost:5432/mydb"
```

Rollback a migration (provide the migration file name or identifier):

```sh
rdbmpy rollback --driver pgsql --migration_name=20251208113351_add_users_table --dbstring="user:password@localhost:5432/mydb"
```

## Configuration

You can provide your connection string either with the environment variable `DATABASE_MIGRATION_URL` or with `--dbstring` on each command.

Environment variable example:

```sh
export DATABASE_MIGRATION_URL="user:password@localhost:5432/mydb"
```

Or use a `.env` file in your project root:

```env
DATABASE_MIGRATION_URL=user:password@localhost:5432/mydb
```

`--dbstring` takes precedence for the single command invocation.

## Commands overview

- `rdbmpy setup --driver <driver> [--dbstring]` — create `migrations/` and ensure the migrations table exists.
- `rdbmpy create --driver <driver> --migration_name <name>` — create a new migration file.
- `rdbmpy exec|execute --driver <driver> [--dbstring]` — apply all pending migrations.
- `rdbmpy rollback --driver <driver> --migration_name <name> [--dbstring]` — execute the DOWN section for the specified migration.

Notes:

- `--driver` must be one of `pgsql`, `mysql`, `sqlite`, `sqlserver`.
- `--migration_name` is required for `create` and `rollback`. It is not used by `exec`.

## Examples (consistent)

PostgreSQL

```sh
# create
rdbmpy create --driver pgsql --migration_name add_users_table --dbstring="user:password@localhost:5432/testdb"

# exec
rdbmpy exec --driver pgsql --dbstring="user:password@localhost:5432/testdb"

# rollback
rdbmpy rollback --driver pgsql --migration_name=20251208113351_add_users_table --dbstring="user:password@localhost:5432/testdb"
```

MySQL

```sh
# create
rdbmpy create --driver mysql --migration_name add_users_table --dbstring="user:password@localhost:3306/testdb"

# exec
rdbmpy exec --driver mysql --dbstring="user:password@localhost:3306/testdb"

# rollback
rdbmpy rollback --driver mysql --migration_name=20251208120251_add_users_table --dbstring="user:password@localhost:3306/testdb"
```

SQL Server

```sh
# create
rdbmpy create --driver sqlserver --migration_name add_users_table --dbstring="sa:Your_password123@localhost:1433/testdb"

# exec
rdbmpy exec --driver sqlserver --dbstring="sa:Your_password123@localhost:1433/testdb"

# rollback
rdbmpy rollback --driver sqlserver --migration_name=20251208121019_add_users_table --dbstring="sa:Your_password123@localhost:1433/testdb"
```

SQLite (file)

```sh
# create
rdbmpy create --driver sqlite --migration_name add_users_table --dbstring="/absolute/path/to/sqlite.db"

# exec
rdbmpy exec --driver sqlite --dbstring="/absolute/path/to/sqlite.db"

# rollback
rdbmpy rollback --driver sqlite --migration_name=20251208120000_add_users_table --dbstring="/absolute/path/to/sqlite.db"
```

## Migration file format

Use `=====DOWN` to separate apply/rollback parts. The UP section is applied; the DOWN section is used for rollback.

Example migration file:

```sql
-- UP
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

=====DOWN

DROP TABLE users;
```

## SQL Server ODBC setup (Ubuntu/Debian)

If you use SQL Server, install the Microsoft ODBC driver and `pyodbc` (requires system packages):

```sh
# Add Microsoft GPG key to a keyring
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /usr/share/keyrings/microsoft.gpg > /dev/null

# Add Microsoft package source and reference the keyring
curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo sed -i 's|deb |deb [signed-by=/usr/share/keyrings/microsoft.gpg] |' /etc/apt/sources.list.d/mssql-release.list

sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Install pyodbc via extra
pip install rdbmpy[sqlserver]
```

## Troubleshooting

- If a migration fails, copy the failing SQL and run it directly in your DB client to inspect detailed errors.
- For connection issues verify the `--dbstring` format or `DATABASE_MIGRATION_URL` value.
- SQL Server: ensure `msodbcsql18` and `unixodbc-dev` are installed and `pyodbc` is available in your Python environment.

## Contributing

Contributions are welcome. Open an issue or submit a PR. Add tests for new features and follow existing code style.

## License

See `LICENSE.txt`.

Forked from [py-migrate-db](https://github.com/indicoinnovation/py-migrate-db)