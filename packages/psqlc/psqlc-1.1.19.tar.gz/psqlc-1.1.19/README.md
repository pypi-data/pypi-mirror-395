# PostgreSQL Manager CLI Tool

Feature-rich command-line interface tool for managing PostgreSQL databases. Built with `asyncpg` and featuring beautiful output formatting with Rich, it provides intelligent auto-detection of database configurations from Django settings, environment files, and various configuration formats.


## ✨ Features

- 🚀 **Async Operations**: Built on asyncpg for high-performance database operations
- 🎯 **Intuitive Sub-commands** - Natural command structure (e.g., `show dbs`, `show tables`)
- 🔍 **Auto-detection** - Automatically finds and parses Django `settings.py` files
- 🎨 **Beautiful Output** - Rich formatted tables with color-coded messages
- 🔐 **Security First** - Confirmation prompts for destructive operations, read-only mode for queries
- 📊 **Comprehensive Info** - Database sizes, table structures, indexes, connections, and more
- 🛡️ **Production Ready** - Robust error handling, connection timeouts, transaction management, Error handling, logging, and safety features

## 📋 Requirements

```bash
pip install psqlc
# or
pip install git+https://github.com/cumulus13/psqlc
```

## 🚀 Quick Start

### Basic Usage

```bash
# Show version
psqlc --version

# List all databases
psqlc show dbs

# List tables in current project's database (auto-detected)
psqlc show tables

# Show database users
psqlc show users

# Show all databases
psqlc show dbs -U postgres -P password

# Show tables in a database
psqlc show tables -d mydb -U postgres

# Create user and database
psqlc create newuser newpass newdb -U postgres

# Execute a query
psqlc query -d mydb -q "SELECT * FROM users LIMIT 10" -U postgres
```

## 🔧 Configuration Auto-Detection

### 1. Django settings.py

#### Using Django Settings Auto-detection

If you have a Django `settings.py` file in your project to extract PostgreSQL configuration. It searches:

1. Current working directory
2. Recursively down to 5 levels deep
3. Explicit paths provided as arguments

the tool will automatically detect and use the database configurations from:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

```bash
# No need to specify database credentials!
psqlc show tables
psqlc show dbs
psqlc describe -t users
```

### 2. Environment Files (.env)
```bash
# .env
POSTGRESQL_USERNAME=myuser
POSTGRESQL_PASSWORD=mypassword
POSTGRESQL_DB_NAME=mydatabase
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
```

### 3. JSON/YAML Configuration
```json
{
    "engine": "postgresql",
    "user": "myuser",
    "password": "mypassword",
    "database": "mydatabase",
    "host": "localhost",
    "port": 5432
}
```


The tool searches recursively (up to 5 levels deep) for `settings.py|.env|.json|.yaml|.ini` files and extracts PostgreSQL configuration automatically.


### Auto-detection Priority

1. **Command-line arguments** (highest priority)
2. **Django settings.py -> .env -> .json -> .yaml -> .ini** (if no CLI args provided)
3. **Interactive prompt** (for passwords only)

### Manual Settings Path

```bash
# Specify settings.py file
psqlc create /path/to/settings.py
psqlc create /path/to/*.env
psqlc create /path/to/anyfile.env
psqlc create /path/to/*.json
psqlc create /path/to/anyfile.json
psqlc create /path/to/*.yaml
psqlc create /path/to/anyfile.yaml
psqlc create /path/to/*.ini
psqlc create /path/to/anyfile.ini

# Specify directory containing settings.py
psqlc create /path/to/project/
```


## 📚 Commands Reference

### Global Options

These options can be used with any command:

| Option | Description | Default |
|--------|-------------|---------|
| `-H, --hostname` | PostgreSQL server address | `222.222.222.5` |
| `-U, --user` | PostgreSQL superuser | `postgres` |
| `-P, --passwd` | PostgreSQL superuser password | Auto-detect or prompt |
| `--port` | PostgreSQL server port | `5432` |
| `--debug` | Enable debug mode | `False` |

### SHOW Commands

Display various database information with beautiful formatted tables.

#### List Databases `show dbs`
```bash
psqlc show dbs
```
Shows all databases with sizes, encoding, and collation.

