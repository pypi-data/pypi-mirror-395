sqlite_protocol="sqlite:////"
pgsql_protocol="postgresql+psycopg2://"
mysql_protocol="mysql+pymysql://"
sqlserver_protocol="mssql+pyodbc://"

sqlite = """
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

pgsql = """
    CREATE TABLE IF NOT EXISTS migrations (
        id serial NOT NULL,
        "name" varchar NOT NULL,
        applied_at timestamptz(0) NOT NULL DEFAULT now(),
        CONSTRAINT migrations_pk PRIMARY KEY (id)
    );
"""

mysql = """
    CREATE TABLE IF NOT EXISTS migrations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

sqlserver = """
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[migrations]') AND type = 'U')
    BEGIN
        CREATE TABLE migrations (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(255) NOT NULL,
            applied_at DATETIME DEFAULT GETDATE()
        );
    END;
"""
