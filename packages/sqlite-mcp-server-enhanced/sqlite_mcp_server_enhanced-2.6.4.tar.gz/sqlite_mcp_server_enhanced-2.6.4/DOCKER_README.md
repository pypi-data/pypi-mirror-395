# SQLite MCP Server

Last Updated December 6, 2025 - Production/Stable v2.6.4

[![GitHub](https://img.shields.io/badge/GitHub-neverinfamous/sqlite--mcp--server-blue?logo=github)](https://github.com/neverinfamous/sqlite-mcp-server)
[![Docker Pulls](https://img.shields.io/docker/pulls/writenotenow/sqlite-mcp-server)](https://hub.docker.com/r/writenotenow/sqlite-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-v2.6.4-green)
![Status](https://img.shields.io/badge/status-Production%2FStable-brightgreen)
[![PyPI](https://img.shields.io/pypi/v/sqlite-mcp-server-enhanced)](https://pypi.org/project/sqlite-mcp-server-enhanced/)
[![Security](https://img.shields.io/badge/Security-Enhanced-green.svg)](https://github.com/neverinfamous/sqlite-mcp-server/blob/master/SECURITY.md)
[![GitHub Stars](https://img.shields.io/github/stars/neverinfamous/sqlite-mcp-server?style=social)](https://github.com/neverinfamous/sqlite-mcp-server)
[![Type Safety](https://img.shields.io/badge/Pyright-Strict-blue.svg)](https://github.com/neverinfamous/sqlite-mcp-server)

The SQLite MCP Server transforms SQLite into a powerful, AI-ready database engine with **73 specialized tools**. It combines standard relational operations with advanced analytics, JSON operations, text and vector search, geospatial capabilities, and intelligent workflow automation. By layering business intelligence tools, semantic resources, and guided prompts on top of SQLite, it enables both developers and AI assistants to interact with data more naturally and effectively.

**🚀 Multiple Deployment Options:**
- **[Docker Hub](https://hub.docker.com/r/writenotenow/sqlite-mcp-server)** - Containerized with full 73-tool suite
- **[PyPI Package](https://pypi.org/project/sqlite-mcp-server-enhanced/)** - Simple pip install for Python environments  
- **[MCP Registry](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.neverinfamous/sqlite-mcp-server)** - Auto-discoverable by MCP clients

**📰 [Read the v2.6.0 Release Article](https://adamic.tech/articles/2025-09-22-sqlite-mcp-server-v2-6-0)** - Learn about JSON operations, auto-normalization, and enhanced security

## 📋 Table of Contents

- [🚀 Quick Try](#-quick-try)
- [🚀 Deployment Options](#-deployment-options)
  - [Option 1: PyPI Package (Simple)](#option-1-pypi-package-simple)
  - [Option 2: Docker Hub (Full Features)](#option-2-docker-hub-full-features)
  - [Option 3: Build from Source](#option-3-build-from-source)
- [Quick Start](#quick-start)
  - [Pull and Run](#pull-and-run)
  - [MCP Client Configuration](#mcp-client-configuration)
- [🎛️ Tool Filtering](#️-tool-filtering)
- [✅ Quick Test - Verify Everything Works](#-quick-test---verify-everything-works)
- [🛡️ Security Testing](#️-security-testing)
- [Key Features](#key-features)
  - [🆕 NEW in v2.6.4: Tool Filtering](#-new-in-v264-tool-filtering)
  - [Core Database Capabilities](#core-database-capabilities)
- [Available CLI Commands](#available-cli-commands)
- [Database Configuration](#database-configuration)
- [Statistical Analysis Workflow](#statistical-analysis-workflow)
- [Container Options](#container-options)
  - [Database Locations](#database-locations)
  - [Environment Variables](#environment-variables)
- [Available Tags](#available-tags)
- [Examples](#examples)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [🔍 AI-Powered Wiki Search](#-ai-powered-wiki-search)
- [Links](#links)

## 🚀 Quick Try

Copy and paste to run with Docker instantly:

```bash
docker run -i --rm \
  -v $(pwd):/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/sqlite_mcp.db
```

## ⚡ **Install to Cursor IDE**

### **One-Click Installation**

Click the button below to install directly into Cursor:

[![Install to Cursor](https://img.shields.io/badge/Install%20to%20Cursor-Click%20Here-blue?style=for-the-badge)](cursor://anysphere.cursor-deeplink/mcp/install?name=SQLite%20MCP%20Server&config=eyJzcWxpdGUtbWNwIjp7ImFyZ3MiOlsicnVuIiwiLWkiLCItLXJtIiwiLXYiLCIkKHB3ZCk6L3dvcmtzcGFjZSIsIndyaXRlbm90ZW5vdy9zcWxpdGUtbWNwLXNlcnZlcjpsYXRlc3QiLCItLWRiLXBhdGgiLCIvd29ya3NwYWNlL3NxbGl0ZV9tY3AuZGIiXSwiY29tbWFuZCI6ImRvY2tlciJ9fQ==)

Or copy this deep link:
```
cursor://anysphere.cursor-deeplink/mcp/install?name=SQLite%20MCP%20Server&config=eyJzcWxpdGUtbWNwIjp7ImFyZ3MiOlsicnVuIiwiLWkiLCItLXJtIiwiLXYiLCIkKHB3ZCk6L3dvcmtzcGFjZSIsIndyaXRlbm90ZW5vdy9zcWxpdGUtbWNwLXNlcnZlcjpsYXRlc3QiLCItLWRiLXBhdGgiLCIvd29ya3NwYWNlL3NxbGl0ZV9tY3AuZGIiXSwiY29tbWFuZCI6ImRvY2tlciJ9fQ==
```

### **Prerequisites**
- ✅ Docker installed and running
- ✅ ~500MB disk space available

**📖 [See Full Installation Guide →](https://github.com/neverinfamous/sqlite-mcp-server/wiki/Installation-and-Configuration)**

---

## 🚀 Deployment Options

### Option 1: PyPI Package (Simple)

**Fastest setup** - Install directly from PyPI and run locally:

Install the package:
```bash
pip install sqlite-mcp-server-enhanced
```

Add to MCP config (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "mcp-server-sqlite",
      "args": ["--db-path", "./database.db"]
    }
  }
}
```

Restart your MCP client and start using all 73 tools!

### Option 2: Docker Hub (Full Features)

**Complete containerized solution** with all dependencies included:

Pull the latest image:
```bash
docker pull writenotenow/sqlite-mcp-server:latest
```

Add to MCP config:
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "${workspaceFolder}:/workspace",
        "writenotenow/sqlite-mcp-server:latest",
        "--db-path", "/workspace/database.db"
      ]
    }
  }
}
```

#### 🛡️ **Supply Chain Security**

For enhanced security and reproducible builds, use SHA-pinned images:

Find available SHA tags at: https://hub.docker.com/r/writenotenow/sqlite-mcp-server/tags
Look for tags starting with "sha256-" for cryptographically verified builds

Option 1: Multi-arch manifest digest (recommended for security)
```bash
docker pull writenotenow/sqlite-mcp-server@sha256:<manifest-digest>
```

Option 2: Short SHA tags for convenience
```bash
docker pull writenotenow/sqlite-mcp-server:sha-abc1234
```

**MCP Config with Cryptographically Verified Image:**
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "${workspaceFolder}:/workspace",
        "writenotenow/sqlite-mcp-server@sha256:<manifest-digest>",
        "--db-path", "/workspace/database.db"
      ]
    }
  }
}
```

**How to Find SHA Tags:**
1. Visit the [Tags tab](https://hub.docker.com/r/writenotenow/sqlite-mcp-server/tags) above
2. **For convenience**: Use `sha-abc1234` tags (human-readable, multi-arch, 12-char commit hash)
3. **For maximum security**: Use `sha256-<hash>` tags (manifest digests, immutable, cryptographically verified)

**Understanding SHA Tags:**
- 🏷️ **`sha-abc1234`** - Short commit hash (12-char), multi-arch safe, human-readable
- 🔒 **`sha256-<manifest-digest>`** - Multi-arch manifest digest (works on all architectures, immutable)
- ⚠️ **Architecture-specific digests** - Only for debugging specific architectures

**Tag Strategy Optimizations (October 2025)**
- ✅ **Streamlined to 3 essential tags** - latest, v2.6.4, sha-abc1234 for registry reliability
- ✅ **Short SHA format** - More efficient uploads while maintaining full commit traceability
- ⚠️ **Removed `master-YYYYMMDD-...` timestamps** - These redundant tags caused upload bottlenecks

**Security Features:**
- ✅ **Build Provenance** - Cryptographic proof of build process
- ✅ **SBOM Available** - Complete software bill of materials
- ✅ **Supply Chain Attestations** - Verifiable build integrity

### Option 3: Build from Source

**Development and customization**:

Clone and build:
```bash
git clone https://github.com/neverinfamous/sqlite-mcp-server.git
```

Navigate to directory:
```bash
cd sqlite-mcp-server
```

Build Docker image:
```bash
docker build -t sqlite-mcp-server-local .
```

Or install locally:
```bash
pip install -r requirements.txt
```

Run locally:
```bash
python start_sqlite_mcp.py --db-path ./database.db
```

**Deployment Comparison:**

| Method | Setup Time | Features | Best For |
|--------|------------|----------|----------|
| **PyPI** | 30 seconds | All 73 tools, local Python | Quick setup, Python developers |
| **Docker** | 2 minutes | All 73 tools, isolated environment | Production, consistency |
| **Source** | 5 minutes | Customizable, latest development | Development, contributions |

## Quick Start

### Pull and Run

Pull from Docker Hub (recommended):
```bash
docker pull writenotenow/sqlite-mcp-server:latest
```

Or pull specific version:
```bash
docker pull writenotenow/sqlite-mcp-server:v2.6.4
```

Run with volume mount:
```bash
docker run -i --rm \
  -v /path/to/your/data:/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/database.db
```

### MCP Client Configuration

**Claude Desktop (mcp.json):**

```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/path/to/your/project:/workspace",
        "writenotenow/sqlite-mcp-server:latest",
        "--db-path", "/workspace/database.db"
      ]
    }
  }
}
```

**Cursor IDE:**

```json
{
  "sqlite-mcp-server": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm", 
      "-v", "${workspaceFolder}:/workspace",
      "writenotenow/sqlite-mcp-server:latest",
      "--db-path", "/workspace/database.db"
    ]
  }
}
```

## 🎛️ Tool Filtering

*New in v2.6.4*

Some MCP clients have tool limits (e.g., Windsurf's 100-tool limit). Use the `SQLITE_MCP_TOOL_FILTER` environment variable to expose only the tools you need.

### Filter Syntax

| Syntax | Description |
|--------|-------------|
| `-group` | Disable all tools in a group |
| `-tool` | Disable a specific tool |
| `+tool` | Re-enable a tool (useful after group disable) |

Rules are processed **left-to-right**, so order matters.

### Available Groups

| Group | Tools | Description |
|-------|-------|-------------|
| `core` | 5 | Basic CRUD: read_query, write_query, create_table, list_tables, describe_table |
| `fts` | 4 | Full-text search: fts_search, create_fts_table, rebuild_fts_index, hybrid_search |
| `vector` | 11 | Semantic/vector search and embeddings |
| `json` | 9 | JSON operations and validation |
| `virtual` | 8 | Virtual tables: CSV, R-Tree, series |
| `spatial` | 7 | SpatiaLite geospatial operations |
| `text` | 7 | Text processing: fuzzy, phonetic, regex |
| `stats` | 8 | Statistical analysis |
| `admin` | 14 | Database administration and PRAGMA |
| `misc` | 5 | Miscellaneous utilities |

### Docker Configuration with Tool Filtering

**Basic filtering (reduce to ~40 tools):**
```bash
docker run -i --rm \
  -e SQLITE_MCP_TOOL_FILTER="-vector,-stats,-spatial,-text" \
  -v $(pwd):/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/database.db
```

**MCP Config with filtering:**
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "SQLITE_MCP_TOOL_FILTER=-vector,-stats,-spatial,-text",
        "-v", "${workspaceFolder}:/workspace",
        "writenotenow/sqlite-mcp-server:latest",
        "--db-path", "/workspace/database.db"
      ]
    }
  }
}
```

### Common Configurations

**Windsurf (stay under 100 tools):**
```
SQLITE_MCP_TOOL_FILTER="-vector,-stats,-spatial,-text"
```

**Read-only mode:**
```
SQLITE_MCP_TOOL_FILTER="-write_query,-create_table"
```

**Core + JSON only (minimal footprint):**
```
SQLITE_MCP_TOOL_FILTER="-fts,-vector,-virtual,-spatial,-text,-stats,-admin,-misc"
```

**Disable admin but keep vacuum and backup:**
```
SQLITE_MCP_TOOL_FILTER="-admin,+vacuum_database,+backup_database"
```

See the [Tool Filtering Wiki](https://github.com/neverinfamous/sqlite-mcp-server/wiki/Tool-Filtering) for complete documentation.

## ✅ Quick Test - Verify Everything Works

**Test all 73 tools in 30 seconds:**

Quick smoke test:
```bash
python test_runner.py --quick
```

Standard comprehensive test (recommended):
```bash
python test_runner.py --standard
```

Full test suite with edge cases:
```bash
python test_runner.py --full
```

**Expected output:**
```
🚀 SQLite MCP Server Comprehensive Test Suite v2.6.4
================================================================

🔍 Environment Detection:
  ✅ SQLite 3.50.4 (JSONB supported)
  ✅ Python 3.13.X  
  ✅ MCP 1.14.0

📊 Testing 73 Tools across 14 categories...

✅ Core Database Operations (8/8 passed)
✅ JSON Helper Tools (6/6 passed)  
✅ JSON Operations (12/12 passed)  
✅ Text Processing (8/8 passed)
🎉 SUCCESS: All 73 tools tested successfully!
```

## 🛡️ Security Testing

**NEW: Comprehensive SQL injection protection testing**

Test SQL injection protection (from tests directory):
```bash
cd tests && python test_sql_injection.py
```

Expected result: 🛡️ Overall security posture: STRONG

**What it tests:**
- Protection against the SQL injection vulnerability found in original Anthropic SQLite MCP server
- 11 different attack vectors including multiple statements, UNION injection, blind injection
- Parameter binding protection with malicious payloads
- Stacked queries and comment-based injection attempts

**Security Features Validated:**
- ✅ **Parameter Binding**: All user inputs properly parameterized
- ✅ **Input Sanitization**: Malicious SQL patterns blocked
- ✅ **Query Isolation**: Multiple statements prevented
- ✅ **Injection Prevention**: UNION, blind, and time-based attacks blocked
- ✅ **Error Handling**: Secure error messages without information leakage

**Running Security Tests in Docker:**

Quick security validation:
```bash
docker run -i --rm \
  writenotenow/sqlite-mcp-server:latest \
  --test --security
```

Full security test suite:
```bash
docker run -i --rm \
  -v $(pwd):/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --test --security --full
```

## Key Features

### 🆕 **NEW in v2.6.4: Tool Filtering**

**Selectively enable/disable tools** via `SQLITE_MCP_TOOL_FILTER` environment variable:
- Address MCP client tool limits (Windsurf's 100-tool limit)
- Reduce token overhead by exposing only needed tools
- Group-based filtering and individual tool control

See [Tool Filtering](#️-tool-filtering) section above for details.

### **v2.6.3: Complete JSON Operations Suite**

**5 Major Improvements in this release:**

#### **🎯 JSON Helper Tools (Issue #25)**
* **6 new specialized tools** for simplified JSON operations: `json_insert`, `json_update`, `json_select`, `json_query`, `json_validate_path`, `json_merge`
* **Path-based operations** with security validation and auto-normalization
* **Multiple output formats** (structured, flat, raw) for flexible data extraction

#### **🤖 JSON Auto-Normalization (Issue #23)**  
* **Automatically fixes Python-style JSON**: single quotes, `True`/`False`, `None`, trailing commas
* **Configurable strict mode** for production environments requiring exact JSON compliance
* **Security-aware normalization** with malicious pattern detection

#### **🛡️ Parameter Binding Interface (Issue #28)**
* **Enhanced MCP tools** with optional `params` arrays for secure parameter binding
* **SQL injection prevention** using SQLite's built-in parameter binding protection
* **Backward compatible** - existing queries continue to work unchanged

#### **📦 Automatic Parameter Serialization (Issue #22)**
* **Direct object/array parameters** - no more manual `JSON.stringify()` required
* **Seamless integration** - dict/list objects automatically serialized to JSON
* **Cleaner API** for both humans and AI assistants

#### **🧠 Enhanced JSON Error Diagnostics (Issue #24)**
* **Intelligent error categorization** - structural, security, encoding issues identified
* **Contextual guidance** with specific suggestions for fixing complex JSON problems
* **Security violation detection** with clear messaging for suspicious patterns

**Universal Benefits:**
* **✅ Zero Breaking Changes**: All existing code continues to work
* **🧪 Fully Tested**: All 73 tools validated and working perfectly
* **🛡️ Enhanced Security**: Multiple layers of SQL injection protection

### **Core Database Capabilities**
* **🎯 Strict Type Safety**: Achieved clean bill of health with comprehensive strict type checking (Pyright/Pylance) across 7,000+ lines of code - improved maintainability, enhanced IDE support, and proactive bug prevention
* **Advanced Text Processing**: Comprehensive text analysis toolkit with 8 specialized tools: PCRE regex extraction/replacement, fuzzy matching with Levenshtein distance, phonetic matching (Soundex/Metaphone), text similarity analysis (Cosine/Jaccard), normalization operations, pattern validation, advanced multi-method search, and comprehensive text validation
* **Statistical Analysis Library**: Comprehensive statistical functions for data analysis including descriptive statistics, percentile analysis, and time series analysis
* **JSONB Binary Storage**: Efficient binary JSON storage for improved performance and reduced storage requirements
* **Transaction Safety**: All write operations automatically wrapped in transactions with proper rollback on errors
* **Foreign Key Enforcement**: Automatic enforcement of foreign key constraints across all connections
* **Advanced SQL Support**: Complex queries including window functions, subqueries, and advanced filtering
* **Business Intelligence**: Integrated memo resource for capturing business insights during analysis
* **Enhanced Error Handling**: Detailed diagnostics for JSON-related errors with specific suggestions for fixing issues
* **Multi-Level Caching**: Hierarchical caching for optimal performance
* **Pattern Recognition**: Automatic optimization of frequently executed queries
* **JSON Validation**: Prevents invalid JSON from being stored in the database
* **WAL Mode Compatible**: Works alongside the existing Write-Ahead Logging (WAL) journal mode
* **Comprehensive Schema Tools**: Enhanced tools for exploring and documenting database structure
* **Database Administration Tools**: Complete suite of maintenance tools including VACUUM, ANALYZE, integrity checks, performance statistics, and index usage analysis
* **Full-Text Search (FTS5)**: Comprehensive FTS5 implementation with table creation, index management, and enhanced search with BM25 ranking and snippets
* **Backup/Restore Operations**: Enterprise-grade backup and restore capabilities with SQLite backup API, integrity verification, and safety confirmations
* **Advanced PRAGMA Operations**: Comprehensive SQLite configuration management, performance optimization, and database introspection tools
* **Virtual Table Management**: Complete virtual table lifecycle management for R-Tree spatial indexing, CSV file access, and sequence generation
* **SpatiaLite Geospatial Analytics**: Enterprise-grade GIS capabilities with spatial indexing, geometric operations, and comprehensive spatial analysis
* **Enhanced Virtual Tables**: Smart CSV/JSON import with automatic data type inference, nested object flattening, and schema analysis
* **Semantic/Vector Search**: AI-native semantic search with embedding storage, cosine similarity, and hybrid keyword+semantic ranking
* **Vector Index Optimization**: Approximate Nearest Neighbor (ANN) search with k-means clustering and spatial indexing for sub-linear O(log n) performance
* **Intelligent MCP Resources**: Dynamic database meta-awareness with real-time schema, capabilities, statistics, search indexes, and performance insights
* **Guided MCP Prompts**: Intelligent workflow automation with semantic query translation, table summarization, database optimization, and hybrid search recipes<br><br>

⚠️ **Tool Count Consideration**
The SQLite MCP Server exposes 73 tools by default. MCP clients like Cursor may warn around 80 tools and can become unstable past \~100–120.

**🎛️ NEW in v2.6.4:** Use `SQLITE_MCP_TOOL_FILTER` to reduce tool count. See [Tool Filtering](#️-tool-filtering) section for details.

**Note:** Some MCP clients may display a different tool count in their interface summary due to how they count diagnostic tools. The actual number of usable tools is 73.

## Available CLI Commands

### **📊 Summary by Use Case**

### **For End Users:**
| Use Case | Command | Notes |
|----------|---------|-------|
| Production Server | `docker run ... writenotenow/sqlite-mcp-server:latest` | Main production command |
| Validate Installation | `docker run ... --test --standard` | Recommended after install |
| Quick Check | `docker run ... --test --quick` | 30-second verification |

### **For Developers & DevOps:**
| Use Case | Command | Notes |
|----------|---------|-------|
| CI/CD Pipeline | `docker run ... --test --quick` | Fast automated testing |
| Container Validation | `docker run ... --test --standard` | Pre-deployment check |

**Example Commands:**

Quick validation (30 seconds):
```bash
docker run -i --rm writenotenow/sqlite-mcp-server:v2.6.4 --test --quick
```

Standard testing (2-3 minutes):
```bash
docker run -i --rm writenotenow/sqlite-mcp-server:v2.6.4 --test --standard
```

Production server:
```bash
docker run -i --rm -v $(pwd):/workspace writenotenow/sqlite-mcp-server:latest --db-path /workspace/data.db
```

## Database Configuration

* **Auto-creates** `sqlite_mcp.db` in your project root if none exists (MCP requires persistence).
* **Connects to existing databases** via any SQLite file path.
* **Supports both relative and absolute paths**.

## 🎯 **JSON Helper Tools - Simplified Operations**

**NEW in v2.6.0:** Six powerful JSON helper tools make complex operations simple:

```javascript
// ✅ Insert JSON with auto-normalization
json_insert({
  "table": "products",
  "column": "metadata", 
  "data": {'name': 'Product', 'active': True, 'price': None}
})

// ✅ Update JSON by path
json_update({
  "table": "products",
  "column": "metadata",
  "path": "$.price",
  "value": 29.99,
  "where_clause": "id = 1"
})

// ✅ Query JSON with complex filtering
json_query({
  "table": "products",
  "column": "metadata",
  "filter_paths": {"$.category": "electronics"},
  "select_paths": ["$.name", "$.price"]
})
```

**Benefits for AI Teams:**
- ✅ Simplified JSON operations with dedicated tools
- ✅ Path-based updates and queries
- ✅ Automatic security protection with path validation
- ✅ Multiple output formats (structured, flat, raw)
- ✅ Auto-normalization handles Python-style JSON
- ✅ Intelligent error messages reduce debugging time

## Statistical Analysis Workflow

1. Explore data distribution → `descriptive_statistics`
2. Identify quartiles → `percentile_analysis`  
3. Analyze trends → `moving_averages`
4. Generate insights → `append_insight`

---

## Container Options

### Database Locations

Project database:
```bash
-v /host/project:/workspace --db-path /workspace/data/database.db
```

Dedicated data volume:
```bash
-v sqlite-data:/data --db-path /data/database.db
```

Temporary database:
```bash
--db-path :memory:
```

### Environment Variables

Debug mode:
```bash
-e SQLITE_DEBUG=true
```

Custom log directory:
```bash
-e SQLITE_LOG_DIR=/workspace/logs
```

---

## Available Tags

* `latest` – latest stable release (v2.6.4)
* `v2.6.4` – Production/Stable with tool filtering feature
* `v2.6.3` – Previous version with updated README and consistent version numbering
* `v2.6.2` – Corrected metadata and repository URLs
* `v2.6.1` – JSON Helper Tools and enhanced operations
---

## Examples

**Data Analysis Project**

```bash
docker run -i --rm \
  -v /Users/analyst/project:/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/analysis.db
```

**Development Environment**

```bash
docker run -i --rm \
  -v $(pwd):/workspace \
  -e SQLITE_DEBUG=true \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/dev.db
```

**CI/CD Testing**

Validate server functionality in CI/CD:
```bash
docker run -i --rm \
  writenotenow/sqlite-mcp-server:v2.6.4 \
  --test --quick
```

Full validation with test data:
```bash
docker run -i --rm \
  -v /tmp/test-data:/workspace \
  writenotenow/sqlite-mcp-server:v2.6.4 \
  --test --standard --db-path /workspace/test.db
```

---

## Advanced Usage

**Multi-Architecture Support**

* `linux/amd64` – Intel/AMD 64-bit
* `linux/arm64` – Apple Silicon, ARM64

**Resource Limits**

```bash
docker run -i --rm \
  --memory=512m --cpus=1.0 \
  -v $(pwd):/workspace \
  writenotenow/sqlite-mcp-server:latest
```

**Persistent Volumes**

Create volume:
```bash
docker volume create sqlite-data
```

Run with persistent volume:
```bash
docker run -i --rm \
  -v sqlite-data:/data \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /data/persistent.db
```

---

## Troubleshooting

* **Permission Issues**: Ensure volume mount paths have proper permissions
* **Database Not Found**: Check volume mount and file paths
* **Connection Issues**: Verify MCP client configuration

---

## 🔍 AI-Powered Wiki Search

**[→ Search the Documentation with AI](https://search.adamic.tech)**

Can't find what you're looking for? Use our **AI-powered search interface** to query the complete wiki documentation:

- 🤖 **AI-Enhanced Mode** - Get natural language answers with source attribution
- ⚡ **Vector Search Mode** - Find relevant documentation chunks instantly
- 📚 **Searches All 73 Tools** - Complete coverage of the entire wiki
- 🎯 **Context-Aware** - Understands your questions and provides relevant examples

**Example queries:**
- "How do I prevent SQL injection attacks?"
- "What statistical analysis tools are available?"
- "How do I set up vector search with embeddings?"

The search interface uses Cloudflare's AutoRAG technology to provide intelligent, context-aware answers from our comprehensive wiki documentation.

---

## Links

**Project Resources:**
* **🔍 AI-Powered Search**: [search.adamic.tech](https://search.adamic.tech) - Search the wiki with AI
* **📚 GitHub Gists**: [SQLite MCP Practical Examples](https://gist.github.com/neverinfamous/0c8ed77ddaff0edbe31df4f4e18c33ce) - 9 curated real-world use cases
* **GitHub**: [https://github.com/neverinfamous/sqlite-mcp-server](https://github.com/neverinfamous/sqlite-mcp-server)
* **Wiki Documentation**: [Comprehensive Documentation Wiki](https://github.com/neverinfamous/sqlite-mcp-server/wiki)
* **Quick Start Guide**: See main [README.md](https://github.com/neverinfamous/sqlite-mcp-server/blob/master/README.md) for overview
* **[Adamic Support Blog](https://adamic.tech/)** - Project announcements and releases

**Distribution Channels:**
* **Docker Hub**: [writenotenow/sqlite-mcp-server](https://hub.docker.com/r/writenotenow/sqlite-mcp-server)
* **PyPI Package**: [sqlite-mcp-server-enhanced](https://pypi.org/project/sqlite-mcp-server-enhanced/)
* **MCP Registry**: [Registry Entry](https://registry.modelcontextprotocol.io/v0/servers?search=io.github.neverinfamous/sqlite-mcp-server)