**Example Output:**
```
┌───────────────────┬─────────┬───────────┬────────────┐
│ Database          │ Size    │ Encoding  │ Collation  │
├───────────────────┼─────────┼───────────┼────────────┤
│ myapp_production  │ 15 MB   │ UTF8      │ en_US.utf8 │
│ myapp_development │ 8 MB    │ UTF8      │ en_US.utf8 │
│ postgres          │ 8 MB    │ UTF8      │ en_US.utf8 │
└───────────────────┴─────────┴───────────┴────────────┘
```

#### List Tables `show tables`

List all tables in a database with size and column count.

```bash
psqlc show tables -d mydatabase
# Or auto-detect database from settings
psqlc show tables
```

**Example Output:**
```
┌────────┬──────────────────┬────────┬─────────┐
│ Schema │ Table            │ Size   │ Columns │
├────────┼──────────────────┼────────┼─────────┤
│ public │ auth_user        │ 256 KB │ 11      │
│ public │ django_session   │ 128 KB │ 4       │
│ public │ products_product │ 512 KB │ 8       │
└────────┴──────────────────┴────────┴─────────┘
```

**Options:**
- `-d, --database` - Database name (auto-detects from settings.py if not provided)

#### List Users `show users`

List all PostgreSQL users/roles with their permissions.

```bash
psqlc show users
```

**Output:**
```
┌──────────────┬───────────┬───────────┬─────────────┬───────────┬──────────────┐
│ Username     │ Superuser │ Create DB │ Create Role │ Can Login │ Replication  │
├──────────────┼───────────┼───────────┼─────────────┼───────────┼──────────────┤
│ postgres     │ True      │ True      │ True        │ True      │ True         │
│ myapp_user   │ False     │ True      │ False       │ True      │ True         │
└──────────────┴───────────┴───────────┴─────────────┴───────────┴──────────────┘
```

#### Show Connections `show connections`

Display active database connections with client information.

```bash
psqlc show connections
```

#### Show Indexes `show indexes`

Display indexes in database or specific table.

```bash
# Show all indexes in database
psqlc show indexes

# Show indexes for specific table
psqlc show indexes -d mydb -t users
```

**Options:**
- `-d, --database` - Database name (auto-detect if not provided)
- `-t, --table` - Table name (optional, shows all if not provided)

#### Show Sizes `show size`

Display size information for databases or tables.

```bash
# Show all database sizes
psqlc show size

# Show table sizes in a database
psqlc show size -d mydb

# Show size of specific table
psqlc show size -d mydb -t users
```

**Options:**
- `-d, --database` - Database name (auto-detect if not provided)
- `-t, --table` - Table name (optional, shows all tables if not provided)

**Example Output:**
```
📊 Size of table 'users':
   Total Size:   15 MB
   Table Size:   12 MB
   Indexes Size: 3 MB
```

### CREATE Command

Create a new PostgreSQL user and database with proper privileges.

```bash
# Method 1: Direct arguments
psqlc create username password dbname -U postgres

# Method 2: Named arguments
psqlc create -u username -p password -d dbname -U postgres

# Method 3: Auto-detect from settings.py
psqlc create -U postgres

# Method 4: From Django settings file
psqlc create /path/to/settings.py -U postgres
```

**Options:**
- `CONFIG` - Positional arguments: `NEW_USERNAME NEW_PASSWORD NEW_DB`
- `-u, --username` - New PostgreSQL username
- `-p, --password` - Password for new user
- `-d, --database` - Database name to create

**Features:**
- Automatically creates user with LOGIN, CREATEDB, REPLICATION, BYPASSRLS privileges
- Checks for existing database and prompts for confirmation before dropping
- Supports Django settings.py auto-detection

### DESCRIBE Command

Show detailed table structure including columns, data types, and constraints.

```bash
# Auto-detect database
psqlc describe -t users

# Specify database
psqlc describe -d mydb -t users
```

**Options:**
- `-d, --database` - Database name (auto-detect if not provided)
- `-t, --table` - Table name (required)

