"""
Hot-reload development server for HLA-Compass modules

Provides automatic reloading, real-time logging, and interactive testing UI.
"""

import os
import sys
import json
import time
import socket
import threading
import subprocess
import importlib
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
import asyncio
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from aiohttp import web
from aiohttp import ClientSession, ClientTimeout, WSMsgType, TCPConnector
import ssl

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .testing import ModuleTester
from .module import Module
from .config import Config

console = Console()
logger = logging.getLogger(__name__)


class ModuleReloader(FileSystemEventHandler):
    """Watches for file changes and triggers module reload"""
    
    def __init__(self, callback: Callable, paths: List[str], extensions: List[str] = None):
        self.callback = callback
        self.paths = paths
        self.extensions = extensions or ['.py', '.tsx', '.jsx', '.ts', '.js']
        self.last_reload = 0
        self.reload_delay = 1.0  # Debounce delay in seconds
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Check if file has a watched extension
        file_path = Path(event.src_path)
        if file_path.suffix not in self.extensions:
            return
            
        # Skip __pycache__ and other generated files
        if '__pycache__' in str(file_path) or '.pyc' in str(file_path):
            return
            
        # Debounce rapid changes
        current_time = time.time()
        if current_time - self.last_reload < self.reload_delay:
            return
            
        self.last_reload = current_time
        console.print(f"[yellow]⚡ File changed: {file_path.name}[/yellow]")
        self.callback(str(file_path))


