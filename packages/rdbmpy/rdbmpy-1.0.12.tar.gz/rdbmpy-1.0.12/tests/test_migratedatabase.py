import os
import unittest
import shutil
import tempfile
import src.migrate as migrate

class Test(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test isolation
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test database
        os.makedirs('sqlitedata/db', exist_ok=True)
        with open('sqlitedata/db/test.db', 'w') as file:
            file.close()
        self.db = f"{os.getcwd()}/sqlitedata/db/test.db"
        
    def tearDown(self):
        # Clean up: go back to original directory and remove temp dir
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_migrate_test1_init(self):
        # Test that executing migrations without migration files exits with code 0
        # (no migrations to apply)
        with self.assertRaises(SystemExit) as cm:
            migrate.Migrate("execute", self.db, driver='sqlite')
        # Verify it exits with code 0 (success, no migrations to apply)
        self.assertEqual(cm.exception.code, 0)

    def test_migrate_test2_create(self):
        migrate.Migrate("create", self.db, driver='sqlite', migration_name="test")

    def test_migrate_test3_migrate(self):
        # Create migrations folder if it doesn't exist
        os.makedirs('migrations', exist_ok=True)
        
        with open('migrations/001_migrate.sql', 'w') as file:
            file.write("""
                CREATE TABLE test (
                    id INTEGER PRIMARY KEY,
                    name varchar(100),
                    age INTEGER
                )
            """)

        migrate.Migrate("execute", self.db, driver='sqlite')