**Output:**
```
┌──────────────┬──────────────┬────────────┬──────────┬─────────────┐
│ Column       │ Type         │ Max Length │ Nullable │ Default     │
├──────────────┼──────────────┼────────────┼──────────┼─────────────┤
│ id           │ integer      │ -          │ NO       │ nextval()   │
│ username     │ varchar      │ 150        │ NO       │ -           │
│ email        │ varchar      │ 255        │ YES      │ -           │
│ created_at   │ timestamp    │ -          │ NO       │ now()       │
└──────────────┴──────────────┴────────────┴──────────┴─────────────┘
```

### QUERY Command

Execute custom SQL queries with safety features.

```bash
# Basic query
psqlc query -d mydb -q "SELECT * FROM users LIMIT 10"

# Read-only mode (prevents destructive operations)
psqlc query -d mydb -q "SELECT * FROM users" --readonly

# Limit rows displayed
psqlc query -d mydb -q "SELECT * FROM logs" --limit 50
```

**Options:**
- `-d, --database` - Database name (auto-detect if not provided)
- `-q, --query` - SQL query to execute (required)
- `--readonly` - Prevent destructive operations (blocks DROP, DELETE, TRUNCATE, ALTER, CREATE, INSERT, UPDATE)
- `--limit` - Limit number of rows displayed (default: 100)

**Safety Features:**
- Read-only mode blocks all destructive SQL commands
- Automatic transaction rollback on errors
- Row limit prevents memory issues with large result sets

### BACKUP Command

Generate backup command for a database using pg_dump.

```bash
# Auto-detect database
psqlc backup

# Specify database
psqlc backup -d mydb
```

```bash
psqlc backup -d mydatabase
```

**Output:**
```
🗄️ Creating backup of 'mydatabase'...
💡 Run this command manually:
   pg_dump -h 127.0.0.1 -p 5432 -U postgres -d mydatabase -F p -f mydatabase_backup_20231014_143022.sql
```

**Options:**
- `-d, --database` - Database name to backup (auto-detect if not provided)

**Note:** This command generates the pg_dump command for you to run manually. Direct backup execution requires pg_dump to be installed and accessible in your PATH.

### DROP Commands

Safely drop databases or users with confirmation prompts.

#### Drop Database `drop database`

Drop a database with safety confirmation.

```bash
# Auto-detect database
psqlc drop database

# Specify database
psqlc drop database -d mydb
```

**Options:**
- `-d, --database` - Database name to drop (auto-detect if not provided)

**Safety Features:**
- Requires typing the exact database name for confirmation
- Automatically terminates all active connections before dropping
- Cannot be undone - use with caution!

#### Drop User `drop user`

Drop a PostgreSQL user/role with safety confirmation.

```bash
psqlc drop user -u username
```

**Options:**
- `-u, --username` - Username to drop (required)

**Safety Features:**
- Requires typing the exact username for confirmation
- Cannot be undone - use with caution!

## Advanced Usage

### Using with Custom Configuration Files

```bash
# Use specific settings file
psqlc --debug show tables

# Custom host and port
psqlc -H db.example.com --port 5433 show dbs

# Different superuser
psqlc -U admin show users
```

### Debug Mode

Enable debug mode for detailed logging:

```bash
psqlc --debug show dbs
```

Or set environment variable:
```bash
export DEBUG=1
psqlc show tables
```

## API Reference

### Core Functions

#### `parse_django_settings(settings_path: str = None) -> Optional[Dict[str, Any]]`
Parse Django settings.py or config files for database configuration.

**Parameters:**
- `settings_path`: Optional path to settings file

**Returns:** Database configuration dictionary or None

#### `get_connection(host: str, port: int, user: str, password: str, database: str = "postgres", auto_settings: bool = True, settings_path = None)`
Create async database connection.

#### `show_databases(args)`
List all databases with detailed information.

#### `create_user_db(args)`
Create PostgreSQL user and database with proper privileges.

## Error Handling

psqlc includes comprehensive error handling:

- Connection failures are clearly reported
- Invalid queries show descriptive errors
- Destructive operations require confirmation
- Debug mode provides detailed error information

## 💡 Examples

### Example 1: Complete Database Setup

```bash
# Create user and database from Django settings
psqlc create -U postgres

# Verify creation
psqlc show dbs
psqlc show users

# Check table structure
psqlc show tables
psqlc describe -t auth_user
```

### Example 2: Database Inspection