class ModuleDevServer:
    """Development server with hot-reload and testing UI"""
    
    def __init__(
        self,
        module_dir: str = ".",
        port: int = 8080,
        *,
        online: bool = False,
        env: Optional[str] = None,
        proxy_routes: Optional[List[str]] = None,
        allow_writes: bool = False,
        frontend_proxy: bool = False,
        start_frontend: bool = False,
        frontend_port: int = 3000,
        ca_bundle: Optional[str] = None,
        verbose: bool = False,
    ):
        self.module_dir = Path(module_dir).resolve()
        self.port = port
        self.backend_dir = self.module_dir / "backend"
        self.frontend_dir = self.module_dir / "frontend"
        self.manifest_path = self.module_dir / "manifest.json"
        
        # Proxy / environment settings
        self.online = online
        self.env = env or Config.get_environment()
        # Update environment for Config if explicitly provided
        if env:
            os.environ["HLA_ENV"] = env
        self.api_base = Config.get_api_endpoint()
        self.proxy_routes = set((proxy_routes or []))
        self.allow_writes = allow_writes
        self.frontend_proxy = frontend_proxy
        self.start_frontend_process = start_frontend
        self.frontend_port = frontend_port
        self.verbose = verbose

        # TLS verification context for upstream API (online mode)
        self.ca_bundle = ca_bundle
        self.ssl_context: Optional[ssl.SSLContext] = None
        if self.online and self.ca_bundle:
            try:
                ctx = ssl.create_default_context(cafile=self.ca_bundle)
                # Enforce modern minimums
                ctx.minimum_version = ssl.TLSVersion.TLSv1_2
                self.ssl_context = ctx
            except Exception as e:
                raise RuntimeError(f"Failed to load CA bundle: {e}")

        # Local data roots (from optional .hla-compass-dev.json)
        self.local_roots: Dict[str, Path] = {}
        self._load_dev_config()
        
        # HTTP client for proxying
        self.http: Optional[ClientSession] = None
        
        # Module state
        self.module = None
        self.module_error = None
        self.reload_count = 0
        self.test_results = []
        
        # Load manifest
        self.manifest = self._load_manifest()
        self.module_name = self.manifest.get("name", "unknown")
        self.module_type = self.manifest.get("type", "no-ui")
        
        # File watcher
        self.observer = Observer()
        self.reloader = ModuleReloader(
            callback=self._reload_module,
            paths=[str(self.backend_dir)]
        )
        
        # Web server
        self.app = web.Application()
        self._setup_routes()
        
        # Frontend process (for UI modules)
        self.frontend_process = None
        self.frontend_log_thread = None
        
    def _load_manifest(self) -> Dict[str, Any]:
        """Load module manifest"""
        if not self.manifest_path.exists():
            console.print("[red]Error: manifest.json not found[/red]")
            return {}
            
        try:
            with open(self.manifest_path) as f:
                return json.load(f)
        except Exception as e:
            console.print(f"[red]Error loading manifest: {e}[/red]")
            return {}
    
    def _reload_module(self, changed_file: str = None):
        """Reload the module after file changes"""
        self.reload_count += 1
        console.print(f"[blue]🔄 Reloading module (#{self.reload_count})...[/blue]")
        
        try:
            # Clear any cached imports
            module_file = self.backend_dir / "main.py"
            if not module_file.exists():
                raise FileNotFoundError(f"Module file not found: {module_file}")
            
            # Remove from sys.modules to force reload
            module_name = "main"
            if module_name in sys.modules:
                del sys.modules[module_name]
            
            # Add backend dir to path if not already there
            if str(self.backend_dir) not in sys.path:
                sys.path.insert(0, str(self.backend_dir))
            
            # Import the module
            spec = importlib.util.spec_from_file_location("main", module_file)
            module = importlib.util.module_from_spec(spec)
            sys.modules["main"] = module
            spec.loader.exec_module(module)
            
            # Find the module class (inherits from Module)
            module_class = None
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, Module) and 
                    obj != Module):
                    module_class = obj
                    break
            
            if not module_class:
                raise ValueError("No Module subclass found in main.py")
            
            # Instantiate the module
            self.module = module_class()
            self.module_error = None
            
            console.print(f"[green]✓ Module reloaded successfully[/green]")
            
        except Exception as e:
            self.module_error = {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            }
            console.print(f"[red]✗ Reload failed: {e}[/red]")
            
            # Show helpful error messages
            self._show_error_help(e)
    
    def _show_error_help(self, error: Exception):
        """Display helpful error messages with suggestions"""
        error_type = type(error).__name__
        error_msg = str(error)
        
        suggestions = {
            "ModuleNotFoundError": "💡 Try: pip install -r backend/requirements.txt",
            "SyntaxError": "💡 Check for missing colons, brackets, or indentation",
            "ImportError": "💡 Check if the module is installed or the import path is correct",
            "AttributeError": "💡 Check if you're calling the right method or attribute",
            "TypeError": "💡 Check function arguments and types",
            "NameError": "💡 Check for typos in variable or function names"
        }
        
        if error_type in suggestions:
            console.print(f"[yellow]{suggestions[error_type]}[/yellow]")
    
    def _setup_routes(self):
        """Setup web server routes"""
        # API routes (local dev endpoints)
        self.app.router.add_get("/api/status", self.handle_status)
        self.app.router.add_post("/api/execute", self.handle_execute)
        self.app.router.add_get("/api/manifest", self.handle_manifest)
        self.app.router.add_get("/api/logs", self.handle_logs)
        
        # Dev-only data endpoints for local resources
        self.app.router.add_get("/dev/data/roots", self.handle_dev_data_roots)
        self.app.router.add_get("/dev/data/list", self.handle_dev_data_list)
        self.app.router.add_get("/dev/data/file", self.handle_dev_data_file)

        # Root route
        self.app.router.add_get("/", self.handle_index)
        # Backend testing UI explicitly under /backend
        self.app.router.add_get("/backend", self.handle_backend)

        # Optional frontend proxy under /ui
        if self.frontend_proxy:
            # Serve a lightweight wrapper at /ui that bootstraps the UI using the dev bundle
            self.app.router.add_get("/ui", self.handle_ui_wrapper)
            # Proxy any nested assets or HMR websocket paths under /ui if needed
            self.app.router.add_route("GET", "/ui/{tail:.*}", self.handle_ui_proxy)

        # Catch-all for /api/* to proxy selected routes to real API (online mode)
        for _m in ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"):
            self.app.router.add_route(_m, "/api/{tail:.*}", self.handle_api_proxy)

    def _load_dev_config(self):
        """Load optional dev config for local data roots and settings"""
        try:
            cfg_path = self.module_dir / ".hla-compass-dev.json"
            if cfg_path.exists():
                import json as _json
                data = _json.loads(cfg_path.read_text())
                # Load local roots
                roots = data.get("data", {}).get("localRoots", [])
                for entry in roots:
                    name = str(entry.get("name")).strip()
                    path = entry.get("path")
                    if not name or not path:
                        continue
                    p = Path(path).expanduser().resolve()
                    if p.exists() and p.is_dir():
                        self.local_roots[name] = p
        except Exception as e:
            console.print(f"[yellow]Warning: failed to load dev config: {e}[/yellow]")

    async def handle_api_proxy(self, request):
        """Selective proxy for /api/* to the real platform API in online mode.
        Falls back to 404 if not proxied and no local handler matched.
        """
        tail = request.match_info.get("tail", "")
        top = tail.split("/", 1)[0] if tail else ""

        # If a specific local endpoint matched previously, this handler wouldn't be called.
        # Here, we only proxy if online mode and route is allowed.
        if self.online and top in self.proxy_routes:
            method = request.method.upper()
            if method not in ("GET", "HEAD", "OPTIONS") and not self.allow_writes:
                return web.json_response(
                    {
                        "error": {
                            "type": "method_not_allowed",
                            "message": "Writes disabled in dev proxy (enable with --allow-writes)",
                        }
                    },
                    status=405,
                )

            # Build upstream URL: /api/<tail> -> {api_base}/v1/<tail>
            target = f"{self.api_base}/v1/{tail}"
            # Prepare headers (copy some, inject Authorization and correlation id)
            headers = {}
            # Preserve content-type and accept
            if request.headers.get("Content-Type"):
                headers["Content-Type"] = request.headers.get("Content-Type")
            headers["Accept"] = request.headers.get("Accept", "application/json")
            # Auth token
            token = Config.get_access_token()
            if not token:
                return web.json_response(
                    {"error": {"type": "auth_error", "message": "Not authenticated"}},
                    status=401,
                )
            headers["Authorization"] = f"Bearer {token}"
            # Correlation id if set
            corr = Config.get_correlation_id()
            if corr:
                headers["X-Correlation-Id"] = corr

            # Query params
            params = list(request.rel_url.query.items())
            # Body (if any)
            data = await request.read()

            # Perform request
            assert self.http is not None
            try:
                async with self.http.request(
                    method,
                    target,
                    params=params,
                    data=data if data else None,
                    headers=headers,
                ) as upstream:
                    resp = web.StreamResponse(status=upstream.status)
                    # Copy headers except hop-by-hop
                    hop = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "transfer-encoding", "upgrade"}
                    for k, v in upstream.headers.items():
                        if k.lower() not in hop:
                            resp.headers[k] = v
                    await resp.prepare(request)
                    async for chunk in upstream.content.iter_chunked(65536):
                        await resp.write(chunk)
                    await resp.write_eof()
                    logger.info(f"PROXY {method} /api/{tail} -> {target} [{upstream.status}]")
                    return resp
            except Exception as e:
                logger.error(f"PROXY error {method} {target}: {e}")
                return web.json_response(
                    {"error": {"type": "upstream_error", "message": str(e)}}, status=502
                )

        # Not proxied: return 404 to indicate no mock exists
        return web.json_response(
            {"error": {"type": "not_found", "message": f"No handler for /api/{tail}"}},
            status=404,
        )

    async def handle_dev_data_roots(self, request):
        """List configured local data roots by name"""
        return web.json_response({"roots": sorted(self.local_roots.keys())})

    async def handle_dev_data_list(self, request):
        """List files under a configured local root.
        Params: root=name, subdir=optional subdirectory within root
        """
        root_name = request.rel_url.query.get("root")
        subdir = request.rel_url.query.get("subdir", "")
        if not root_name or root_name not in self.local_roots:
            return web.json_response(
                {"error": {"type": "bad_request", "message": "Unknown or missing root"}},
                status=400,
            )
        base = self.local_roots[root_name]
        target = (base / subdir).resolve()
        try:
            target.relative_to(base)
        except Exception:
            return web.json_response(
                {"error": {"type": "bad_request", "message": "Path outside root"}},
                status=400,
            )
        if not target.exists() or not target.is_dir():
            return web.json_response(
                {"error": {"type": "not_found", "message": "Directory not found"}},
                status=404,
            )
        items = []
        for entry in target.iterdir():
            try:
                stat = entry.stat()
                items.append(
                    {
                        "name": entry.name,
                        "path": str(entry.relative_to(base)),
                        "type": "dir" if entry.is_dir() else "file",
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    }
                )
            except Exception:
                continue
        return web.json_response({"root": root_name, "items": sorted(items, key=lambda x: x["name"])})

    async def handle_dev_data_file(self, request):
        """Stream a file from a configured local root.
        Params: root=name, path=relative path under that root
        """
        import mimetypes
        root_name = request.rel_url.query.get("root")
        rel_path = request.rel_url.query.get("path")
        if not root_name or not rel_path or root_name not in self.local_roots:
            return web.json_response(
                {"error": {"type": "bad_request", "message": "Missing root or path"}},
                status=400,
            )
        base = self.local_roots[root_name]
        target = (base / rel_path).resolve()
        try:
            target.relative_to(base)
        except Exception:
            return web.json_response(
                {"error": {"type": "bad_request", "message": "Path outside root"}},
                status=400,
            )
        if not target.exists() or not target.is_file():
            return web.json_response(
                {"error": {"type": "not_found", "message": "File not found"}},
                status=404,
            )
        ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        return web.FileResponse(path=target, headers={"Content-Type": ctype})

    async def handle_ui_wrapper(self, request):
        """Serve a wrapper HTML that loads the dev bundle and mounts the UI.
        This avoids relying on webpack-dev-server to provide index.html and ensures
        consistent bootstrapping. The dev bundle is expected to expose a UMD global
        named 'ModuleUI' as configured in webpack (library: 'ModuleUI').
        """
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{self.module_name} - HLA-Compass UI Dev</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet" />
  <!-- Ant Design base reset (optional) -->
  <link rel="stylesheet" href="https://unpkg.com/antd@5/dist/reset.css" />
  <style>
    html, body, #root {{ height: 100%; margin: 0; }}
    body {{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif; }}
  </style>
