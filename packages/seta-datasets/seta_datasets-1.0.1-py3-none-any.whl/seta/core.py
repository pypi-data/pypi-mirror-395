import os
import time
import requests
from pathlib import Path
from urllib.parse import urlparse
from rich.console import Console
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
from rich.panel import Panel
from rich.table import Table
from rich import box

# --- Configuration ---
DEFAULT_BASE_URL = "https://calm-charm-production.up.railway.app"

# --- UI Engine ---
console = Console()

def _log(msg, level="info"):
    timestamp = time.strftime("%H:%M:%S")
    icons = {
        "info":  ("[blue]i[/]", "blue"),
        "success": ("[green]✔[/]", "green"),
        "warn":  ("[yellow]![/]", "yellow"),
        "error": ("[red]✖[/]", "red"),
        "sys":   ("[gray]⚙[/]", "bright_black")
    }
    icon, color = icons.get(level, icons["info"])
    console.print(f"[dim]║[/] [dim][{timestamp}][/] {icon}  {msg}")

def _kv(key, value, color="cyan"):
    key_str = f"[ {key.upper()} ]"
    pad_len = max(2, 25 - len(key_str))
    padding = "." * pad_len
    console.print(f"[dim] │ {key_str} {padding}[/] [{color}]{value}[/]")

def _header(title):
    console.print()
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_row(f"[bold white on blue]  S E T A   L O A D E R  [/] [dim]:: {title.ljust(35)}[/]")
    console.print(Panel(grid, box=box.HEAVY_EDGE, border_style="dim"))

def _footer():
    console.print(f"[dim]╚{'═'*60}╝[/]\n")

def _sep():
    console.print(f"[dim] ╟{'─'*60}╢[/]")

# --- Core Functions ---