```bash
# Check database sizes
psqlc show size

# Check specific database details
psqlc show size -d mydb
psqlc show tables -d mydb
psqlc show indexes -d mydb

# Monitor connections
psqlc show connections
```

### Example 3: Safe Query Execution

```bash
# Read-only query (safe)
psqlc query -q "SELECT COUNT(*) FROM users" --readonly

# Regular query with limit
psqlc query -q "SELECT * FROM logs ORDER BY created_at DESC" --limit 20

# Complex query
psqlc query -q "
SELECT u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.username
ORDER BY order_count DESC
" --readonly
```

### Example 4: Database Maintenance

```bash
# Backup database
psqlc backup -d production_db

# Check sizes before cleanup
psqlc show size -d production_db

# Drop old test database
psqlc drop database -d old_test_db

# Drop old user
psqlc drop user -u old_test_user
```

### Example 5: Complete Workflow Example

```bash
# 1. Check existing databases
psqlc show dbs

# 2. Create new user and database
psqlc create -u myapp -p mypass123 -d myapp_db

# 3. List tables in new database
psqlc show tables -d myapp_db

# 4. Execute setup queries
psqlc query -d myapp_db -q "CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(100))"

# 5. Check table structure
psqlc describe -d myapp_db -t users

# 6. Monitor database size
psqlc show size -d myapp_db

# 7. Generate backup command
psqlc backup -d myapp_db
```

### Example 6: Integration with Django Projects

When working in a Django project directory, psqlc automatically detects your `settings.py`:

```bash
cd /path/to/your/django/project
psqlc show tables  # Auto-detects database from settings.py
psqlc describe -t auth_user  # No need to specify database
```

### Example 7: Production Monitoring

```bash
# Monitor active connections
psqlc show connections

# Check database sizes regularly
psqlc show size

# Monitor user activity
psqlc show users
```


## 🔐 Security Best Practices

1. **Never hardcode passwords** - Use environment variables or settings files
2. **Use read-only mode** for SELECT queries in production
3. **Always confirm** before dropping databases or users
4. **Limit query results** to prevent memory issues
5. **Use connection timeouts** (built-in: 10 seconds)
6. **Regular backups** before major operations

## 🐛 Troubleshooting

### Enable Debug Mode

```bash
psqlc --debug show dbs
```

### Enable full traceback:

```bash
export TRACEBACK=1
psqlc show dbs
```

Debug mode shows:
- Settings.py detection attempts
- Connection details
- Detailed error messages
- full traceback

### Common Issues

### "Connection Refused**

```bash
# Check if PostgreSQL is running
psqlc -H localhost --port 5432 show dbs
```

#### "Connection failed"
- Check hostname, port, username, and password
- Verify PostgreSQL server is running
- Check firewall settings

```bash
   # Provide password explicitly
psqlc -U postgres -P yourpassword show dbs
```

#### "Settings.py not found"
- Ensure settings.py exists in current directory or subdirectories
- Try specifying the path explicitly
- Use `--debug` to see search paths

```bash
# Specify settings file directly
psqlc --debug show tables
```

#### "Permission denied"
- Verify user has sufficient privileges
- Some operations require superuser access
- Check PostgreSQL user permissions

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug output | `0` |
| `TRACEBACK` | Show full tracebacks on errors | `0` |
| `HOST` | Database host | empty/None |
| `PORT` | Database port | `5432` |
| `USER` | Database user | `postgres` |
| `PASSWORD` | Database password | empty/None |
| `DATABASE`/`DB_NAME`/`DB` | Database name | empty/None |

Set environment variables:

```bash
# Linux/Mac
export DEBUG=1
psqlc show dbs

# Windows
set DEBUG=1
psqlc show dbs
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)
 
[Support me on Patreon](https://www.patreon.com/cumulus13)

## 🙏 Acknowledgments

- Built with [psycopg2](https://www.psycopg.org/) for PostgreSQL connectivity
- Styled with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Argument parsing with [licface](https://github.com/cumulus13/licface) for custom help formatting

## 📞 Support

For issues, questions, or contributions, please visit the project repository or contact the author.

---

**Note:** This tool is designed for PostgreSQL database management. Always test commands in a development environment before using in production.