</head>
<body>
  <div id="root"></div>
  <!-- Externals required by the dev UMD bundle (React, ReactDOM, Day.js, AntD, Icons) -->
  <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <!-- Day.js core and plugins required by AntD v5 date components -->
  <script src="https://unpkg.com/dayjs@1/dayjs.min.js"></script>
  <script src="https://unpkg.com/dayjs@1/plugin/customParseFormat.js"></script>
  <script src="https://unpkg.com/dayjs@1/plugin/advancedFormat.js"></script>
  <script src="https://unpkg.com/dayjs@1/plugin/weekday.js"></script>
  <script src="https://unpkg.com/dayjs@1/plugin/localeData.js"></script>
  <script src="https://unpkg.com/dayjs@1/plugin/weekOfYear.js"></script>
  <script src="https://unpkg.com/dayjs@1/plugin/weekYear.js"></script>
  <script>
    // Extend dayjs with commonly used plugins before AntD initializes
    (function() {{
      try {{
        if (window.dayjs) {{
          if (window.dayjs_plugin_customParseFormat) dayjs.extend(window.dayjs_plugin_customParseFormat);
          if (window.dayjs_plugin_advancedFormat) dayjs.extend(window.dayjs_plugin_advancedFormat);
          if (window.dayjs_plugin_weekday) dayjs.extend(window.dayjs_plugin_weekday);
          if (window.dayjs_plugin_localeData) dayjs.extend(window.dayjs_plugin_localeData);
          if (window.dayjs_plugin_weekOfYear) dayjs.extend(window.dayjs_plugin_weekOfYear);
          if (window.dayjs_plugin_weekYear) dayjs.extend(window.dayjs_plugin_weekYear);
        }} else {{
          console.error('dayjs failed to load before AntD.');
        }}
      }} catch (e) {{
        console.error('Failed to extend dayjs plugins:', e);
      }}
    }})();
  </script>
  <script src="https://unpkg.com/antd@5/dist/antd.min.js"></script>
  <script src="https://unpkg.com/@ant-design/icons@6/dist/index.umd.js"></script>
  <!-- Dev bundle from webpack-dev-server -->
  <script src="http://localhost:{self.frontend_port}/bundle.js"></script>
  <script>
    (function() {{
      // Helper to call module execute via dev server API
      async function onExecute(params) {{
        const res = await fetch('/api/execute', {{
          method: 'POST', headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ input: params }})
        }});
        return res.json();
      }}
      function mount() {{
        const rootEl = document.getElementById('root');
        const Comp = (window.ModuleUI && (window.ModuleUI.default || window.ModuleUI)) || null;
        if (!Comp) {{
          rootEl.innerHTML = '<pre style="padding:16px;color:#b91c1c">Error: ModuleUI UMD not found. Ensure webpack output.library is set to \"ModuleUI\".</pre>';
          return;
        }}
        const el = React.createElement(Comp, {{ onExecute }});
        if (window.ReactDOM && window.ReactDOM.createRoot) {{
          window.ReactDOM.createRoot(rootEl).render(el);
        }} else if (window.ReactDOM && window.ReactDOM.render) {{
          window.ReactDOM.render(el, rootEl);
        }} else {{
          rootEl.innerHTML = '<pre style="padding:16px;color:#b91c1c">Error: ReactDOM not available.</pre>';
        }}
      }}
      // Try mounting after a short delay to ensure bundle is loaded
      if (document.readyState === 'complete' || document.readyState === 'interactive') {{
        setTimeout(mount, 0);
      }} else {{
        window.addEventListener('DOMContentLoaded', mount);
      }}
    }})();
  </script>
