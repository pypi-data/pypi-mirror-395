# WebQuest MCP

WebQuest MCP is a Model Context Protocol (MCP) server that exposes powerful web search and scraping tools to AI agents and MCP-compatible clients.

**Scrapers**

- **Any Article:** Extracts readable content from arbitrary web articles.
- **DuckDuckGo Search:** General web search using DuckDuckGo.
- **Google News Search:** News-focused search via Google News.
- **YouTube Search:** Search YouTube videos, channels, posts, and shorts.
- **YouTube Transcript:** Fetch transcripts for YouTube videos.

**Browsers**

- **Hyperbrowser:** A cloud-based browser service for running Playwright scrapers without managing infrastructure.

## Installation

Installing using pip:

```bash
pip install webquest-mcp
```

Installing using uv:

```bash
uv add webquest-mcp
```

## Usage

### Starting the server

To start the WebQuest MCP server, run:

```bash
webquest-mcp
```

This will launch the MCP server using the `streamable-http` transport. The server will listen for incoming connections from MCP-compatible clients (like Cursor, Windsurf, or other AI agents).

### Configuration

You can configure the server using either environment variables (recommended) or command-line arguments.

#### Environment variables

Create a `.env` file in your working directory with the following content:

```text
# Required API keys
OPENAI_API_KEY=your_openai_api_key
HYPERBROWSER_API_KEY=your_hyperbrowser_api_key

# Optional authentication (JWT)
AUTH_SECRET=your_jwt_secret_key
AUTH_AUDIENCE=webquest-mcp
```

#### Command-line arguments

Alternatively, you can pass configuration options directly when running the server:

```bash
webquest-mcp --openai_api_key "..." --hyperbrowser_api_key "..."
```

To see all available options, run:

```bash
webquest-mcp --help
```

### Token generation

To generate an authentication token for the MCP client, use the `webquest-mcp-token-generator` command. You need to provide a secret and a subject.

```bash
webquest-mcp-token-generator --auth_secret "your-secret-key" --auth_subject "client-name"
```

You can also configure these values using environment variables or a `.env` file.

## Disclaimer

This tool is for educational and research purposes only. The developers of WebQuest MCP are not responsible for any misuse of this tool. Scraping websites may violate their Terms of Service. Users are solely responsible for ensuring their activities comply with all applicable laws and website policies.
