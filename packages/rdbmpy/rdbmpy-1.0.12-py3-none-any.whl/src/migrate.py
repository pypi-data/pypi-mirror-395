import argparse
from asyncio import constants
import os
import logging
import sys

from datetime import datetime
from glob import glob
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import src.constants as constants

logging.basicConfig(level=logging.DEBUG)

class Migrate:
    def __init__(self, command, database_url=None, migration_name=None, driver=None):
        # Command variables
        self.command = command
        self.migration_name = migration_name
        self.driver = driver

        self.base_folder = 'migrations'
        
        # Initialize database connection for all commands except 'create' without database access
        if self.command != 'create':
            database = getattr(constants, f"{self.driver}_protocol")
            if self.driver == 'sqlserver':
                self.sql_engine = create_engine(f"{database}{database_url}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes")
            else:
                self.sql_engine = create_engine(f"{database}{database_url}")
        
        # Only initialize files list if not setup or create command
        if self.command not in ['setup', 'create']:
            self.files = [file.split("/")[-1] for file in glob(f"./{self.base_folder}/*")]
            self.files.sort()

        if self.command not in ['create', 'setup']:
            self.init_migration_table()

        if self.command in ['execute', 'exec']:
            self.execute_migration()
        
        if self.command == 'rollback':
            if migration_name is None:
                logging.error('you should provide the migration name to rollback database changes')
                sys.exit(0)
            self.rollback_migration()

        if self.command == 'create':
            if migration_name is None:
                logging.error('you should provide the migration name to create file')
                sys.exit(0)
            self.create_migration()
        
        if self.command == 'setup':
            self.setup()
            

    def init_migration_table(self):
        logging.info("EXECUTING MIGRATION INITIALIZER")
        sql_statement = getattr(constants, self.driver)
        with self.sql_engine.begin() as conn:
            conn.execute(text(sql_statement))
            
        logging.info("MIGRATION INITIALIZED SUCCESSFULLY")

    def execute_migration(self):
        logging.info("INITIALIZING MIGRATIONS EXECUTION\n")
        with self.sql_engine.connect() as conn:
            migrated = conn.execute(text("""
                SELECT name FROM migrations
            """))

            migrated = migrated.fetchall()

        migrated = [item[0] for item in migrated]
        to_migrate = [item for item in self.files if item not in migrated]

        if len(to_migrate) == 0:
            logging.info("NO MIGRATIONS TO BE EXECUTED")
            sys.exit(0)

        with self.sql_engine.begin() as conn:
            for file in to_migrate:
                with open(f"{self.base_folder}/{file}", "r") as f:
                    archive = f.read()
                    up = archive
                    if "=====DOWN" in archive:
                        split = archive.split("=====DOWN")
                        up = split[0]

                    logging.info(f"APPLYING -> {f.name}")
                    conn.execute(text(up))
                    conn.execute(text("""
                        INSERT INTO migrations (name)
                        VALUES (:name)
                    """),
                        {"name": file}
                    )

            logging.info("\nALL MIGRATIONS APPLIED SUCCESSFULLY")

    def rollback_migration(self):
        logging.info(f"PREPARING TO ROLLBACK MIGRATION {self.migration_name}")
        migration_file = f"{self.base_folder}/{self.migration_name}.sql"
        if not os.path.exists(migration_file):
            logging.error(f"Migration file {migration_file} does not exist")
            sys.exit(1)
        
        with open(migration_file, "r") as f:
            archive = f.read()
            down = archive
            if "=====DOWN" in archive:
                split = archive.split("=====DOWN")
                down = split[1]

        with self.sql_engine.begin() as conn:
            logging.info(f"ROLLING BACK -> {self.migration_name}.sql")
            conn.execute(text(down))
            conn.execute(
                text("""
                    DELETE FROM migrations
                    WHERE name = :name
                """),
                {"name": f"{self.migration_name}.sql"}
            )
        logging.info("ROLLBACK EXECUTED SUCCESSFULLY")
        sys.exit(0)

    def create_migration(self):
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

        file_name = f'{self.base_folder}/{datetime.now().strftime("%Y%m%d%H%M%S")}_{self.migration_name}.sql'
        with open(file_name, "w") as f:
            f.write("""-- Paste your migrations here to apply inside database\n\n=====DOWN\n\n-- Paste your rollback queries to rollback database modifications""")
        logging.info(f"Migration file created: {file_name}")

    def create_folders(self):
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)

    def setup(self):
        self.create_folders()
        self.init_migration_table()
        logging.info("SETUP COMPLETED SUCCESSFULLY - migrations folder created")
        
def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Migrate and rollback database scripts')
    parser.add_argument('command', help="command to execute inside dbms")
    parser.add_argument('--driver', help="SQL Driver to use: sqlite, pgsql, mysql, sqlserver", default="pgsql")
    parser.add_argument('--dbstring', help="Add dbstring without protocol to connection if you didn't set DATABASE_MIGRATION_URL environment var")
    parser.add_argument('--migration_name', help="Inform migration name to create or rollback sql migration file")
    args = parser.parse_args()

    if args.command == 'setup':
        if not args.dbstring and 'DATABASE_MIGRATION_URL' not in os.environ:
            logging.error('dbstring is missing for setup, you have to provide it as DATABASE_MIGRATION_URL environment variable, or via --dbstring argument')
            return
        Migrate(
            command=args.command,
            database_url=f"{os.getenv('DATABASE_MIGRATION_URL') if 'DATABASE_MIGRATION_URL' in os.environ else args.dbstring}",
            driver=args.driver
        )
        return

    if args.command == 'create':
        Migrate(command=args.command, migration_name=args.migration_name, driver=args.driver)
        return

    if not args.dbstring and 'DATABASE_MIGRATION_URL' not in os.environ:
        logging.error('dbstring is missing, you have to provide it as DATABASE_MIGRATION_URL environment variable, or via --dbstring positional argument of command')
        return

    Migrate(
        command=args.command,
        database_url=f"{os.getenv('DATABASE_MIGRATION_URL') if 'DATABASE_MIGRATION_URL' in os.environ else args.dbstring}",
        migration_name=args.migration_name,
        driver=args.driver
    )
