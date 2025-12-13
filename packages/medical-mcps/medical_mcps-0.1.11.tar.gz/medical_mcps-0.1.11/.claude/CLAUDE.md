# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

## Project Overview

**Biological APIs MCP Server** - An MCP server that integrates 13+ biological and medical databases
(Reactome, KEGG, UniProt, ChEMBL, PubMed, GWAS Catalog, ClinicalTrials.gov, OpenFDA, and more) into
a unified interface with 100+ tools.

The server supports:

-   **Unified endpoint**: Single connection to access all APIs
-   **Individual endpoints**: Separate connections per API (e.g., `/tools/reactome/mcp`)
-   **Local and remote deployment**: Development locally, production on Railway
-   **HTTP caching**: RFC 9111 compliant caching via hishel, 30-day TTL
-   **Sentry monitoring**: Optional error tracking and performance monitoring

## Development Setup

```bash
# Install dependencies with uv (Python package manager)
uv sync

# Start server with auto-reload (watches for code changes)
make server

# Run tests with auto-watch
make test-watch

# Run all tests
make test

# Run slow tests (Pathway Commons with 200s timeout)
make test-slow

# Start Docker containers with auto-rebuild
make docker-watch
```

### Key Commands

-   `make server` - HTTP server at http://localhost:8000 with auto-reload
-   `make test` - Run tests (excludes slow Pathway Commons tests)
-   `make test-all` - Run all tests including slow ones with 200s timeout
-   `make test-watch` - Auto-run tests on file changes
-   `make docker-watch` - Start Docker services with auto-rebuild (MCP at localhost:8000)

## Architecture

### High-Level Structure

