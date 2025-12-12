# 🚀 WowSQL Python SDK

Official Python client for [WowSQL](https://wowsql.com) - MySQL Backend-as-a-Service with S3 Storage.

## Installation

```bash
pip install wowsql
```

## Quick Start

### Database Operations

```python
from wowsql import WowSQLClient

# Initialize client
client = WowSQLClient(
    project_url="https://your-project.wowsql.com",
    api_key="your-api-key"  # Get from dashboard
)

# Select data
response = client.table("users").select("*").limit(10).execute()
print(response.data)  # [{'id': 1, 'name': 'John', ...}, ...]

# Insert data
result = client.table("users").insert({
    "name": "Jane Doe",
    "email": "jane@example.com",
    "age": 25
}).execute()

# Update data
result = client.table("users").update({
    "name": "Jane Smith"
}).eq("id", 1).execute()

# Delete data
result = client.table("users").delete().eq("id", 1).execute()
```

### Storage Operations (NEW in 0.2.0!)

```python
from wowsql import WowSQLStorage

# Initialize storage client
storage = WowSQLStorage(
    project_url="https://your-project.wowsql.com",
    api_key="your-api-key"
)

# Upload file
storage.upload("local-file.pdf", "uploads/document.pdf")

# Download file (get presigned URL)
url = storage.download("uploads/document.pdf")
print(url)

# List files
files = storage.list_files(prefix="uploads/")
for file in files:
    print(f"{file.key}: {file.size} bytes")

# Delete file
storage.delete_file("uploads/document.pdf")

# Check storage quota
quota = storage.get_quota()
print(f"Used: {quota.used_bytes}/{quota.limit_bytes} bytes")
print(f"Available: {quota.available_bytes} bytes")
```

### Project Authentication (NEW)

```python
from wowsql import ProjectAuthClient

auth = ProjectAuthClient(
    project_url="https://your-project.wowsql.com",
    api_key="your-anon-key"  # Use anon key for client-side, service key for server-side
)
```

#### Sign Up Users

```python
result = auth.sign_up(
    email="user@example.com",
    password="SuperSecret123",
    full_name="End User",
    user_metadata={"referrer": "landing"}
)

print(result.user.email, result.session.access_token)
```

#### Sign In & Persist Sessions

```python
session = auth.sign_in(
    email="user@example.com",
    password="SuperSecret123"
).session

auth.set_session(
    access_token=session.access_token,
    refresh_token=session.refresh_token
)

current_user = auth.get_user()
print(current_user.id, current_user.email_verified)
```

#### OAuth Authentication

```python
# Step 1: Get authorization URL
oauth = auth.get_oauth_authorization_url(
    provider="github",
    redirect_uri="https://app.example.com/auth/callback"
)
print("Send the user to:", oauth["authorization_url"])

# Step 2: After user authorizes, exchange code for tokens
# (In your callback handler)
result = auth.exchange_oauth_callback(
    provider="github",
    code="authorization_code_from_callback",
    redirect_uri="https://app.example.com/auth/callback"
)
print(f"Logged in as: {result.user.email}")
print(f"Access token: {result.session.access_token}")
```

#### Password Reset

```python
# Request password reset
result = auth.forgot_password(email="user@example.com")
print(result["message"])  # "If that email exists, a password reset link has been sent"

# Reset password (after user clicks email link)
result = auth.reset_password(
- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Advanced filtering (eq, neq, gt, gte, lt, lte, like, is_null)
- ✅ Pagination (limit, offset)
- ✅ Sorting (order_by)
- ✅ Raw SQL queries
- ✅ Table schema introspection
- ✅ Automatic rate limit handling
- ✅ Built-in error handling
- ✅ Context manager support

### Storage Features (NEW!)
- ✅ S3-compatible storage client
- ✅ File upload with automatic quota validation
- ✅ File download (presigned URLs)
- ✅ File listing with metadata
- ✅ File deletion (single and batch)
- ✅ Storage quota management
- ✅ Multi-region support
- ✅ Client-side limit enforcement

## Usage Examples

### Select Queries

```python
from wowsql import WowSQLClient

client = WowSQLClient(
    project_url="https://your-project.wowsql.com",
    api_key="your-api-key"
)

# Select all columns
users = client.table("users").select("*").execute()

# Select specific columns
users = client.table("users").select("id", "name", "email").execute()

# With filters
active_users = client.table("users") \
    .select("*") \
    .eq("status", "active") \
    .gt("age", 18) \
    .execute()

# With ordering
recent_users = client.table("users") \
    .select("*") \
    .order_by("created_at", desc=True) \
    .limit(10) \
    .execute()

# With pagination
page_1 = client.table("users").select("*").limit(20).offset(0).execute()
page_2 = client.table("users").select("*").limit(20).offset(20).execute()

# Pattern matching
gmail_users = client.table("users") \
    .select("*") \
    .like("email", "%@gmail.com") \
    .execute()
```

### Insert Data

```python
# Insert single row
result = client.table("users").insert({
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
}).execute()

# Insert multiple rows
result = client.table("users").insert([
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]).execute()
```

### Update Data

```python
# Update by ID
result = client.table("users").update({
    "name": "Jane Smith",
    "age": 26
}).eq("id", 1).execute()

# Update with conditions
result = client.table("users").update({
    "status": "inactive"
}).lt("last_login", "2024-01-01").execute()
```

### Delete Data

```python
# Delete by ID
result = client.table("users").delete().eq("id", 1).execute()

# Delete with conditions
result = client.table("users").delete() \
    .eq("status", "deleted") \
    .lt("created_at", "2023-01-01") \
    .execute()
```

### Filter Operators

```python
# Equal
.eq("status", "active")

# Not equal
.neq("status", "deleted")

# Greater than
.gt("age", 18)

# Greater than or equal
.gte("age", 18)

# Less than
.lt("age", 65)

# Less than or equal
.lte("age", 65)

# Pattern matching (SQL LIKE)
.like("email", "%@gmail.com")

# Is null
.is_null("deleted_at")
```

### Storage Operations

```python
from wowsql import WowSQLStorage, StorageLimitExceededError

storage = WowSQLStorage(
    project_url="https://your-project.wowsql.com",
    api_key="your-api-key"
)

# Upload file with metadata
storage.upload(
    "document.pdf",
    "uploads/2024/document.pdf",
    metadata={"category": "reports"}
)

# Upload file object
with open("image.jpg", "rb") as f:
    storage.upload_fileobj(f, "images/photo.jpg")

# Check if file exists
if storage.file_exists("uploads/document.pdf"):
    print("File exists!")

# Get file information
info = storage.get_file_info("uploads/document.pdf")
print(f"Size: {info.size} bytes")
print(f"Modified: {info.last_modified}")

# List files with prefix
files = storage.list_files(prefix="uploads/2024/", limit=100)
for file in files:
    print(f"{file.key}: {file.size} bytes")

# Download file to local path
storage.download("uploads/document.pdf", "local-copy.pdf")

# Get presigned URL (valid for 1 hour)
url = storage.download("uploads/document.pdf")
print(url)  # https://s3.amazonaws.com/...

# Delete single file
storage.delete_file("uploads/old-file.pdf")

# Delete multiple files
storage.delete_files([
    "uploads/file1.pdf",
    "uploads/file2.pdf",
    "uploads/file3.pdf"
])

# Check quota before upload
quota = storage.get_quota()
file_size = storage.get_file_size("large-file.zip")

if quota.available_bytes < file_size:
    print(f"Not enough storage! Need {file_size} bytes, have {quota.available_bytes}")
else:
    storage.upload("large-file.zip", "backups/large-file.zip")

# Handle storage limit errors
try:
    storage.upload("huge-file.zip", "uploads/huge-file.zip")
except StorageLimitExceededError as e:
    print(f"Storage limit exceeded: {e}")
    print("Please upgrade your plan or delete old files")
```

### Context Manager

```python
# Automatically closes connection
with WowSQLClient(project_url="...", api_key="...") as client:
    users = client.table("users").select("*").execute()
    print(users.data)
# Connection closed here

# Works with storage too
with WowSQLStorage(project_url="...", api_key="...") as storage:
    files = storage.list_files()
    print(f"Total files: {len(files)}")
```

### Error Handling

```python
from wowsql import (
    WowSQLClient,
    WowSQLError,
    StorageError,
    StorageLimitExceededError
)

client = WowSQLClient(project_url="...", api_key="...")

try:
    users = client.table("users").select("*").execute()
except WowSQLError as e:
    print(f"Database error: {e}")

storage = WowSQLStorage(project_url="...", api_key="...")

try:
    storage.upload("file.pdf", "uploads/file.pdf")
except StorageLimitExceededError as e:
    print(f"Storage full: {e}")
except StorageError as e:
    print(f"Storage error: {e}")
```

### Utility Methods

```python
# Check API health
health = client.health()
print(health)  # {'status': 'healthy', ...}

# List all tables
tables = client.list_tables()
print(tables)  # ['users', 'posts', 'comments']

# Get table schema
schema = client.describe_table("users")
print(schema)  # {'columns': [...], 'row_count': 100}
```

## Response Object

All database queries return a response object:

```python
response = client.table("users").select("*").limit(10).execute()

# Access data
print(response.data)   # [{'id': 1, ...}, {'id': 2, ...}]

# Access count
print(response.count)  # 10

# Check for errors
if response.error:
    print(response.error)
```

## Configuration

### Timeouts

```python
# Custom timeout (default: 30 seconds)
client = WowSQLClient(
    project_url="...",
    api_key="...",
    timeout=60  # 60 seconds
)

# Storage timeout (default: 60 seconds for large files)
storage = WowSQLStorage(
    project_url="...",
    api_key="...",
    timeout=120  # 2 minutes
)
```

### Auto Quota Check

```python
# Disable automatic quota checking before uploads
storage = WowSQLStorage(
    project_url="...",
    api_key="...",
    auto_check_quota=False
)

# Manually check quota
quota = storage.get_quota()
if quota.available_bytes > file_size:
    storage.upload("file.pdf", "uploads/file.pdf", check_quota=False)
```

## API Keys

WOWSQL uses **different API keys for different operations**. Understanding which key to use is crucial for proper authentication.

### Key Types Overview

## 🔑 Unified Authentication

**✨ One Project = One Set of Keys for ALL Operations**

WowSQL uses **unified authentication** - the same API keys work for both database operations AND authentication operations.

| Operation Type | Recommended Key | Alternative Key | Used By |
|---------------|----------------|-----------------|---------|
| **Database Operations** (CRUD) | Service Role Key (`wowsql_service_...`) | Anonymous Key (`wowsql_anon_...`) | `WowSQLClient` |
| **Authentication Operations** (OAuth, sign-in) | Anonymous Key (`wowsql_anon_...`) | Service Role Key (`wowsql_service_...`) | `ProjectAuthClient` |

### Where to Find Your Keys

All keys are found in: **WOWSQL Dashboard → Settings → API Keys** or **Authentication → PROJECT KEYS**

1. **Anonymous Key** (`wowsql_anon_...`) ✨ **Unified Key**
   - Location: "Anonymous Key (Public)"
   - Used for: 
     - ✅ Client-side auth operations (signup, login, OAuth)
     - ✅ Public/client-side database operations with limited permissions
   - **Safe to expose** in frontend code (browser, mobile apps)

2. **Service Role Key** (`wowsql_service_...`) ✨ **Unified Key**
   - Location: "Service Role Key (keep secret)"
   - Used for:
     - ✅ Server-side auth operations (admin, full access)
     - ✅ Server-side database operations (full access, bypass RLS)
   - **NEVER expose** in frontend code - server-side only!

### Database Operations

Use **Service Role Key** or **Anonymous Key** for database operations:

```python
from wowsql import WowSQLClient

# Using Service Role Key (recommended for server-side, full access)
client = WowSQLClient(
    project_url="https://your-project.wowsql.com",
    api_key="wowsql_service_your-service-key-here"  # Service Role Key
)

# Using Anonymous Key (for public/client-side access with limited permissions)
client = WowSQLClient(
    project_url="https://your-project.wowsql.com",
    api_key="wowsql_anon_your-anon-key-here"  # Anonymous Key
)

# Query data
users = client.table("users").get()
```

### Authentication Operations

**✨ UNIFIED AUTHENTICATION:** Use the **same keys** as database operations!

```python
from wowsql import ProjectAuthClient

# Using Anonymous Key (recommended for client-side auth operations)
auth = ProjectAuthClient(
    project_url="https://your-project.wowsql.com",
    api_key="wowsql_anon_your-anon-key-here"  # Same key as database operations!
)

# Using Service Role Key (for server-side auth operations)
auth = ProjectAuthClient(
    project_url="https://your-project.wowsql.com",
    api_key="wowsql_service_your-service-key-here"  # Same key as database operations!
)

# OAuth authentication
oauth_url = auth.get_oauth_authorization_url(
    provider="github",
    redirect_uri="https://app.example.com/auth/callback"
)
```

**Note:** The `public_api_key` parameter is deprecated but still works for backward compatibility. Use `api_key` instead.

### Environment Variables

Best practice: Use environment variables for API keys:

```python
import os
from wowsql import WowSQLClient, ProjectAuthClient

# UNIFIED AUTHENTICATION: Same keys for both operations!

# Database operations - Service Role Key
db_client = WowSQLClient(
    project_url=os.getenv("WOWSQL_PROJECT_URL"),
    api_key=os.getenv("WOWSQL_SERVICE_ROLE_KEY")  # or WOWSQL_ANON_KEY
)

# Authentication operations - Use the SAME key!
auth_client = ProjectAuthClient(
    project_url=os.getenv("WOWSQL_PROJECT_URL"),
    api_key=os.getenv("WOWSQL_ANON_KEY")  # Same key for client-side auth
    # Or use WOWSQL_SERVICE_ROLE_KEY for server-side auth
)
```

### Key Usage Summary

**✨ UNIFIED AUTHENTICATION:**
- **`WowSQLClient`** → Uses **Service Role Key** or **Anonymous Key** for database operations
- **`ProjectAuthClient`** → Uses **Anonymous Key** (client-side) or **Service Role Key** (server-side) for authentication operations
- **Same keys work for both** database AND authentication operations! 🎉
- **Anonymous Key** (`wowsql_anon_...`) → Client-side operations (auth + database)
- **Service Role Key** (`wowsql_service_...`) → Server-side operations (auth + database)
- **Anonymous Key** is optional and provides limited permissions for public database access

### Security Best Practices

1. **Never expose Service Role Key** in client-side code or public repositories
2. **Use Public API Key** for client-side authentication flows
3. **Use Anonymous Key** for public database access with limited permissions
4. **Store keys in environment variables**, never hardcode them
5. **Rotate keys regularly** if compromised

### Troubleshooting

**Error: "Invalid API key for project"**
- Ensure you're using the correct key type for the operation
- Database operations require Service Role Key or Anonymous Key
- Authentication operations require Anonymous Key (client-side) or Service Role Key (server-side)
- Verify the key is copied correctly (no extra spaces)

**Error: "Authentication failed"**
- Check that you're using the correct key: Anonymous Key for client-side, Service Role Key for server-side
- Verify the project URL matches your dashboard
- Ensure the key hasn't been revoked or expired

## Examples

### Blog Application

```python
from wowsql import WowSQLClient

client = WowSQLClient(project_url="...", api_key="...")

# Create a new post
post = client.table("posts").insert({
    "title": "Hello World",
    "content": "My first blog post",
    "author_id": 1,
    "published": True
}).execute()

# Get published posts
posts = client.table("posts") \
    .select("id", "title", "content", "created_at") \
    .eq("published", True) \
    .order_by("created_at", desc=True) \
    .limit(10) \
    .execute()

# Get post with comments
post = client.table("posts").select("*").eq("id", 1).execute()
comments = client.table("comments").select("*").eq("post_id", 1).execute()
```

### File Upload Application

```python
from wowsql import WowSQLClient, WowSQLStorage

client = WowSQLClient(project_url="...", api_key="...")
storage = WowSQLStorage(project_url="...", api_key="...")

# Upload user avatar
user_id = 123
avatar_path = f"avatars/{user_id}.jpg"
storage.upload("avatar.jpg", avatar_path)

# Save avatar URL in database
avatar_url = storage.download(avatar_path)
client.table("users").update({
    "avatar_url": avatar_url
}).eq("id", user_id).execute()

# List user's files
user_files = storage.list_files(prefix=f"users/{user_id}/")
print(f"User has {len(user_files)} files")
```

## Requirements

- Python 3.8+
- requests>=2.31.0

## Development

```bash
# Clone repository
git clone https://github.com/wowsql/wowsql.git
cd wowsql/sdk/python

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run examples
python examples/basic_usage.py
python examples/storage_usage.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License - see LICENSE file for details.

## Links

- 📚 [Documentation](https://wowsql.com/docs)
- 🌐 [Website](https://wowsql.com)
- 💬 [Discord](https://discord.gg/wowsql)
- 🐛 [Issues](https://github.com/wowsql/wowsql/issues)

## 🔧 Schema Management (NEW in v0.5.0!)

Programmatically manage your database schema with the `WowSQLSchema` client.

> **⚠️ IMPORTANT**: Schema operations require a **Service Role Key** (`service_*`). Anonymous keys will return a 403 Forbidden error.

### Quick Start

```python
from wowsql import WowSQLSchema

# Initialize schema client with SERVICE ROLE KEY
schema = WowSQLSchema(
    project_url="https://your-project.wowsql.com",
    service_key="service_xyz789..."  # ⚠️ Backend only! Never expose!
)
```

### Create Table

```python
# Create a new table
schema.create_table(
    table_name="products",
    columns=[
        {"name": "id", "type": "INT", "auto_increment": True},
        {"name": "name", "type": "VARCHAR(255)", "not_null": True},
        {"name": "price", "type": "DECIMAL(10,2)", "not_null": True},
        {"name": "category", "type": "VARCHAR(100)"},
        {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
    ],
    primary_key="id",
    indexes=[
        {"name": "idx_category", "columns": ["category"]},
        {"name": "idx_price", "columns": ["price"]}
    ]
)
print("Table 'products' created successfully!")
```

### Alter Table

```python
# Add a new column
schema.alter_table(
    table_name="products",
    add_columns=[
        {"name": "stock_quantity", "type": "INT", "default": "0"}
    ]
)

# Modify an existing column
schema.alter_table(
    table_name="products",
    modify_columns=[
        {"name": "price", "type": "DECIMAL(12,2)"}  # Increase precision
    ]
)

# Drop a column
schema.alter_table(
    table_name="products",
    drop_columns=["category"]
)

# Rename a column
schema.alter_table(
    table_name="products",
    rename_columns=[
        {"old_name": "name", "new_name": "product_name"}
    ]
)
```

### Drop Table

```python
# Drop a table
schema.drop_table("old_table")

# Drop with CASCADE (removes dependent objects)
schema.drop_table("products", cascade=True)
```

### Execute Raw SQL

```python
# Execute custom schema SQL
schema.execute_sql("""
    CREATE INDEX idx_product_name 
    ON products(product_name);
""")

# Add a foreign key constraint
schema.execute_sql("""
    ALTER TABLE orders 
    ADD CONSTRAINT fk_product 
    FOREIGN KEY (product_id) 
    REFERENCES products(id);
""")
```

### Security & Best Practices

#### ✅ DO:
- Use service role keys **only in backend/server code**
- Store service keys in environment variables
- Use anonymous keys for client-side data operations
- Test schema changes in development first

#### ❌ DON'T:
- Never expose service role keys in frontend code
- Never commit service keys to version control
- Don't use anonymous keys for schema operations (will fail)

### Example: Backend Migration Script

```python
import os
from wowsql import WowSQLSchema

def run_migration():
    schema = WowSQLSchema(
        project_url=os.getenv("WOWSQL_PROJECT_URL"),
        service_key=os.getenv("WOWSQL_SERVICE_KEY")  # From env var
    )
    
    # Create users table
    schema.create_table(
        table_name="users",
        columns=[
            {"name": "id", "type": "INT", "auto_increment": True},
            {"name": "email", "type": "VARCHAR(255)", "unique": True, "not_null": True},
            {"name": "name", "type": "VARCHAR(255)", "not_null": True},
            {"name": "created_at", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"}
        ],
        primary_key="id",
        indexes=[{"name": "idx_email", "columns": ["email"]}]
    )
    
    print("Migration completed!")

if __name__ == "__main__":
    run_migration()
```

### Error Handling

```python
from wowsql import WowSQLSchema, PermissionError

try:
    schema = WowSQLSchema(
        project_url="https://your-project.wowsql.com",
        service_key="service_xyz..."
    )
    schema.create_table("test", [{"name": "id", "type": "INT"}])
except PermissionError as e:
    print(f"Permission denied: {e}")
    print("Make sure you're using a SERVICE ROLE KEY, not an anonymous key!")
except Exception as e:
    print(f"Error: {e}")
```

---

## Support

- Email: support@wowsql.com
- Discord: https://discord.gg/wowsql
- Documentation: https://wowsql.com/docs

---

Made with ❤️ by the WowSQL Team