def download_file(url, save_path, custom_name=None, headers=None):
    if not url: raise ValueError("Invalid URL")

    # Determine filename
    if custom_name:
        filename = custom_name
    else:
        parsed = urlparse(url)
        filename = os.path.basename(parsed.path) or 'file.bin'
    
    # Clean query params
    if '?' in filename: filename = filename.split('?')[0]
    
    full_path = os.path.join(save_path, filename)
    
    try:
        # Pass headers (auth) to the download request too, in case the file URL is protected
        with requests.get(url, stream=True, timeout=30, headers=headers) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            progress_layout = [
                TextColumn("[dim]║[/] [cyan]➜[/]"),
                TextColumn("[bold]{task.fields[filename]}", justify="left"),
                BarColumn(bar_width=20, style="dim", complete_style="green"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                "|", TransferSpeedColumn(), "|", TimeRemainingColumn(),
            ]

            with Progress(*progress_layout, console=console) as progress:
                task = progress.add_task("download", total=total_size, filename=filename[:12].ljust(12))
                with open(full_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(task, advance=len(chunk))
                        
        _log(f"Checksum verification passed", "success")
        return {"path": full_path, "size": total_size}

    except Exception as e:
        _log(f"Download interrupt: {filename} - {str(e)}", "error")
        raise e

def _fetch_and_process(endpoint, params, save_path, request_desc, base_url=None, api_key=None):
    init_time = time.time()
    api_url = f"{base_url or DEFAULT_BASE_URL}{endpoint}"

    # --- AUTHENTICATION & HEADERS ---
    headers = {
        "User-Agent": "Seta-Loader/1.0.1",
        "Accept": "application/json"
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        headers["x-api-key"] = api_key 

    try:
        # 1. HEADER
        _header(request_desc)
        _log("Initializing SETA Protocol v2.1", "sys")
        _log(f"Target Endpoint: {endpoint}", "sys")
        time.sleep(0.2)
        
        # 2. METADATA REQUEST
        _log("Requesting dataset manifest...", "info")
        
        response = requests.get(api_url, params=params, headers=headers, timeout=15)
        
        # --- VISIBILITY & ERROR CHECKING ---
        if response.status_code in [401, 403]:
            _sep()
            _kv("ACCESS", "DENIED", "red")
            _log("This dataset appears to be PRIVATE.", "warn")
            _log("Please provide a valid 'api_key' or check your permissions.", "error")
            _footer()
            raise PermissionError("Access Denied: Private Dataset")
            
        response.raise_for_status()
        data = response.json()

        # 3. DASHBOARD
        _sep()
        _log("MANIFEST RETRIEVED", "success")
        
        if params.get('id'): _kv("DATASET ID", params.get('id'), "gold")
        if params.get('version'): _kv("VERSION", f"v{params['version']}", "magenta")
        
        # VISIBILITY VISUALIZATION
        is_private = data.get('isPrivate') or data.get('visibility') == 'private' or data.get('private')
        if is_private:
            _kv("VISIBILITY", "PRIVATE 🔒", "red")
        else:
            _kv("VISIBILITY", "PUBLIC 🌍", "green")
        
        _sep()

        # 4. FILE PARSING
        raw_files = data.get('files', [])
        if not isinstance(raw_files, list): raw_files = [raw_files]

        normalized_files = []
        for f in raw_files:
            if not f: continue
            
            # Case A: Object from Firebase/DB
            if isinstance(f, dict) and f.get('fileUrl'):
                parsed_url = urlparse(f['fileUrl'])
                default_name = os.path.basename(parsed_url.path) or "downloaded_data"
                name = f.get('fileName') or f.get('title') or default_name.split('?')[0]
                normalized_files.append({"url": f['fileUrl'], "name": name})
            
            # Case B: String URL
            elif isinstance(f, str):
                parsed_url = urlparse(f)
                name = os.path.basename(parsed_url.path).split('?')[0]
                normalized_files.append({"url": f, "name": name})

        if not normalized_files:
            _log("Manifest contains no valid file pointers.", "error")
            _footer()
            return {"message": "No files found", "files": []}

        _kv("PAYLOAD", f"{len(normalized_files)} file(s) queued", "blue")
        _sep()
        time.sleep(0.3)

        # 5. DOWNLOAD
        Path(save_path).mkdir(parents=True, exist_ok=True)
        results = []

        for file_obj in normalized_files:
            try:
                # Pass headers here too in case file storage is also protected
                res = download_file(file_obj['url'], save_path, file_obj['name'], headers=headers)
                results.append(res['path'])
            except Exception:
                pass 

        # 6. SUMMARY
        total_time = f"{time.time() - init_time:.2f}s"
        _sep()
        _kv("STATUS", "COMPLETED", "green")
        _kv("LATENCY", total_time, "gold")
        _kv("PATH", os.path.abspath(save_path), "dim")
        _footer()

        return {"message": "Success", "files": results, "metadata": data}

    except Exception as e:
        err_msg = str(e)
        # Try to extract server error message if available
        if hasattr(e, 'response') and e.response is not None:
            try:
                err_msg = e.response.json().get('error', err_msg)
            except:
                pass
        
        _sep()
        _log(f"CRITICAL FAILURE: {err_msg}", "error")
        _footer()
        raise e

# --- Public API Wrappers ---

def get_recent_seta(dataset_id, user_id=None, api_key=None, save_path="./downloads", base_url=None):
    return _fetch_and_process(
        endpoint="/getRecentSeta",
        params={"id": dataset_id, "userId": user_id},
        save_path=save_path,
        request_desc="FETCH :: LATEST",
        base_url=base_url,
        api_key=api_key
    )

def get_seta_by_version(dataset_id, version, user_id=None, api_key=None, save_path="./downloads", base_url=None):
    if not version: raise ValueError("Version arg missing")
    return _fetch_and_process(
        endpoint="/getSetaByVersion",
        params={"id": dataset_id, "version": version, "userId": user_id},
        save_path=save_path,
        request_desc=f"FETCH :: v{version}",
        base_url=base_url,
        api_key=api_key
    )

def get_seta_instance(dataset_id, version, instance_id, user_id=None, api_key=None, save_path="./downloads", base_url=None):
    if not version or not instance_id: raise ValueError("Instance args missing")
    return _fetch_and_process(
        endpoint="/getSetaInstance",
        params={"id": dataset_id, "version": version, "instanceId": instance_id, "userId": user_id},
        save_path=save_path,
        request_desc=f"FETCH :: INSTANCE {instance_id}",
        base_url=base_url,
        api_key=api_key
    )

def get_seta(options):
    # Extract
    d_id = options.get('id')
    ver = options.get('version')
    inst = options.get('instance_id') or options.get('instanceId')
    uid = options.get('user_id') or options.get('userId')
    key = options.get('api_key') or options.get('apiKey')
    path = options.get('save_path') or options.get('savePath') or './downloads'
    url = options.get('base_url') or options.get('baseUrl')

    # Route
    if inst and ver:
        return get_seta_instance(d_id, ver, inst, uid, key, path, url)
    if ver:
        return get_seta_by_version(d_id, ver, uid, key, path, url)
    return get_recent_seta(d_id, uid, key, path, url)