</body>
</html>'''
        return web.Response(text=html, content_type="text/html")

    async def handle_ui_proxy(self, request):
        """Proxy /ui (and subpaths) to the local frontend dev server."""
        # Map /ui and /ui/* to upstream path
        tail = request.match_info.get("tail", "")
        upstream_path = tail or ""
        # Build target (http only)
        target = f"http://localhost:{self.frontend_port}/{upstream_path}"

        # WebSocket proxy (for HMR)
        if request.headers.get("Upgrade", "").lower() == "websocket":
            # Connect to upstream websocket
            assert self.http is not None
            qs = request.rel_url.query_string
            ws_target = target.replace("http", "ws", 1)
            if qs:
                ws_target = f"{ws_target}?{qs}"
            try:
                upstream_ws = await self.http.ws_connect(ws_target)
            except Exception as e:
                return web.json_response(
                    {"error": {"type": "upstream_ws_error", "message": str(e)}}, status=502
                )
            ws_server = web.WebSocketResponse()
            await ws_server.prepare(request)

            async def forward_client_to_upstream():
                async for msg in ws_server:
                    if msg.type == WSMsgType.TEXT:
                        await upstream_ws.send_str(msg.data)
                    elif msg.type == WSMsgType.BINARY:
                        await upstream_ws.send_bytes(msg.data)
                    elif msg.type == WSMsgType.CLOSE:
                        await upstream_ws.close()
                        break

            async def forward_upstream_to_client():
                async for msg in upstream_ws:
                    if msg.type == WSMsgType.TEXT:
                        await ws_server.send_str(msg.data)
                    elif msg.type == WSMsgType.BINARY:
                        await ws_server.send_bytes(msg.data)
                    elif msg.type in (WSMsgType.CLOSE, WSMsgType.ERROR):
                        await ws_server.close()
                        break

            await asyncio.gather(forward_client_to_upstream(), forward_upstream_to_client())
            return ws_server

        # HTTP proxy
        method = request.method
        headers = {k: v for k, v in request.headers.items() if k.lower() not in {"host", "content-length"}}
        data = await request.read()
        params = list(request.rel_url.query.items())
        assert self.http is not None
        try:
            async with self.http.request(method, target, params=params, data=data or None, headers=headers) as upstream:
                resp = web.StreamResponse(status=upstream.status)
                hop = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization", "te", "trailers", "transfer-encoding", "upgrade"}
                for k, v in upstream.headers.items():
                    if k.lower() not in hop:
                        resp.headers[k] = v
                await resp.prepare(request)
                async for chunk in upstream.content.iter_chunked(65536):
                    await resp.write(chunk)
                await resp.write_eof()
                logger.info(f"PROXY UI {method} /ui/{tail} -> {target} [{upstream.status}]")
                return resp
        except Exception as e:
            return web.Response(
                text=f"Frontend dev server not reachable on port {self.frontend_port}. Start it via 'cd frontend && npm run dev'.\nError: {e}",
                status=502,
                content_type="text/plain",
            )

    async def handle_index(self, request):
        """Serve the development UI or redirect to UI for with-ui modules"""
        # If this is a UI module and frontend proxy is enabled, send users to the UI by default
        if self.module_type == "with-ui" and self.frontend_proxy:
            raise web.HTTPFound(location="/ui")
        # Otherwise, show the backend testing UI
        html = self._generate_dev_ui()
        return web.Response(text=html, content_type="text/html")
    
    async def handle_status(self, request):
        """Get module status"""
        return web.json_response({
            "module_name": self.module_name,
            "module_type": self.module_type,
            "loaded": self.module is not None,
            "error": self.module_error,
            "reload_count": self.reload_count,
            "backend_dir": str(self.backend_dir),
            "frontend_dir": str(self.frontend_dir) if self.module_type == "with-ui" else None,
            "online": self.online,
            "env": self.env,
            "proxy_routes": sorted(list(self.proxy_routes)),
        })

    async def handle_backend(self, request):
        """Explicit backend testing UI under /backend"""
        html = self._generate_dev_ui()
        return web.Response(text=html, content_type="text/html")
    
    async def handle_execute(self, request):
        """Execute the module with test data"""
        if not self.module:
            return web.json_response({
                "status": "error",
                "error": self.module_error or {"message": "Module not loaded"}
            }, status=500)
        
        try:
            # Get input data from request
            data = await request.json()
            input_data = data.get("input", {})
            
            # Create mock context
            context = {
                "job_id": f"dev-test-{datetime.now().isoformat()}",
                "user_id": "dev-user",
                "organization_id": "dev-org",
                "timestamp": datetime.now().isoformat()
            }
            
            # Execute module via standard run wrapper (validates, handles errors, adds metadata)
            result = self.module.run(input_data, context)
            
            # Store test result
            self.test_results.append({
                "timestamp": datetime.now().isoformat(),
                "input": input_data,
                "output": result,
                "success": result.get("status") == "success"
            })
            
            return web.json_response(result)
            
        except Exception as e:
            error_response = {
                "status": "error",
                "error": {
                    "type": type(e).__name__,
                    "message": str(e),
                    "traceback": traceback.format_exc()
                }
            }
            return web.json_response(error_response, status=500)
    
    async def handle_manifest(self, request):
        """Get module manifest"""
        return web.json_response(self.manifest)
    
    async def handle_logs(self, request):
        """Get recent test results"""
        return web.json_response({
            "results": self.test_results[-10:],  # Last 10 results
            "total": len(self.test_results)
        })
    
    def _generate_dev_ui(self) -> str:
        """Generate the development UI HTML"""
        return '''<!DOCTYPE html>
