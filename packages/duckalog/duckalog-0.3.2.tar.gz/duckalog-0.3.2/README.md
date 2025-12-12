# Duckalog

[![PyPI version](https://badge.fury.io/py/duckalog.svg)](https://badge.fury.io/py/duckalog)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/duckalog.svg)](https://pypi.org/project/duckalog/)
[![Tests](https://github.com/legout/duckalog/workflows/Tests/badge.svg)](https://github.com/legout/duckalog/actions)
[![codecov](https://codecov.io/gh/legout/duckalog/branch/main/graph/badge.svg)](https://codecov.io/gh/legout/duckalog)
[![Security](https://github.com/legout/duckalog/workflows/Security/badge.svg)](https://github.com/legout/duckalog/actions/workflows/security.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/lint-ruff-blue.svg)](https://github.com/charliermarsh/ruff)

Duckalog is a Python library and CLI for building DuckDB catalogs from
declarative YAML/JSON configuration files. A single config file describes your
DuckDB database, attachments (other DuckDB files, SQLite, Postgres), Iceberg
catalogs, and views over Parquet/Delta/Iceberg or attached tables.

The goal is to make DuckDB catalogs reproducible, versionable, and easy to
apply in local workflows and automated pipelines.

---

## Features

- **Config-driven catalogs** – Define DuckDB views in YAML/JSON instead of
  scattering `CREATE VIEW` statements across scripts.
- **Multiple sources** – Views over S3 Parquet, Delta Lake, Iceberg tables, and
  attached DuckDB/SQLite/Postgres databases.
- **Attachments & catalogs** – Configure attachments and Iceberg catalogs in
  same config and reuse them across views.
- **Semantic layer** – Define business-friendly dimensions and measures on top of existing views for BI and analytics.
- **Safe credentials** – Use environment variables (e.g. `${env:AWS_ACCESS_KEY_ID}`)
  instead of embedding secrets.
- **CLI + Python API** – Build catalogs from command line or from Python
  code with the same semantics.
- **Web UI** – Interactive dashboard for catalog management, query execution, and data export (requires `duckalog[ui]`).

For a full product and technical description, see `docs/PRD_Spec.md`.

**Ready to try examples?** See the [`examples/`](examples/) directory for hands-on learning:

- 📊 **Multi-Source Analytics**: Combine Parquet, DuckDB, and PostgreSQL data
- 🔒 **Environment Variables Security**: Secure credential management patterns
- ⚡ **DuckDB Performance Settings**: Optimize memory, threads, and storage
- 🏷️ **Semantic Layer v2**: Business-friendly semantic models with dimensions and measures

---

## Installation

**Requirements:** Python 3.12 or newer

### Install from PyPI

[![PyPI version](https://badge.fury.io/py/duckalog.svg)](https://pypi.org/project/duckalog/) [![Downloads](https://pepy.tech/badge/duckalog)](https://pepy.tech/project/duckalog)

```bash
pip install duckalog
```

This installs the Python package and provides the `duckalog` CLI command.

### Install with UI support

For the web UI dashboard, install with optional UI dependencies:

```bash
pip install duckalog[ui]
```

#### **UI Dependencies**

The `duckalog[ui]` extra includes these core dependencies:

- **Starlette** (`starlette>=0.27.0`): ASGI web framework
- **Datastar Python SDK** (`datastar-python>=0.1.0`): Reactive web framework
- **Uvicorn** (`uvicorn[standard]>=0.20.0`): ASGI server
- **Background task support**: Built-in Starlette background tasks
- **CORS middleware**: Security-focused web access control

#### **Datastar Runtime Requirements**

The web UI uses **Datastar** for reactive, real-time updates:

- **No legacy fallback**: The UI exclusively uses Datastar patterns
- **Reactive data binding**: Automatic UI updates when data changes
- **Server-Sent Events**: Real-time communication for background tasks
- **Modern web patterns**: Built-in security and performance optimizations
- **Bundled assets**: Datastar v1.0.0-RC.6 is served locally for offline operation
- **Supply chain security**: No external CDN dependencies for the UI

The bundled Datastar JavaScript is served from `/static/datastar.js` and works offline without external network access.

#### **Optional Enhanced YAML Support**

For better YAML formatting preservation, install optional dependency:

```bash
pip install duckalog[ui,yaml]
# or
pip install ruamel.yaml>=0.17.0
```

This provides:
- **Comment preservation** in YAML configs
- **Formatting maintenance** during updates
- **Advanced YAML features** like anchors and aliases

### Verify Installation

```bash
duckalog --help
duckalog --version
```

### Alternative Installation Methods

**Development installation:**
```bash
git clone https://github.com/legout/duckalog.git
cd duckalog
pip install -e .
```

**Using uv (recommended for development):**
```bash
uv pip install duckalog
```

### Install with Remote Configuration Support

For loading configuration files from remote storage systems and exporting catalogs to cloud storage (S3, GCS, Azure, SFTP), install with remote dependencies:

```bash
pip install duckalog[remote]
```

#### **Remote Storage Support**

The `duckalog[remote]` extra includes support for:

- **fsspec** (`fsspec>=2023.6.0`): Unified filesystem interface for remote storage
- **requests** (`requests>=2.28.0`): HTTP/HTTPS support for remote configs

#### **Backend-Specific Extras**

For specific cloud storage backends, install additional extras:

```bash
# AWS S3 support
pip install duckalog[remote-s3]

# Google Cloud Storage support  
pip install duckalog[remote-gcs]

# Azure Blob Storage support
pip install duckalog[remote-azure]

# SFTP/SSH support
pip install duckalog[remote-sftp]
```

#### **Authentication**

Remote configurations use standard authentication methods for each backend:

- **S3**: AWS credentials via environment variables, `~/.aws/credentials`, or IAM role
- **GCS/GS**: Google Cloud credentials via `GOOGLE_APPLICATION_CREDENTIALS` or Application Default Credentials
- **Azure/ABFS/ADL**: Azure credentials via environment variables or managed identity
- **SFTP/SSH**: SSH config or environment variables
- **HTTPS**: No authentication required for public URLs

**Note**: Credentials are not embedded in URIs for security. Use standard authentication methods for each cloud provider.

---

## Quickstart

### 1. Create a minimal config

Create a file `catalog.yaml`:

```yaml
version: 1

duckdb:
  database: catalog.duckdb
  pragmas:
    - "SET memory_limit='1GB'"

views:
  - name: users
    source: parquet
    uri: "s3://my-bucket/data/users/*.parquet"
```

### 2. Initialize a new configuration

Duckalog makes it easy to get started with the `init` command, which generates a basic configuration template with educational examples:

```bash
# Create a basic YAML config (default)
duckalog init

# Create a JSON config with custom filename
duckalog init --format json --output my_config.json

# Create with custom database and project names
duckalog init --database sales.db --project sales_analytics

# Force overwrite existing file
duckalog init --force
```

The generated config includes:
- Sensible defaults for DuckDB settings
- Example views showing common data sources and patterns
- Educational comments explaining each section
- Valid, working configuration that can be immediately used

### 3. Build the catalog via CLI

```bash
duckalog build catalog.yaml
```

This will:

- Read `catalog.yaml`.
- Connect to `catalog.duckdb` (creating it if necessary).
- Apply pragmas.
- Create or replace the `users` view.

### 3. Generate SQL instead of touching the DB

```bash
duckalog generate-sql catalog.yaml --output create_views.sql
```

`create_views.sql` will contain `CREATE OR REPLACE VIEW` statements for all
views defined in the config.

### 4. Export catalogs to remote storage

Export built DuckDB catalogs directly to cloud storage:

```bash
# Export to Amazon S3
duckalog build catalog.yaml --db-path s3://my-bucket/catalogs/analytics.duckdb

# Export to Google Cloud Storage
duckalog build catalog.yaml --db-path gs://my-project-bucket/catalogs/analytics.duckdb

# Export to Azure Blob Storage
duckalog build catalog.yaml --db-path abfs://account@container/catalogs/analytics.duckdb \
  --azure-connection-string "DefaultEndpointsProtocol=https;AccountName=..."

# Export to SFTP server
duckalog build catalog.yaml --db-path sftp://server/path/catalogs/analytics.duckdb \
  --sftp-host server.com --sftp-key-file ~/.ssh/id_rsa

# Export with custom authentication
duckalog build catalog.yaml --db-path s3://secure-bucket/catalogs/analytics.duckdb \
  --fs-key AKIAIOSFODNN7EXAMPLE \
  --fs-secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

#### **Remote Export Authentication**

Remote export uses the same authentication patterns as remote configuration loading:

```bash
# AWS profiles (recommended)
duckalog build catalog.yaml --db-path s3://bucket/catalog.duckdb --aws-profile production

# Google Cloud service accounts
duckalog build catalog.yaml --db-path gs://bucket/catalog.duckdb \
  --gcs-credentials-file /path/to/service-account.json

# Azure managed identities or connection strings
duckalog build catalog.yaml --db-path abfs://account@container/catalog.duckdb \
  --azure-connection-string "DefaultEndpointsProtocol=https;..."

# SFTP with SSH keys
duckalog build catalog.yaml --db-path sftp://server/path/catalog.duckdb \
  --sftp-host server.com --sftp-key-file ~/.ssh/id_rsa
```

### 5. Validate a config

```bash
duckalog validate catalog.yaml
```

This parses and validates config (including env interpolation), without
connecting to DuckDB.

### 6. Explore Examples

```bash
# Try multi-source analytics
cd examples/data-integration/multi-source-analytics
python data/generate.py
duckalog build catalog.yaml

# Try environment variables security
cd examples/production-operations/environment-variables-security
python generate-test-data.py
python validate-configs.py dev

# Try DuckDB performance tuning
cd examples/production-operations/duckdb-performance-settings
python generate-datasets.py --size small
duckalog build catalog-limited.yaml
```

### 7. Use Remote Configuration

Duckalog supports loading configuration files directly from remote storage systems:

```bash
# Load config from S3
duckalog build s3://my-bucket/configs/catalog.yaml

# Load config from Google Cloud Storage
duckalog validate gs://my-project/configs/catalog.yaml

# Load config from Azure Blob Storage
duckalog generate-sql abfs://my-account@my-container/configs/catalog.yaml

# Load config from HTTPS URL
duckalog build https://raw.githubusercontent.com/user/repo/main/catalog.yaml

# Load config from SFTP server
duckalog validate sftp://user@server/path/configs/catalog.yaml
```

**Remote Configuration Features:**

- **Transparent usage**: Same CLI commands work with local and remote configs
- **Environment interpolation**: `${env:VAR}` patterns work with remote configs
- **SQL file references**: Remote configs can reference both local and remote SQL files
- **Error handling**: Clear error messages for authentication or connectivity issues
- **Timeout control**: Configurable timeout for remote fetching (default: 30 seconds)

**Limitations:**

- **Web UI**: Currently only supports local configuration files
- **Path resolution**: Relative paths are not resolved for remote configs
- **SQL file references**: Local SQL files in remote configs require manual download

### Custom Filesystem Authentication

For advanced authentication scenarios, you can pass pre-configured fsspec filesystem objects directly to the Python API or use CLI options for dynamic filesystem creation.

#### **Supported Cloud Providers**

Duckalog supports authentication for all major cloud storage providers through custom filesystems:

| Provider | Protocol | Authentication Methods | CLI Options |
|----------|----------|------------------------|-------------|
| **Amazon S3** | `s3://` | AWS credentials, profiles, IAM roles | `--fs-key/--fs-secret`, `--aws-profile` |
| **Google Cloud Storage** | `gs://` | Service accounts, ADC | `--gcs-credentials-file` |
| **Azure Blob Storage** | `abfs://` | Connection strings, account keys | `--azure-connection-string` |
| **GitHub** | `github://` | Personal access tokens, username/password | `--fs-token`, `--fs-key/--fs-secret` |
| **SFTP** | `sftp://` | SSH keys, passwords, key files | `--sftp-host`, `--sftp-key-file` |

#### **Python API with Custom Filesystems**

```python
import fsspec
from duckalog import load_config

# S3 with direct credentials
fs = fsspec.filesystem("s3", 
    key="AKIAIOSFODNN7EXAMPLE", 
    secret="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
)
config = load_config("s3://my-bucket/config.yaml", filesystem=fs)

# GitHub with personal access token
fs = fsspec.filesystem("github", token="ghp_xxxxxxxxxxxxxxxxxxxx")
config = load_config("github://user/repo/config.yaml", filesystem=fs)

# Azure with connection string
fs = fsspec.filesystem("abfs", 
    connection_string="DefaultEndpointsProtocol=https;AccountName=account;AccountKey=key;EndpointSuffix=core.windows.net"
)
config = load_config("abfs://account@container/config.yaml", filesystem=fs)

# SFTP with SSH key
fs = fsspec.filesystem("sftp", 
    host="sftp.example.com",
    username="user",
    private_key="~/.ssh/id_rsa"
)
config = load_config("sftp://user@sftp.example.com/path/config.yaml", filesystem=fs)

# Google Cloud with service account
fs = fsspec.filesystem("gcs", token="/path/to/service-account.json")
config = load_config("gs://my-bucket/config.yaml", filesystem=fs)
```

#### **CLI with Filesystem Options**

```bash
# S3 with direct credentials
duckalog build s3://bucket/config.yaml \
  --fs-key AKIAIOSFODNN7EXAMPLE \
  --fs-secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
  --fs-timeout 60

# S3 with AWS profile (recommended for production)
duckalog build s3://bucket/config.yaml \
  --aws-profile myprofile

# GitHub with personal access token
duckalog validate github://user/repo/config.yaml \
  --fs-token ghp_xxxxxxxxxxxxxxxxxxxx

# Azure with connection string
duckalog generate-sql abfs://account@container/config.yaml \
  --azure-connection-string "DefaultEndpointsProtocol=https;AccountName=account;AccountKey=key"

# Azure with account key authentication
duckalog build abfs://account@container/config.yaml \
  --fs-key myaccountname \
  --fs-secret myaccountkey

# SFTP with SSH key file
duckalog build sftp://user@server/path/config.yaml \
  --sftp-host sftp.example.com \
  --sftp-key-file ~/.ssh/id_rsa \
  --sftp-port 22

# SFTP with password authentication
duckalog build sftp://user@server/path/config.yaml \
  --sftp-host sftp.example.com \
  --fs-key username \
  --fs-secret password

# Google Cloud with service account file
duckalog validate gs://my-project/config.yaml \
  --gcs-credentials-file /path/to/service-account.json

# Anonymous access (public S3 buckets)
duckalog build s3://public-bucket/config.yaml \
  --fs-anon true

# HTTP/HTTPS (no authentication needed)
duckalog build https://raw.githubusercontent.com/user/repo/main/config.yaml
```

#### **Protocol Inference**

The CLI can automatically infer the filesystem protocol from the provided options:

```bash
# These commands will automatically use the correct protocol:
duckalog build s3://bucket/config.yaml --aws-profile myprofile    # → S3
duckalog build gs://bucket/config.yaml --gcs-credentials-file file.json   # → GCS
duckalog build github://user/repo/config.yaml --fs-token token    # → GitHub
duckalog build sftp://server/config.yaml --sftp-host server.com   # → SFTP
```

#### **Error Handling and Validation**

Duckalog provides comprehensive validation for filesystem options:

```bash
# Examples of helpful error messages
duckalog build s3://bucket/config.yaml --aws-profile myprofile --fs-key key
# Error: Cannot specify both --aws-profile and --fs-key

duckalog build sftp://server/config.yaml --sftp-key-file missing.txt
# Error: SFTP key file not found: missing.txt

duckalog build s3://bucket/config.yaml --fs-anon true --fs-key key
# Error: S3 with anonymous access doesn't require credentials

duckalog build gs://bucket/config.yaml --gcs-credentials-file invalid.json
# Error: GCS credentials file not found: invalid.json
```

#### **Benefits of Custom Filesystems**

- **Programmatic credential management** - No need to set environment variables
- **Testing scenarios** - Easy to inject test filesystems with mocked credentials
- **CI/CD integration** - Credentials can be passed securely from secrets
- **Multi-cloud support** - Different authentication methods for different backends
- **Backward compatibility** - Existing environment variable authentication preserved
- **Dynamic configuration** - Change authentication methods without environment setup

#### **Security Best Practices**

| Use Case | Recommended Method | Reason |
|----------|-------------------|---------|
| **Production deployments** | Environment variables | Most secure, no credentials in code |
| **CI/CD pipelines** | Custom filesystems | Secure credential injection |
| **Local development** | Environment variables or profiles | Easy and secure |
| **Testing** | Custom filesystems | Easy to mock and test |
| **One-off commands** | CLI options | Convenient for ad-hoc usage |

#### **Security Guidelines**

- **Environment variables remain most secure** for production use and regular workflows
- **Custom filesystems enable secure credential injection** in code and CI/CD
- **No credentials embedded in URIs** - maintains security principles
- **CLI credentials visible in process list** - be aware of this limitation
- **Use least privilege** - grant only necessary permissions to credentials
- **Rotate credentials regularly** - follow cloud provider best practices

#### **Troubleshooting**

**Common Issues:**

1. **"fsspec is required" error**
   ```bash
   pip install duckalog[remote]  # Install with remote dependencies
   ```

2. **Authentication failures**
   ```bash
   # Check credentials are correct
   # Verify cloud provider permissions
   # Test connectivity with cloud provider tools
   ```

3. **Timeout issues**
   ```bash
   # Increase timeout for slow connections
   duckalog build s3://bucket/config.yaml --fs-timeout 120
   ```

4. **Protocol inference not working**
   ```bash
   # Explicitly specify protocol
   duckalog build s3://bucket/config.yaml --fs-protocol s3 --fs-key key --fs-secret secret
   ```

### 8. Start the web UI

```bash
duckalog ui catalog.yaml
```

**Note**: The web UI currently only supports local configuration files. For remote configs, download them locally first:

```bash
# Download remote config locally
curl -o catalog.yaml https://raw.githubusercontent.com/user/repo/main/catalog.yaml

# Then use with UI
duckalog ui catalog.yaml
```

This starts a secure, reactive web-based dashboard at http://127.0.0.1:8000 with:

#### **Core Features**
- **View Management**: Create, edit, and delete catalog views
- **Query Execution**: Run SQL queries with real-time results
- **Data Export**: Export data as CSV, Excel, or Parquet
- **Schema Inspection**: View table and view schemas
- **Catalog Rebuild**: Rebuild catalog with updated configuration
- **Semantic Layer Explorer**: Browse semantic models with business-friendly labels
- **Model Details**: View dimensions and measures with expressions and descriptions

#### **Security Features**
- **Read-Only SQL Enforcement**: Only allows SELECT queries, blocks DDL/DML
- **Authentication**: Admin token protection for mutating operations (production mode)
- **CORS Protection**: Restricted to localhost origins by default
- **Background Task Processing**: Non-blocking database operations
- **Configuration Security**: Atomic, format-preserving config updates

#### **Technical Implementation**
- **Reactive UI**: Built with Datastar for real-time updates
- **Background Processing**: All database operations run in background threads
- **Format Preservation**: Maintains YAML/JSON formatting when updating configs
- **Error Handling**: Comprehensive security-focused error messages

#### **Production Deployment**
```bash
# Set admin token for production security
export DUCKALOG_ADMIN_TOKEN="your-secure-random-token"
duckalog ui catalog.yaml --host 0.0.0.0 --port 8000
```

**Dependencies**: Requires `duckalog[ui]` installation for Datastar and Starlette dependencies.

**Security**: See [docs/SECURITY.md](docs/SECURITY.md) for comprehensive security documentation.

---

## Python API

The `duckalog` package exposes the same functionality as the CLI with
convenience functions:

```python
from duckalog import build_catalog, generate_sql, validate_config
from duckalog.config_init import create_config_template

# Generate a basic configuration template
content = create_config_template(format="yaml")
print(content)

# Save a template to a file
create_config_template(
    format="yaml", 
    output_path="my_config.yaml",
    database_name="analytics.db",
    project_name="my_project"
)

# Build or update a catalog file in place
build_catalog("catalog.yaml")

# Generate SQL without executing it
sql = generate_sql("catalog.yaml")
print(sql)

# Validate config (raises ConfigError on failure)
validate_config("catalog.yaml")
```

You can also work directly with the Pydantic model:

```python
from duckalog import load_config

config = load_config("catalog.yaml")
for view in config.views:
    print(view.name, view.source)
```

---

## Configuration Overview

At a high level, configs follow this structure:

```yaml
version: 1

duckdb:
  database: catalog.duckdb
  install_extensions: []
  load_extensions: []
  pragmas: []

attachments:
  duckdb:
    - alias: refdata
      path: ./refdata.duckdb
      read_only: true

  sqlite:
    - alias: legacy
      path: ./legacy.db

  postgres:
    - alias: dw
      host: "${env:PG_HOST}"
      port: 5432
      database: dw
      user: "${env:PG_USER}"
      password: "${env:PG_PASSWORD}"

iceberg_catalogs:
  - name: main_ic
    catalog_type: rest
    uri: "https://iceberg-catalog.internal"
    warehouse: "s3://my-warehouse/"
    options:
      token: "${env:ICEBERG_TOKEN}"

views:
  # Parquet view
  - name: users
    source: parquet
    uri: "s3://my-bucket/data/users/*.parquet"

  # Delta view
  - name: events_delta
    source: delta
    uri: "s3://my-bucket/delta/events"

  # Iceberg catalog-based view
  - name: ic_orders
    source: iceberg
    catalog: main_ic
    table: analytics.orders

  # Attached DuckDB view
  - name: ref_countries
    source: duckdb
    database: refdata
    table: reference.countries

  # Raw SQL view
  - name: vip_users
    sql: |
      SELECT *
      FROM users
      WHERE is_vip = TRUE

semantic_models:
  # Business-friendly semantic model on top of existing view
  - name: sales_analytics
    base_view: sales_data
    label: "Sales Analytics"
    description: "Business metrics for sales analysis"
    tags: ["sales", "revenue"]
    dimensions:
      - name: order_date
        expression: "created_at::date"
        label: "Order Date"
        type: "date"
      - name: customer_region
        expression: "UPPER(customer_region)"
        label: "Customer Region"
        type: "string"
    measures:
      - name: total_revenue
        expression: "SUM(amount)"
        label: "Total Revenue"
        type: "number"
      - name: order_count
        expression: "COUNT(*)"
        label: "Order Count"
        type: "number"
```

### Semantic Models (v1)

Semantic models provide business-friendly metadata on top of existing views. **v1 is metadata-only** - no new DuckDB views are created, and no automatic query generation is performed.

**Key limitations in v1:**
- No joins between semantic models
- No automatic query generation 
- No time dimension handling
- Single base view per model

**Use semantic models to:**
- Define business-friendly names for technical columns
- Document dimensions and measures for BI tools
- Provide structured metadata for future UI features

### Semantic Models (v2)

Semantic layer v2 extends v1 with **joins, time dimensions, and defaults** while maintaining full backward compatibility.

**New v2 features:**
- **Joins**: Optional joins to other views (typically dimension tables)
- **Time dimensions**: Enhanced time dimensions with supported time grains
- **Defaults**: Default time dimension, primary measure, and default filters

```yaml
semantic_models:
  - name: sales_analytics
    base_view: sales_data
    label: "Sales Analytics"

    # v2: Joins to dimension views
    joins:
      - to_view: customers
        type: left
        on_condition: "sales.customer_id = customers.id"
      - to_view: products
        type: left
        on_condition: "sales.product_id = products.id"

    dimensions:
      # v2: Time dimension with time grains
      - name: order_date
        expression: "created_at"
        type: "time"
        time_grains: ["year", "quarter", "month", "day"]
        label: "Order Date"

      - name: customer_region
        expression: "customers.region"
        type: "string"
        label: "Customer Region"

    measures:
      - name: total_revenue
        expression: "SUM(sales.amount)"
        label: "Total Revenue"
        type: "number"

    # v2: Default configuration
    defaults:
      time_dimension: order_date
      primary_measure: total_revenue
      default_filters:
        - dimension: customer_region
          operator: "="
          value: "NORTH AMERICA"
```

**Backward Compatibility:**
- All existing v1 semantic models continue to work unchanged
- New v2 fields are optional and additive
- No breaking changes to existing validation rules

See the [`examples/semantic_layer_v2`](examples/semantic_layer_v2/) directory for a complete example demonstrating all v2 features.

### Environment variable interpolation

Any string value may contain `${env:VAR_NAME}` placeholders. During
`load_config`, these are resolved using `os.environ["VAR_NAME"]`. Missing
variables cause a `ConfigError`.

Examples:

```yaml
duckdb:
  pragmas:
    - "SET s3_access_key_id='${env:AWS_ACCESS_KEY_ID}'"
    - "SET s3_secret_access_key='${env:AWS_SECRET_ACCESS_KEY}'"
```

### Path Resolution

Duckalog automatically resolves relative paths to absolute paths, ensuring consistent behavior regardless of where Duckalog is executed from.

#### **Automatic Path Resolution**
- **Relative Paths**: Paths like `"data/file.parquet"` are automatically resolved relative to the configuration file's directory
- **Absolute Paths**: Already absolute paths (e.g., `"/absolute/path/file.parquet"` or `"C:\path\file.parquet"`) are preserved unchanged
- **Remote URIs**: Cloud storage URIs (`s3://`, `gs://`, `http://`) and database connections are not modified
- **Cross-Platform**: Works consistently on Windows, macOS, and Linux

#### **Security Features**
- **Directory Traversal Protection**: Prevents malicious path patterns (e.g., `"../../../etc/passwd"`)
- **Sandboxing**: Resolved paths are restricted to stay within reasonable bounds from the config directory
- **Validation**: Path resolution is validated to ensure security and accessibility

#### **Examples**

```yaml
# Relative paths (recommended)
views:
  - name: users
    source: parquet
    uri: "data/users.parquet"  # Resolved to: /path/to/config/data/users.parquet
    description: "User data relative to config location"

  - name: events
    source: parquet
    uri: "../shared/events.parquet"  # Resolved to: /path/to/../shared/events.parquet
    description: "Shared data from parent directory"

# Absolute paths (still supported)
views:
  - name: fixed_data
    source: parquet
    uri: "/absolute/path/data.parquet"  # Used as-is
    description: "Absolute path preserved unchanged"

# Remote URIs (not modified)
views:
  - name: s3_data
    source: parquet
    uri: "s3://my-bucket/data/file.parquet"  # Used as-is
    description: "S3 paths unchanged"
```

#### **Benefits**
- **Reproducible Builds**: Catalogs work consistently across different working directories
- **Flexible Project Structure**: Organize data files relative to configuration location
- **Portability**: Move configuration and data together without path updates
- **Safety**: Security validation prevents path traversal attacks

### Configuration Format Preservation

Duckalog automatically preserves your configuration file format when making updates through the web UI:

#### **YAML Format Preservation**
- Maintains comments and formatting
- Preserves indentation and structure
- Uses `ruamel.yaml` when available for best results
- Falls back to standard `pyyaml` if needed

#### **JSON Format Preservation**
- Maintains pretty-printed structure
- Preserves field ordering
- Uses 2-space indentation for readability

#### **Automatic Format Detection**
- **File Extension**: `.yaml`, `.yml`, `.json`
- **Content Analysis**: Analyzes file structure if extension is ambiguous
- **Smart Detection**: JSON detected by `{`/`[` starts, YAML otherwise

#### **Atomic Operations**
All configuration updates use atomic file operations:
1. Write to temporary file with new format
2. Validate the temporary file
3. Atomically replace original file
4. Clean up temporary files on failure
5. Reload configuration into memory

#### **In-Memory Configuration**
- Configuration changes take effect immediately
- No server restart required for updates
- Background tasks use latest configuration
- Failed updates don't affect running operations

---

## Contributing

We welcome contributions to duckalog! This section provides guidelines and instructions for contributing to the project.

### Development Setup

**Requirements:** Python 3.12 or newer

#### Automated Version Management

This project uses automated version tagging to streamline releases. When you update the version in `pyproject.toml` and push to the main branch, the system automatically:

- Extracts the new version from `pyproject.toml`
- Validates semantic versioning format (X.Y.Z)
- Compares with existing tags to prevent duplicates
- Creates a Git tag in format `v{version}` (e.g., `v0.1.0`)
- Triggers the existing `publish.yml` workflow to publish to PyPI

**Simple Release Process:**
```bash
# 1. Update version in pyproject.toml
sed -i 's/version = "0.1.0"/version = "0.1.1"/' pyproject.toml

# 2. Commit and push
git add pyproject.toml
git commit -m "bump: Update version to 0.1.1"
git push origin main

# 3. Automated tagging creates tag and triggers publishing
# Tag v0.1.1 is created automatically
# publish.yml workflow runs and publishes to PyPI
```

For detailed examples and troubleshooting, see:
- [Automated Version Tagging Documentation](docs/automated-version-tagging.md)
- [Version Update Examples](docs/version-update-examples.md)
- [Troubleshooting Guide](docs/troubleshooting-version-tagging.md)

#### Continuous Integration

Duckalog uses a streamlined GitHub Actions setup to keep CI predictable:

- **Tests workflow** runs Ruff + mypy on Python 3.12 and executes pytest on Ubuntu for Python 3.12 and 3.13. If tests fail, the workflow fails—no auto-generated smoke tests.
- **Security workflow** focuses on a curated set of scans: TruffleHog and GitLeaks for secrets, Safety + pip-audit for dependency issues, and Bandit + Semgrep for code-level checks. Heavy container or supply-chain scans run only when explicitly needed.
- **publish.yml** builds sdist + wheel once on Python 3.12, validates artifacts with `twine check`, smoke-tests the wheel, and then reuses the artifacts for Test PyPI, PyPI, or dry-run scenarios. Release jobs rely on the `Tests` workflow’s status rather than re-running the full test matrix.

For local development, we recommend:

- `uv run ruff check src/ tests/` to run lint checks (CI treats these as required).
- `uv run ruff format src/ tests/` to auto-format code (CI runs `ruff format --check` in advisory mode).
- `uv run mypy src/duckalog` to run type checks.

#### Using uv (recommended for development)

```bash
# Clone the repository
git clone https://github.com/legout/duckalog.git
cd duckalog

# Install in development mode
uv pip install -e .
```

#### Using pip

```bash
# Clone the repository
git clone https://github.com/legout/duckalog.git
cd duckalog

# Install in development mode
pip install -e .
```

#### Install development dependencies

```bash
# Using uv
uv pip install -e ".[dev]"

# Using pip
pip install -e ".[dev]"
```

### Coding Standards

We follow the conventions documented in [`openspec/project.md`](openspec/project.md):

- **Python Style**: Follow PEP 8 with type hints on public functions and classes
- **Module Structure**: Prefer small, focused modules over large monoliths
- **Configuration**: Use Pydantic models as the single source of truth for config schemas
- **Architecture**: Separate concerns between config, SQL generation, and engine layers
- **Naming**: Use descriptive, domain-aligned names (e.g., `AttachmentConfig`, `ViewConfig`)
- **Testing**: Keep core logic pure and testable; isolate I/O operations

### Testing

We use pytest for testing. The test suite includes both unit and integration tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=duckalog

# Run specific test file
pytest tests/test_config.py
```

**Testing Strategy:**
- **Unit tests**: Config parsing, validation, and SQL generation
- **Integration tests**: End-to-end catalog building with temporary DuckDB files
- **Deterministic tests**: Avoid network dependencies unless explicitly required
- **Test-driven development**: Add tests for new behaviors before implementation

### Change Proposal Process

For significant changes, we use OpenSpec to manage proposals and specifications:

1. **Create a change proposal**: Use the OpenSpec CLI to create a new change
   ```bash
   openspec new "your-change-description"
   ```

2. **Define requirements**: Write specs with clear requirements and scenarios in `changes/<id>/specs/`

3. **Plan implementation**: Break down the work into tasks in `changes/<id>/tasks.md`

4. **Validate your proposal**: Ensure it meets project standards
   ```bash
   openspec validate <change-id> --strict
   ```

5. **Implement and test**: Work through the tasks sequentially

See [`openspec/project.md`](openspec/project.md) for detailed project conventions and the OpenSpec workflow.

### Pull Request Guidelines

When submitting pull requests:

1. **Branch naming**: Use small, focused branches with the OpenSpec change-id (e.g., `add-s3-parquet-support`)

2. **Commit messages**: 
   - Keep spec changes (`openspec/`, `docs/`) and implementation changes (`src/`, `tests/`) clear
   - Reference relevant OpenSpec change IDs in PR titles or first commit messages

3. **PR description**: Include a clear description of the change and link to relevant OpenSpec proposals

4. **Testing**: Ensure all tests pass and add new tests for new functionality

5. **Review process**: Be responsive to review feedback and address all comments

We prefer incremental, reviewable PRs over large multi-feature changes.

### Getting Help

- **Project Documentation**: See [`plan/PRD_Spec.md`](plan/PRD_Spec.md) for the full product and technical specification
- **Project Conventions**: Refer to [`openspec/project.md`](openspec/project.md) for detailed development guidelines
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/legout/duckalog/issues)
- **Discussions**: Join project discussions on [GitHub Discussions](https://github.com/legout/duckalog/discussions)

Thank you for contributing to duckalog! 🚀

---
