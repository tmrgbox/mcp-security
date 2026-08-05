# Tool Poisoning MCP Server

Malicious MCP server used for security research (see the [root README](../README.md)).

⚠️ **Use only in isolated test environments. Do not deploy to production or expose without access controls.**

## Local stdio mode (default)

For MCP clients that launch a local process (Claude Desktop, Cursor stdio config):

```bash
uv run python tool_poisoning.py
```

## Remote mode (Streamable HTTP)

Expose the server over HTTP so clients connect to a URL instead of spawning a process.

### Run locally

```bash
uv run python tool_poisoning.py --transport streamable-http
```

The MCP endpoint is available at `http://127.0.0.1:8000/mcp`.

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_TRANSPORT` | `stdio` | Transport: `stdio`, `sse`, or `streamable-http` |
| `FASTMCP_HOST` | `0.0.0.0` (HTTP) / `127.0.0.1` (stdio) | Bind address |
| `FASTMCP_PORT` | `8000` | Listen port |

### Docker

```bash
docker compose up --build
```

Or without compose:

```bash
docker build -t tool-poisoning .
docker run -p 8000:8000 tool-poisoning
```

### Expose to the internet

For a quick public URL during testing, use a tunnel:

```bash
# Start the server first, then in another terminal:
cloudflared tunnel --url http://localhost:8000
# or
ngrok http 8000
```

Use the tunnel URL with `/mcp` appended (e.g. `https://abc123.ngrok-free.app/mcp`).

For a persistent deployment, host the Docker container on any platform that supports HTTP services (Fly.io, Railway, Render, AWS ECS, etc.) and point a domain at port 8000.

### Deploy on Railway

1. **Push to GitHub** — Railway deploys from a repo. Push this repository (or fork it) to GitHub.

2. **Create a Railway project**
   - Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
   - Select your `mcp-security` repository

3. **Set the root directory** — This repo is a monorepo, so point Railway at the server folder:
   - Open the service → **Settings** → **Source**
   - Set **Root Directory** to `tool-poisoning`

4. **Configure environment variables** (Settings → **Variables**):

   | Variable | Value |
   |----------|-------|
   | `MCP_TRANSPORT` | `streamable-http` |
   | `FASTMCP_HOST` | `0.0.0.0` |

   Railway injects `PORT` automatically; the server reads it at startup. Do not hardcode a port.

5. **Generate a public domain**
   - Service → **Settings** → **Networking** → **Generate Domain**
   - Railway gives you a URL like `https://tool-poisoning-production.up.railway.app`

6. **Connect Cursor** — Use the domain with `/mcp`:

   ```json
   {
     "mcpServers": {
       "tool-poisoning": {
         "url": "https://tool-poisoning-production.up.railway.app/mcp"
       }
     }
   }
   ```

7. **Verify the deployment**

   ```bash
   curl -i -X POST "https://YOUR-DOMAIN.up.railway.app/mcp" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}'
   ```

   A `200 OK` with an SSE `event: message` response means the server is live.

**CLI alternative** (if you prefer not to use the dashboard):

```bash
npm i -g @railway/cli
railway login
cd tool-poisoning
railway init
railway up
railway domain
```

⚠️ Railway's free tier has usage limits. This server is for research only — add auth (Railway private networking, API gateway, or reverse proxy) before sharing the URL publicly.

## Connect from Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tool-poisoning": {
      "url": "https://your-server.example.com/mcp"
    }
  }
}
```

For local testing:

```json
{
  "mcpServers": {
    "tool-poisoning": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

## Connect from other clients

Clients that only support stdio can bridge to the remote server with [fastmcp-remote](https://pypi.org/project/fastmcp-remote/):

```json
{
  "mcpServers": {
    "tool-poisoning": {
      "command": "uvx",
      "args": ["fastmcp-remote", "https://your-server.example.com/mcp"]
    }
  }
}
```

## Verify with MCP Inspector

1. Start the server in streamable-http mode.
2. Open [MCP Inspector](https://github.com/modelcontextprotocol/inspector).
3. Choose **Streamable HTTP** transport.
4. Enter `http://127.0.0.1:8000/mcp`.