<html>
<head>
    <title>HLA-Compass Dev Server</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #333;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status { 
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }
        .status.loaded { background: #10b981; color: white; }
        .status.error { background: #ef4444; color: white; }
        .status.loading { background: #f59e0b; color: white; }
        
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        
        .panel {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        h2 { 
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
        }
        
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 12px;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
            resize: vertical;
        }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 10px;
            transition: all 0.2s;
        }
        
        button:hover {
            background: #5a67d8;
            transform: translateY(-1px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        button:active { transform: translateY(0); }
        
        .output {
            background: #f7fafc;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 12px;
            margin-top: 10px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .output.success { border-color: #10b981; background: #f0fdf4; }
        .output.error { border-color: #ef4444; background: #fef2f2; }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f3f4f6;
        }
        
        .info-label { color: #6b7280; font-size: 14px; }
        .info-value { 
            color: #333;
            font-weight: 500;
            font-size: 14px;
            font-family: 'Monaco', 'Menlo', monospace;
        }
        
        .logs {
            margin-top: 15px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .log-entry {
            padding: 8px;
            margin-bottom: 5px;
            background: #f9fafb;
            border-radius: 6px;
            font-size: 13px;
            font-family: 'Monaco', 'Menlo', monospace;
        }
        
        .log-entry.success { background: #f0fdf4; }
        .log-entry.error { background: #fef2f2; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>
                🧬 HLA-Compass Dev Server
                <span id="status" class="status loading">Loading...</span>
            </h1>
            <p style="color: #6b7280; margin-top: 10px;">
                Hot-reload development environment for module testing
            </p>
        </div>
        
        <div class="grid">
            <div class="panel">
                <h2>📝 Input</h2>
                <textarea id="input" placeholder='{"param1": "value1", "param2": "value2"}'>{}</textarea>
                <button onclick="executeModule()">🚀 Execute Module</button>
                <button onclick="loadExample()" style="background: #6b7280; margin-left: 10px;">📄 Load Example</button>
            </div>
            
            <div class="panel">
                <h2>📊 Output</h2>
                <div id="output" class="output">Ready to execute...</div>
            </div>
            
            <div class="panel">
                <h2>ℹ️ Module Info</h2>
                <div class="info-item">
                    <span class="info-label">Name:</span>
                    <span class="info-value" id="module-name">-</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Type:</span>
                    <span class="info-value" id="module-type">-</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Reloads:</span>
                    <span class="info-value" id="reload-count">0</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Backend:</span>
                    <span class="info-value" id="backend-dir">-</span>
                </div>
            </div>
            
            <div class="panel">
                <h2>📜 Recent Executions</h2>
                <div id="logs" class="logs">
                    <div class="log-entry">No executions yet...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let moduleStatus = {};
        let exampleInput = {};
        
        // Load status on page load
        window.onload = async () => {
            await updateStatus();
            await loadManifest();
            setInterval(updateStatus, 2000); // Poll for changes
        };
        
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                moduleStatus = await response.json();
                
                const statusEl = document.getElementById('status');
                if (moduleStatus.error) {
                    statusEl.className = 'status error';
                    statusEl.textContent = 'Error';
                } else if (moduleStatus.loaded) {
                    statusEl.className = 'status loaded';
                    statusEl.textContent = 'Ready';
                } else {
                    statusEl.className = 'status loading';
                    statusEl.textContent = 'Loading...';
                }
                
                document.getElementById('module-name').textContent = moduleStatus.module_name;
                document.getElementById('module-type').textContent = moduleStatus.module_type;
                document.getElementById('reload-count').textContent = moduleStatus.reload_count;
                document.getElementById('backend-dir').textContent = 
                    moduleStatus.backend_dir?.split('/').slice(-2).join('/') || '-';
                    
            } catch (e) {
                console.error('Failed to update status:', e);
            }
        }
        
        async function loadManifest() {
            try {
                const response = await fetch('/api/manifest');
                const manifest = await response.json();
                
                // Create example input from manifest
                if (manifest.inputs) {
                    exampleInput = {};
                    for (const [key, schema] of Object.entries(manifest.inputs)) {
                        if (schema.type === 'string') {
                            exampleInput[key] = schema.default || 'example_value';
                        } else if (schema.type === 'number' || schema.type === 'integer') {
                            exampleInput[key] = schema.default || 10;
                        } else if (schema.type === 'boolean') {
                            exampleInput[key] = schema.default || false;
                        } else if (schema.type === 'array') {
                            exampleInput[key] = schema.default || [];
                        } else if (schema.type === 'object') {
                            exampleInput[key] = schema.default || {};
                        }
                    }
                    document.getElementById('input').value = JSON.stringify(exampleInput, null, 2);
                }
            } catch (e) {
                console.error('Failed to load manifest:', e);
            }
        }
        
        function loadExample() {
            document.getElementById('input').value = JSON.stringify(exampleInput, null, 2);
        }
        
        async function executeModule() {
            const inputEl = document.getElementById('input');
            const outputEl = document.getElementById('output');
            
            try {
                const input = JSON.parse(inputEl.value);
                
                outputEl.textContent = 'Executing...';
                outputEl.className = 'output';
                
                const response = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({input})
                });
                
                const result = await response.json();
                
                if (result.status === 'success') {
                    outputEl.className = 'output success';
                } else {
                    outputEl.className = 'output error';
                }
                
                outputEl.textContent = JSON.stringify(result, null, 2);
                
                // Update logs
                await updateLogs();
                
            } catch (e) {
                outputEl.className = 'output error';
                outputEl.textContent = 'Error: ' + e.message;
            }
        }
        
        async function updateLogs() {
            try {
                const response = await fetch('/api/logs');
                const data = await response.json();
                
                const logsEl = document.getElementById('logs');
                if (data.results.length === 0) {
                    logsEl.innerHTML = '<div class="log-entry">No executions yet...</div>';
                } else {
                    logsEl.innerHTML = data.results.reverse().map(r => {
                        const cls = r.success ? 'success' : 'error';
                        const time = new Date(r.timestamp).toLocaleTimeString();
                        return `<div class="log-entry ${cls}">${time} - ${r.success ? '✓' : '✗'} ${JSON.stringify(r.input).slice(0, 50)}...</div>`;
                    }).join('');
                }
            } catch (e) {
                console.error('Failed to update logs:', e);
            }
        }
    </script>
</body>
</html>'''
    
    def start_frontend_dev(self):
        """Start frontend development server for UI modules"""
        if self.module_type != "with-ui":
            return
            
        if not self.frontend_dir.exists():
            console.print("[yellow]No frontend directory found[/yellow]")
            return
            
        package_json = self.frontend_dir / "package.json"
        if not package_json.exists():
            console.print("[yellow]No package.json found in frontend[/yellow]")
            return
            
        try:
            # Install dependencies if node_modules doesn't exist, or if required packages are missing
            node_modules = self.frontend_dir / "node_modules"
            if not node_modules.exists():
                console.print("[blue]Installing frontend dependencies...[/blue]")
                subprocess.run(
                    ["npm", "install"],
                    cwd=self.frontend_dir,
                    check=True,
                    capture_output=True
                )
            else:
                # Verify a few key packages; if missing, run install to recover partial installs
                required = ["react", "react-dom", "antd", "@ant-design/icons", "recharts", "react-plotly.js"]
                missing: list[str] = []
                for pkg in required:
                    pkg_path = node_modules / Path(*pkg.split("/"))
                    if not pkg_path.exists():
                        missing.append(pkg)
                if missing:
                    console.print(f"[yellow]Detected missing frontend packages: {', '.join(missing)} — running npm install...[/yellow]")
                    subprocess.run(
                        ["npm", "install"],
                        cwd=self.frontend_dir,
                        check=True,
                        capture_output=True
                    )
            
            # Start webpack dev server
            console.print(f"[blue]Starting frontend dev server on port {self.frontend_port}...[/blue]")
            popen_kwargs: dict[str, Any] = {
                "cwd": self.frontend_dir,
            }
            if self.verbose:
                popen_kwargs.update(
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                )
            else:
                popen_kwargs.update(
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

            self.frontend_process = subprocess.Popen(
                ["npm", "run", "dev"],
                **popen_kwargs,
            )

            if self.verbose and self.frontend_process.stdout:
                self.frontend_log_thread = threading.Thread(
                    target=self._stream_frontend_output,
                    args=(self.frontend_process.stdout,),
                    daemon=True,
                )
                self.frontend_log_thread.start()

            # Detect immediate failures (e.g., webpack config errors)
            time.sleep(0.5)
            if self.frontend_process.poll() is not None:
                console.print(
                    f"[red]Frontend dev server exited early with code {self.frontend_process.returncode}."
                    + (" Check logs above for details." if self.verbose else " Rerun with --verbose for webpack output.")
                )
            
        except Exception as e:
            console.print(f"[yellow]Could not start frontend server: {e}[/yellow]")

    def _stream_frontend_output(self, stream):
        """Forward frontend dev server output to console."""
        try:
            for line in iter(stream.readline, ""):
                if not line:
                    break
                console.print(f"[cyan][frontend][/cyan] {line.rstrip()}")
        except Exception:
            # Avoid noisy stack traces if the stream is closed unexpectedly
            pass
        finally:
            try:
                stream.close()
            except Exception:
                pass
    
    def _find_available_port(self, start_port: int, max_tries: int = 100) -> int:
        """Find an available port starting from start_port"""
        for port_offset in range(max_tries):
            port = start_port + port_offset
            try:
                # Try to bind to the port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.bind(('localhost', port))
                    return port
            except OSError:
                # Port is in use, try next one
                continue
        raise RuntimeError(f"Could not find an available port in range {start_port}-{start_port + max_tries}")

    async def start(self):
        """Start the development server"""
        # Try to find an available port if the default is busy
        original_port = self.port
        try:
            self.port = self._find_available_port(self.port)
            if self.port != original_port:
                console.print(f"[yellow]⚠ Port {original_port} is busy, using port {self.port} instead[/yellow]")
        except RuntimeError as e:
            console.print(f"[red]Failed to find available port: {e}[/red]")
            raise

        console.print(Panel.fit(
            f"[bold green]🚀 Starting HLA-Compass Dev Server[/bold green]\n\n"
            f"Module: [cyan]{self.module_name}[/cyan]\n"
            f"Type: [cyan]{self.module_type}[/cyan]\n"
            f"Port: [cyan]http://localhost:{self.port}[/cyan]\n"
            f"Online: [cyan]{'Yes' if self.online else 'No'}[/cyan]  Env: [cyan]{self.env.upper()}[/cyan]\n"
            f"Proxy routes: [cyan]{', '.join(sorted(self.proxy_routes)) if self.online else '-'}[/cyan]\n\n"
            f"[yellow]Watching for changes...[/yellow]\n"
            f"Press [bold]Ctrl+C[/bold] to stop",
            title="Dev Server",
            border_style="green"
        ))
        
        # Initial module load
        self._reload_module()
        
        # Start file watcher
        self.observer.schedule(self.reloader, str(self.backend_dir), recursive=True)
        self.observer.start()
        
        # Start frontend dev server if UI module and requested
        if self.module_type == "with-ui" and self.start_frontend_process:
            self.start_frontend_dev()
        
        # Start HTTP client session for proxying
        if self.ssl_context:
            connector = TCPConnector(ssl=self.ssl_context)
            self.http = ClientSession(timeout=ClientTimeout(total=60), connector=connector)
        else:
            self.http = ClientSession(timeout=ClientTimeout(total=60))

        # Start web server
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.port)
        
        try:
            await site.start()
            console.print(f"\n[green]✓ Dev server running at http://localhost:{self.port}[/green]")
            console.print("[dim]Open /ui for the module UI (UI modules auto-redirect from /). Use /backend for the backend testing UI.[/dim]\n")
            
            # Keep running
            while True:
                await asyncio.sleep(1)
                
        except OSError as e:
            if "address already in use" in str(e).lower():
                console.print(f"[red]Port {self.port} is already in use. Trying to find another port...[/red]")
                # This shouldn't happen since we already checked, but handle it anyway
                raise
            else:
                raise
        except KeyboardInterrupt:
            console.print("\n[yellow]Shutting down...[/yellow]")
        finally:
            self.observer.stop()
            self.observer.join()
            
            if self.frontend_process:
                self.frontend_process.terminate()
                try:
                    self.frontend_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.frontend_process.kill()
                self.frontend_process = None
            if self.frontend_log_thread and self.frontend_log_thread.is_alive():
                self.frontend_log_thread.join(timeout=1)
                self.frontend_log_thread = None
            
            if self.http:
                await self.http.close()
            
            await runner.cleanup()


def run_dev_server(
    module_dir: str = ".",
    port: int = 8080,
    *,
    online: bool = False,
    env: Optional[str] = None,
    proxy_routes: Optional[List[str]] = None,
    allow_writes: bool = False,
    frontend_proxy: bool = False,
    start_frontend: bool = False,
    frontend_port: int = 3000,
    ca_bundle: Optional[str] = None,
    verbose: bool = False,
):
    """Entry point for dev server"""
    server = ModuleDevServer(
        module_dir,
        port,
        online=online,
        env=env,
        proxy_routes=proxy_routes,
        allow_writes=allow_writes,
        frontend_proxy=frontend_proxy,
        start_frontend=start_frontend,
        frontend_port=frontend_port,
        ca_bundle=ca_bundle,
        verbose=verbose,
    )
    
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        console.print("\n[green]Dev server stopped[/green]")
    except Exception as e:
        console.print(f"[red]Server error: {e}[/red]")
        raise
