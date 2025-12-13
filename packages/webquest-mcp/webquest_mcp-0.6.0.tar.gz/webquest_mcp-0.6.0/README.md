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

The server reads its configuration from environment variables (or a `.env` file loaded automatically). Available settings:

- `OPENAI_API_KEY` (required): OpenAI API key for scrapers.
- `HYPERBROWSER_API_KEY` (required): Hyperbrowser API key.
- `AUTH_SECRET` (optional): JWT secret to enable authenticated requests. Leave unset to disable auth.
- `AUTH_AUDIENCE` (optional, default `webquest-mcp`): JWT audience to validate when auth is enabled.
- `TRANSPORT` (optional, default `stdio`): MCP transport. Supported values: `stdio`, `sse`, `streamable-http`.
- `PORT` (optional, default `8000`): Port to use when the transport is HTTP-based.

Example `.env`:

```text
OPENAI_API_KEY=your_openai_api_key
HYPERBROWSER_API_KEY=your_hyperbrowser_api_key
AUTH_SECRET=your_jwt_secret_key
AUTH_AUDIENCE=webquest-mcp
TRANSPORT=streamable-http
PORT=8000
```

### Token generation

To generate an authentication token for the MCP client, set the required environment variables and run the generator.

Required settings:

- `AUTH_SECRET`: JWT secret used by the server.
- `AUTH_SUBJECT`: Identifier for the client receiving the token.

Optional settings:

- `AUTH_AUDIENCE` (default `webquest-mcp`)
- `AUTH_EXPIRATION_DAYS` (default `365`)

Example `.env`:

```text
AUTH_SECRET=your-secret-key
AUTH_SUBJECT=client-name
AUTH_AUDIENCE=webquest-mcp
AUTH_EXPIRATION_DAYS=365
```

Run the generator:

```bash
webquest-mcp-token-generator
```

## Disclaimer

This tool is for educational and research purposes only. The developers of WebQuest MCP are not responsible for any misuse of this tool. Scraping websites may violate their Terms of Service. Users are solely responsible for ensuring their activities comply with all applicable laws and website policies.