The server is built on **FastMCP** (Anthropic's MCP SDK) with a multi-layer architecture:

```
HTTP Request
    ↓
http_server.py (Starlette ASGI app)
    ↓
/tools/{api_name}/mcp (Streamable HTTP transport)
    ↓
med_mcp_server.py (unified_mcp FastMCP instance)
    ↓
servers/ (Individual API servers with @medmcps_tool decorators)
    ↓
api_clients/ (HTTP clients with caching via hishel)
    ↓
External APIs (Reactome, KEGG, UniProt, ChEMBL, etc.)
```

### Key Components

**1. Central Hub: `med_mcp_server.py`**

-   Defines `unified_mcp` - a single FastMCP instance that aggregates all tools
-   Provides `@medmcps_tool` decorator - allows registering one function with multiple FastMCP
    servers
-   Used by all servers to register tools with both individual AND unified servers

**2. HTTP Server: `http_server.py`**

-   Starlette ASGI app with Sentry initialization
-   Mounts individual API servers at `/tools/{api_name}/mcp` (e.g., `/tools/reactome/mcp`)
-   Mounts unified server at `/tools/unified/mcp`
-   Uses AsyncExitStack to manage session lifecycles for all servers
-   Suppresses expected `ClosedResourceError` messages from MCP streamable HTTP

**3. Individual API Servers: `servers/{api_name}_server.py`**

-   One FastMCP instance per API (e.g., `reactome_mcp`, `kegg_mcp`)
-   Each server creates its own client instance
-   All tools decorated with `@medmcps_tool` which registers them with both their API server AND
    unified_mcp
-   Naming convention: `{api_name}_{tool_name}` (e.g., `reactome_get_pathway`,
    `chembl_search_molecules`)

**4. API Clients: `api_clients/{api_name}_client.py`**

-   Implements the actual API interaction logic
-   Uses httpx or library clients (e.g., chembl-webresource-client)
-   Inherits from `base_client.py` which handles:
    -   HTTP caching via hishel (transparent, RFC 9111 compliant)
    -   Retry logic via tenacity
    -   Error handling and logging
-   Each client is instantiated per-request with required API keys

### Data Flow Example: ChEMBL Molecule Search

```
User calls: chembl_search_molecules(query="ocrelizumab")
    ↓
http_server routes to /tools/unified/mcp
    ↓
unified_mcp.handle("tools/call") invokes chembl_search_molecules
    ↓
chembl_server.py chembl_search_molecules calls ChEMBLClient
    ↓
api_clients/chembl_client.py makes HTTP request
    ↓
hishel caches response to ~/.cache/medical-mcps/api_cache/chembl.db
    ↓
Response returned to user
```

## Adding a New API

### 1. Create API Client

File: `medical_mcps/api_clients/{api_name}_client.py`

```python
from .base_client import BaseClient

class MyAPIClient(BaseClient):
    def __init__(self, enable_cache: bool = True):
        super().__init__(cache_file=f"{api_name}.db", enable_cache=enable_cache)
        self.base_url = "https://api.example.com"

    async def get_resource(self, resource_id: str) -> dict:
        url = f"{self.base_url}/resource/{resource_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        return response.json()
```

### 2. Create API Server

File: `medical_mcps/servers/{api_name}_server.py`

```python
from mcp.server.fastmcp import FastMCP
from ..med_mcp_server import unified_mcp, tool as medmcps_tool
from ..api_clients.myapi_client import MyAPIClient

myapi_mcp = FastMCP("myapi", stateless_http=True, json_response=True)

@medmcps_tool(name="myapi_get_resource", servers=[myapi_mcp, unified_mcp])
async def myapi_get_resource(resource_id: str) -> dict:
    """Get a resource by ID.

    Args:
        resource_id: Resource identifier
    """
    client = MyAPIClient()
    return await client.get_resource(resource_id)
```

### 3. Register Server

File: `medical_mcps/http_server.py`

```python
# Add import
from .servers import myapi_server

# Add to lifespan - initialize session manager
await stack.enter_async_context(myapi_server.myapi_mcp.session_manager.run())

# Add to Mount list
Mount("/tools/myapi/mcp", myapi_server.myapi_mcp.aio_transport.asgi_app)
```

### 4. Naming Conventions

-   **Tools**: `{api_name}_{function_name}` (e.g., `myapi_get_resource`)
-   **Files**: `{api_name}_client.py`, `{api_name}_server.py`
-   **Server variable**: `{api_name}_mcp` (e.g., `myapi_mcp`)

## API Key Handling

**Important:** The server is stateless - it does NOT store API keys.

### Requiring API Keys

For APIs requiring authentication (OMIM, NCI):

1. Add `api_key: str` as a required parameter to all tools
2. Pass it to client during instantiation: `client = APIClient(api_key=api_key)`
3. Return clear error if missing: `"Error: API key is required. Get from <url>"`

Example:

```python
@medmcps_tool(name="omim_get_entry", servers=[omim_mcp, unified_mcp])
async def omim_get_entry(mim_number: str, api_key: str) -> dict:
    """Get OMIM entry by MIM number.

    Args:
        mim_number: MIM number
        api_key: OMIM API key (REQUIRED - get from https://omim.org/api)
    """
    if not api_key:
        return {"error": "API key is required. Get from https://omim.org/api"}
    client = OMIMClient(api_key=api_key)
    return await client.get_entry(mim_number)
```

## HTTP Caching

Most HTTP clients use **hishel** for transparent RFC 9111 compliant caching:

-   **Cache location**: `~/.cache/medical-mcps/api_cache/`
-   **TTL**: 30 days (default)
-   **Refresh**: TTL resets on access
-   **Per-API cache files**: Each API has its own SQLite cache (e.g., `reactome.db`)

To disable caching for a client:

```python
client = ReactomeClient(enable_cache=False)
```

To clear cache:

```bash
rm -rf ~/.cache/medical-mcps/api_cache/
```

## Testing

Tests are in `tests/` directory using pytest + tavern (API testing):

-   Standard pytest files for unit/integration tests
-   `.tavern.yaml` files for HTTP API contract tests
-   Slow tests (Pathway Commons) are skipped by `make test`, use `make test-slow` or `make test-all`

Key test markers:

-   `@pytest.mark.slow` - Marks slow tests (deselected by `make test`)

Run specific tests:

```bash
uv run pytest tests/test_filename.py -v
uv run pytest tests/test_filename.py::test_function_name -v
```

## Sentry Monitoring (Optional)

Sentry integration is optional. When configured, it tracks:

-   **MCP tool executions**: Tool name, arguments, results, errors
-   **HTTP requests**: All outgoing API calls (Reactome, KEGG, etc.)
-   **Errors**: All exceptions that cause 5xx responses
-   **Performance**: Request timing and transaction data

Configuration:

```bash
export SENTRY_DSN="your-sentry-dsn"
export SENTRY_ENVIRONMENT="production"  # or "local"
export SENTRY_TRACES_SAMPLE_RATE=1.0    # 100% of transactions
```

By default, Sentry does NOT include tool inputs/outputs (PII). To include:

```bash
export SENTRY_SEND_DEFAULT_PII=true
```

## Docker Deployment

Docker setup is in `docker-compose.yml`:

-   **MCP Backend**: Python service running uvicorn (port 8000)

```bash
make docker-watch    # Start with auto-rebuild
make docker-up       # Start in background
make docker-logs     # View logs
make docker-down     # Stop services
```

The Railway deployment (`railway.json`) is configured for production deployment.

## Deployment

**Production URL**: `https://medical-mcps-production.up.railway.app`

Endpoints available at both production and local URLs:

-   `/tools/unified/mcp` - All APIs (100+ tools)
-   `/tools/{api_name}/mcp` - Individual API servers

Recent commits show the project removed playbooks and added documentation updates.

## Important Implementation Details

### MCP Streamable HTTP Transport

-   Uses POST for JSON-RPC requests, optional GET for SSE streams
-   Mounted as ASGI app on FastAPI at `/mcp` path
-   Session managers must be initialized in lifespan context for async resource management
-   `ClosedResourceError` messages are expected and suppressed (see http_server.py)

### Tool Naming Convention

All tools are prefixed with API name for clarity:

-   `reactome_get_pathway`
-   `chembl_search_molecules`
-   `pubmed_search_articles`

This makes it clear which API is being used in unified endpoint.

### Error Handling in API Clients

-   `BaseClient` handles retries via tenacity
-   Clients raise exceptions on HTTP errors (`.raise_for_status()`)
-   Server tools catch exceptions and return error messages (no exceptions propagated to user)
-   Sentry captures errors for monitoring

## Related Files

-   **README.md**: Comprehensive user documentation, API descriptions, deployment info
-   **pyproject.toml**: Dependencies (mcp, httpx, starlette, uvicorn, hishel, tenacity, sentry-sdk)
-   **.env patterns**: SENTRY_DSN, SENTRY_ENVIRONMENT, MCP_HOST/PORT, OMIM_API_KEY
