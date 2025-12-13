import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional, Callable, List, Dict, Any
from urllib.parse import urlparse, parse_qs
import socket
import secrets 

import msal
import requests
import webbrowser

"""
SharePoint Graph API Client with OAuth authentication.
Supports file operations including upload, download, and listing.
"""

# -----------------------------------------------------------
# Local server for OAuth redirect
# -----------------------------------------------------------
class OAuthHandler(BaseHTTPRequestHandler):
    """
    Handles OAuth callback from Microsoft authentication.
    """

    # Now track both code and state
    auth_code_store = {"code": None, "state": None}

    def do_GET(self):
        """
        Parse the authorization callback and store auth code + state.
        """
        if self.path.startswith("/callback"):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)

            OAuthHandler.auth_code_store["code"] = params.get("code", [None])[0]
            OAuthHandler.auth_code_store["state"] = params.get("state", [None])[0]

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authentication complete.</h1>"
                b"<p>You can close this window.</p></body></html>"
            )
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """
        Suppress HTTP server logging to avoid noisy output.
        """
        pass


# -----------------------------------------------------------
# Main SharePoint Graph Client
# -----------------------------------------------------------
class GraphSharePointClient:
    """
    Client for interacting with SharePoint via Microsoft Graph API.
    
    Environment variables required:
    - SHAREPOINT_CLIENT_ID
    - SHAREPOINT_CLIENT_SECRET
    - SHAREPOINT_TENANT_ID
    - SHAREPOINT_URL_<SITE_KEY>

    NOTE: The only site-specific environment variable is SHAREPOINT_URL_<SITE_KEY>. 
    For example: 
    - SHAREPOINT_URL_PROGRAM=https://cpisf.sharepoint.com/sites/program
    - SHAREPOINT_URL_NZFT=https://cpisf.sharepoint.com/sites/NZFT-ProprietaryData
    
    where you'd pass the following depending on which site you want to connect to:
    - client = GraphSharePointClient("program")
    - client = GraphSharePointClient("nzft")
    
    Otherwise, you can use the same client ID, client secret, and tenant ID for all sites in the cpisf tenant. 
    """

    def __init__(
        self, 
        sharepoint_site_name: str,
        redirect_port: int = 8010,
        drive_name: str = "Documents"
    ):
        """
        Initialize SharePoint client.
        
        Parameters:
        - sharepoint_site_name: Suffix used in environment variables for specific site (i.e. program or nzft)
        - redirect_port: Port for OAuth callback server (default: 8010)
        - drive_name: Name of core SharePoint drive to use (default: "Documents". You should use Documents unless you have a specific reason to use a different drive)
        """
        site_key = sharepoint_site_name.strip().upper()

        self.client_id = os.getenv("SHAREPOINT_CLIENT_ID")
        self.client_secret = os.getenv("SHAREPOINT_CLIENT_SECRET")
        self.tenant_id = os.getenv("SHAREPOINT_TENANT_ID")
        self.site_url = os.getenv(f"SHAREPOINT_URL_{site_key}")

        if not all([self.client_id, self.client_secret, self.site_url, self.tenant_id]):
            raise ValueError(
                f"Missing environment variables for SharePoint configuration '{site_key}'. "
                f"Required: SHAREPOINT_CLIENT_ID, SHAREPOINT_CLIENT_SECRET, "
                f"SHAREPOINT_TENANT_ID, SHAREPOINT_URL_{site_key}"
            )

        # Parse site URL to extract site hostname + path
        # Example: https://contoso.sharepoint.com/sites/program
        parsed = urlparse(self.site_url)
        self.hostname = parsed.hostname
        self.site_path = parsed.path.lstrip("/")  # "sites/program"

        # get authority request link from our cpisf tenant.
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"

        # initialize msal client app
        self.client_app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=authority
        )

        # initialize access token, site ID, and drive ID (empty until retrieved)
        self.access_token: Optional[str] = None
        self.site_id: Optional[str] = None
        self.drive_id: Optional[str] = None
        self.drive_name = drive_name
        
        # initialize redirect port and redirect URI
        self.redirect_port = redirect_port
        self.redirect_uri = f"http://localhost:{redirect_port}/callback"

        # Define authorized SCOPES for our current API key. 
        # If these change, you'll need to update the API key in the Azure portal.
        self.scopes = [
            "https://graph.microsoft.com/Sites.Read.All",
            "https://graph.microsoft.com/Sites.ReadWrite.All"
        ]

    # -------------------------------------------------------
    # Context Manager Support
    # -------------------------------------------------------
    def __enter__(self):
        """Enable context manager usage."""
        self.authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cleanup on context exit. 
        Doesn't do anything, just required for context manager protocol.
        """
        pass

    # -------------------------------------------------------
    # LOGIN FLOW
    # -------------------------------------------------------
    def authenticate(self):
        """
        Perform interactive login and initialize site/drive information.
        Opens default browser for user authentication.
        """
        # Reset auth code + state
        OAuthHandler.auth_code_store["code"] = None
        OAuthHandler.auth_code_store["state"] = None

        # Find an available port first before opening browser
        actual_port = self._find_available_port(self.redirect_port)

        # Update redirect_uri to use the actual port
        if actual_port != self.redirect_port:
            print(f"ℹ️  Port {self.redirect_port} unavailable, using port {actual_port} instead")
            self.redirect_port = actual_port
            self.redirect_uri = f"http://localhost:{actual_port}/callback"

        # Generate a random state value for CSRF protection
        state = secrets.token_urlsafe(32)

        # Generate auth URL with redirect URI + state
        auth_url = self.client_app.get_authorization_request_url(
            self.scopes,
            redirect_uri=self.redirect_uri,
            state=state,
        )

        print("Opening browser for authentication...")
        webbrowser.open(auth_url)

        # Run local server on the confirmed available port
        server_error = None

        def run_server_wrapper():
            nonlocal server_error
            try:
                httpd = HTTPServer(("localhost", actual_port), OAuthHandler)
                httpd.handle_request()
                httpd.server_close()
            except Exception as e:
                server_error = e

        # Thread to run the local server and wait for the user to sign in
        server_thread = threading.Thread(target=run_server_wrapper)
        server_thread.start()
        server_thread.join()

        if server_error:
            raise server_error

        code = OAuthHandler.auth_code_store["code"]
        returned_state = OAuthHandler.auth_code_store["state"]

        if not code:
            raise RuntimeError("Did not receive authorization code from Microsoft.")
        if returned_state != state:
            raise RuntimeError("State mismatch in OAuth callback; aborting authentication.")

        # After signing in, pull the access token
        result = self.client_app.acquire_token_by_authorization_code(
            code=code,
            scopes=self.scopes,
            redirect_uri=self.redirect_uri,
        )

        if "access_token" not in result:
            error_msg = result.get("error_description", result.get("error", "Unknown error"))
            raise RuntimeError(f"Authentication failed: {error_msg}")

        # Store the access token
        self.access_token = result["access_token"]
        print("✔ Logged in successfully!")

        # Initialize site and drive information
        self._init_site_and_drive()

    
    def _find_available_port(self, start_port: int, max_attempts: int = 10) -> int:
        """
        Find an available port starting from start_port.
        Just a utility function to find an available port for the OAuth callback.
        
        Parameters:
        - start_port: Port to start checking from
        - max_attempts: Maximum number of ports to try
            
        Returns:
        - An available port number
        """        
        for attempt in range(max_attempts):
            try_port = start_port + attempt
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(("localhost", try_port))
                sock.close()
                return try_port
            except OSError:
                sock.close()
                if attempt == max_attempts - 1:
                    raise RuntimeError(
                        f"Could not find available port. Tried ports {start_port}-{start_port + max_attempts - 1}"
                    )
                continue

    def _refresh_token(self) -> bool:
        """
        Attempt to refresh access token silently, so user doesn't have to re-authenticate.
        
        Returns:
        - True if token was refreshed successfully, False otherwise
        """
        accounts = self.client_app.get_accounts()
        if not accounts:
            return False

        result = self.client_app.acquire_token_silent(
            self.scopes, account=accounts[0]
        )
        
        if result and "access_token" in result:
            self.access_token = result["access_token"]
            return True
        
        return False

    def _ensure_authenticated(self):
        """Ensure we have a valid access token."""
        if not self.access_token:
            raise RuntimeError("Not authenticated. Call client.authenticate() first.")
        
        # Try to refresh token if it might be expired
        # (In production, you'd check expiration time)
        if not self._refresh_token():
            # Token refresh failed - might need re-authentication
            pass

    # -------------------------------------------------------
    # Initialize site and drive IDs
    # -------------------------------------------------------
    def _init_site_and_drive(self):
        """
        After authentication, retrieve site ID and document library drive ID.
        i.e. for Program and core Documents drive.

        Note that these are not the same as the site path and drive name, but rather unique numeric IDs for those sites and drives.
        They are actually static IDs that do not change, so we can hardcode them, but leaving flexible for now in case we need to change them in the future.

        """
        if not self.access_token:
            raise RuntimeError("Call client.authenticate() first")

        # Get site ID
        url = f"https://graph.microsoft.com/v1.0/sites/{self.hostname}:/{self.site_path}"
        try:
            r = requests.get(url, headers=self._headers())
            r.raise_for_status()
            self.site_id = r.json()["id"]
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"Failed to resolve SharePoint site: {e}")

        # Get drives for this site
        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives"
        try:
            r = requests.get(url, headers=self._headers())
            r.raise_for_status()
            drives = r.json()["value"]
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"Failed to retrieve drives: {e}")

        if not drives:
            raise RuntimeError("No drives found for this SharePoint site")

        # Try to find the specified drive, fallback to first drive
        self.drive_id = next(
            (d["id"] for d in drives if d.get("name") == self.drive_name),
            drives[0]["id"]
        )
        
        actual_drive_name = next(
            (d["name"] for d in drives if d["id"] == self.drive_id),
            "Unknown"
        )
        
        print(f"✔ Site ID found")
        print(f"✔ Core drive found. All file paths can be relative to: {actual_drive_name}")

    def _headers(self) -> Dict[str, str]:
        """Get authorization headers for API requests."""
        return {"Authorization": f"Bearer {self.access_token}"}

    def _format_bytes(self, num_bytes: int) -> str:
        """Pretty-print file sizes for summaries."""
        units = ["bytes", "KB", "MB", "GB", "TB"]
        size = float(max(num_bytes, 0))
        for unit in units:
            if size < 1024 or unit == units[-1]:
                if unit == "bytes":
                    return f"{int(size)} bytes"
                return f"{size:.2f} {unit}"
            size /= 1024
        
    def _build_sharepoint_manifest(self, folder_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
            """
            Gather metadata for items inside a SharePoint folder.

            Parameters:
            - folder_path: Path to the SharePoint folder relative to the drive root
            - recursive: If True (default), traverse all subfolders recursively.
                        If False, only include immediate children.

            Returns:
            - List of dictionaries describing files and folders inside the folder
            """
            self._ensure_authenticated()
            normalized_path = folder_path.strip("/")
            manifest: List[Dict[str, Any]] = []
            base_url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives/{self.drive_id}"

            def fetch_children(sp_path: str, relative_prefix: str = ""):
                if sp_path:
                    url = f"{base_url}/root:/{sp_path}:/children"
                else:
                    url = f"{base_url}/root/children"

                next_link = url
                while next_link:
                    try:
                        response = requests.get(next_link, headers=self._headers())
                        response.raise_for_status()
                    except requests.exceptions.HTTPError as e:
                        if response.status_code == 404:
                            raise FileNotFoundError(
                                f"SharePoint folder not found: {folder_path}"
                            ) from e
                        raise RuntimeError(f"Failed to traverse SharePoint folder: {e}")

                    data = response.json()
                    items = data.get("value", [])

                    for item in items:
                        sp_child_path = f"{sp_path}/{item['name']}".strip("/")
                        relative_path = f"{relative_prefix}{item['name']}"
                        is_folder = "folder" in item
                        manifest.append(
                            {
                                "name": item["name"],
                                "relative_path": relative_path,
                                "absolute_path": sp_child_path,
                                "size": item.get("size", 0),
                                "is_folder": is_folder,
                            }
                        )

                        # Only descend into subfolders if recursive traversal is enabled
                        if is_folder and recursive:
                            fetch_children(sp_child_path, f"{relative_path}/")

                    next_link = data.get("@odata.nextLink")

            fetch_children(normalized_path)
            return manifest


    def _build_local_manifest(self, local_folder: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Gather metadata for items inside a local folder.

        Parameters:
        - local_folder: Path to the local folder on disk
        - recursive: If True (default), traverse all subfolders recursively.
                     If False, only include the immediate children.

        Returns:
        - List of dictionaries describing files and folders inside the folder
        """
        base_path = Path(local_folder).expanduser().resolve()
        if not base_path.is_dir():
            raise NotADirectoryError(f"Local folder not found: {local_folder}")

        manifest: List[Dict[str, Any]] = []

        if recursive:
            iterator = base_path.rglob("*")
        else:
            iterator = base_path.iterdir()

        for path in iterator:
            try:
                # Skip symlinks to avoid loops and surprises
                if path.is_symlink():
                    print(f"⚠️  Skipping symlink: {path}")
                    continue

                is_folder = path.is_dir()
                size = path.stat().st_size if path.is_file() else 0
            except OSError as e:
                # Handle permission errors, broken links, etc.
                print(f"⚠️  Skipping {path}: {e}")
                continue

            relative_path = path.relative_to(base_path).as_posix()

            manifest.append(
                {
                    "name": path.name,
                    "relative_path": relative_path,
                    "absolute_path": path.as_posix(),
                    "size": size,
                    "is_folder": is_folder,
                }
            )

        return manifest

    def _print_manifest_summary(
        self,
        manifest: List[Dict[str, Any]],
        source_label: str,
        root_label: str
    ) -> None:
        """
        Print details for every entry in a manifest and total size for visibility.

        Parameters:
        - manifest: List of manifest entries
        - source_label: Text describing the source (e.g., "SharePoint" or "Local")
        - root_label: The path of the folder being summarized
        """
        total_bytes = sum(item["size"] for item in manifest if not item["is_folder"])
        pretty_root = root_label or "/"

        print(f"\n{source_label} folder summary ({pretty_root}):")
        if not manifest:
            print(" No files or subfolders found.")
            print(f" Total size: {self._format_bytes(0)}")
            return

        for item in manifest:
            icon = "📁" if item["is_folder"] else "📄"
            size_text = "" if item["is_folder"] else f" ({self._format_bytes(item['size'])})"
            print(f" {icon} {item['relative_path']}{size_text}")

        print(f"Total items: {len(manifest)}")
        print(f"Total size: {self._format_bytes(total_bytes)}")

    def describe_sharepoint_folder(self, sp_folder_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Print a summary of a SharePoint folder and return the manifest.

        Parameters:
        - sp_folder_path: Path to the SharePoint folder relative to the drive root
        - recursive: If True (default), include all subfolders recursively.
                     If False, only list immediate children.

        Returns:
        - Manifest describing items inside the folder
        """
        manifest = self._build_sharepoint_manifest(sp_folder_path, recursive=recursive)
        self._print_manifest_summary(manifest, "SharePoint", sp_folder_path)
        return manifest

    def describe_local_folder(self, local_folder: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Print a summary of a local folder and return the manifest.

        Parameters:
        - local_folder: Path to the local folder on disk
        - recursive: If True (default), include all subfolders recursively.
                     If False, only list immediate children.

        Returns:
        - Manifest describing items inside the folder
        """
        manifest = self._build_local_manifest(local_folder, recursive=recursive)
        self._print_manifest_summary(manifest, "Local", local_folder)
        return manifest

    def ensure_sharepoint_folder(self, folder_path: str) -> None:
        """
        Ensure a SharePoint folder exists by creating missing parent segments.

        Parameters:
        - folder_path: Path to the SharePoint folder relative to the drive root
        """
        self._ensure_authenticated()
        path = folder_path.strip("/")
        if not path:
            return

        base_url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives/{self.drive_id}"
        segments = path.split("/")
        current_path = ""

        for segment in segments:
            current_path = f"{current_path}/{segment}".strip("/")
            folder_url = f"{base_url}/root:/{current_path}"

            try:
                response = requests.get(folder_url, headers=self._headers())
                if response.status_code == 404:
                    parent_path = current_path.rsplit("/", 1)[0]
                    if parent_path:
                        children_url = f"{base_url}/root:/{parent_path}:/children"
                    else:
                        children_url = f"{base_url}/root/children"

                    payload = {
                        "name": segment,
                        "folder": {},
                        "@microsoft.graph.conflictBehavior": "replace",
                    }
                    create_resp = requests.post(children_url, headers=self._headers(), json=payload)
                    create_resp.raise_for_status()
                else:
                    response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise RuntimeError(f"Failed to ensure SharePoint folder '{current_path}': {e}")

    # -------------------------------------------------------
    # FILE OPERATIONS
    # -------------------------------------------------------
    def _format_bytes(self, num_bytes: int) -> str:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if num_bytes < 1024:
                return f"{num_bytes:.2f} {unit}"
            num_bytes /= 1024
        return f"{num_bytes:.2f} PB"


    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in SharePoint.
        
        Parameters:
        - file_path: Path to file in SharePoint (e.g., "folder/file.txt")
            
        Returns:
        - True if file exists, False otherwise
        """
        self._ensure_authenticated()
        file_path = file_path.strip("/")
        
        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives/{self.drive_id}/root:/{file_path}"
        
        try:
            r = requests.get(url, headers=self._headers())
            return r.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def download_file(self, file_path: str, local_path: str, overwrite: bool = False):
        """
        Download a file from SharePoint.

        Behavior:
        - overwrite=False (default): if the local file exists, skip download.
        - overwrite=True: overwrite the existing local file.

        Parameters:
        - file_path: Path to file in SharePoint (relative to drive root)
        - local_path: Local path where file will be saved
        - overwrite: Whether to overwrite existing local file
        """
        self._ensure_authenticated()
        file_path = file_path.strip("/")
        local_path_obj = Path(local_path).expanduser()

        # Safe overwrite behavior
        if local_path_obj.exists():
            if not overwrite:
                print(f"⏭ Skipping download; local file already exists at: {local_path_obj}")
                return
            else:
                print(f"⚠ Overwriting existing local file: {local_path_obj}")

        url = (
            f"https://graph.microsoft.com/v1.0/sites/"
            f"{self.site_id}/drives/{self.drive_id}/root:/{file_path}:/content"
        )

        try:
            r = requests.get(url, headers=self._headers(), stream=True)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if r.status_code == 404:
                raise FileNotFoundError(f"File not found in SharePoint: {file_path}")
            raise RuntimeError(f"Failed to download file: {e}")

        # Ensure local directory exists
        local_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(local_path_obj, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✔ Downloaded {file_path} → {local_path_obj}")
    
    def download_folder(
        self,
        sp_folder_path: str,
        local_folder: str,
        overwrite: bool = False,
        recursive: bool = True,
        dry_run: bool = False,
    ):
        """
        Download files from a SharePoint folder to a local directory.

        Parameters:
        - sp_folder_path: SharePoint source folder path
        - local_folder: Local destination folder
        - overwrite: Whether to overwrite existing local files
        - recursive: If True, include subfolders recursively
        - dry_run: If True, do not download anything—only print what would happen
        """

        manifest = self.describe_sharepoint_folder(sp_folder_path, recursive=recursive)

        files = [x for x in manifest if not x["is_folder"]]
        folders = [x for x in manifest if x["is_folder"]]

        total_files = len(files)
        total_bytes = sum(x["size"] for x in files)

        print("\n========= DOWNLOAD SUMMARY =========")
        print(f"SharePoint source:{sp_folder_path}")
        print(f"Local target:     {local_folder}")
        print(f"Recursive:       {recursive}")
        print(f"Overwrite:       {overwrite}")
        print(f"Dry run:         {dry_run}")
        print(f"Folders:         {len(folders)}")
        print(f"Files:           {total_files}")
        print(f"Total size:      {self._format_bytes(total_bytes)}")
        print("===================================\n")

        if total_files == 0:
            print("Nothing to download.")
            return

        local_root = Path(local_folder).expanduser().resolve()

        if dry_run:
            print("🧪 DRY RUN — no files will be downloaded.\n")
            for item in files:
                print(f"[DRY RUN] Would download: {item['relative_path']} "
                    f"({self._format_bytes(item['size'])})")
            return

        local_root.mkdir(parents=True, exist_ok=True)
        normalized_root = sp_folder_path.strip("/")

        for item in sorted(manifest, key=lambda x: (not x["is_folder"], x["relative_path"])):
            destination = local_root / item["relative_path"]

            if item["is_folder"]:
                destination.mkdir(parents=True, exist_ok=True)
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)
            sp_item_path = "/".join(
                filter(None, [normalized_root, item["relative_path"]])
            ).strip("/")

            self.download_file(
                sp_item_path,
                destination.as_posix(),
                overwrite=overwrite,
            )

    def upload_small_file(self, local_path: str, sp_path: str):
        """
        Upload a small file to SharePoint (< 4MB).
        
        Parameters:
        - local_path: Path to local file
        - sp_path: Destination path in SharePoint
        """
        self._ensure_authenticated()
        sp_path = sp_path.strip("/")

        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")

        file_size = os.path.getsize(local_path)
        if file_size > 4 * 1024 * 1024:
            raise ValueError(
                f"File is {file_size / (1024*1024):.2f} MB. "
                "Use upload_large_file() for files > 4MB"
            )

        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives/{self.drive_id}/root:/{sp_path}:/content"

        with open(local_path, "rb") as f:
            data = f.read()

        try:
            r = requests.put(url, headers=self._headers(), data=data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"Failed to upload file: {e}")

        print(f"✔ Uploaded {local_path} → {sp_path}")

    def upload_large_file(
        self,
        local_path: str,
        sp_path: str,
        chunk_size: int = 5 * 1024 * 1024,
        show_progress: bool = True,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ):
        """
        Upload a large file to SharePoint using chunked upload (> 4MB).
        
        Parameters:
        - local_path: Path to local file
        - sp_path: Destination path in SharePoint
        - chunk_size: Size of each chunk in bytes (default: 5MB)
        - show_progress: Whether to display built-in progress bar (default: True)
        - progress_callback: Optional custom callback function(bytes_uploaded, total_bytes)
        """
        self._ensure_authenticated()
        sp_path = sp_path.strip("/")

        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")

        # Create upload session
        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives/{self.drive_id}/root:/{sp_path}:/createUploadSession"
        
        try:
            r = requests.post(url, headers=self._headers(), json={})
            r.raise_for_status()
            upload_url = r.json()["uploadUrl"]
        except requests.exceptions.HTTPError as e:
            raise RuntimeError(f"Failed to create upload session: {e}")

        file_size = os.path.getsize(local_path)
        print(f"Starting chunked upload: {file_size / (1024*1024):.2f} MB ...")

        with open(local_path, "rb") as f:
            chunk_start = 0

            while chunk_start < file_size:
                chunk = f.read(chunk_size)
                chunk_end = chunk_start + len(chunk) - 1

                headers = {
                    "Content-Length": str(len(chunk)),
                    "Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}"
                }

                try:
                    r = requests.put(upload_url, headers=headers, data=chunk)
                    if r.status_code not in (200, 201, 202):
                        raise RuntimeError(f"Upload chunk failed: {r.text}")
                except requests.exceptions.RequestException as e:
                    raise RuntimeError(f"Error uploading chunk: {e}")

                chunk_start += len(chunk)
                
                # Handle progress display
                if progress_callback:
                    # Custom callback takes precedence
                    progress_callback(chunk_start, file_size)
                elif show_progress:
                    # Built-in progress display
                    progress = (chunk_start / file_size) * 100
                    print(f"Progress: {progress:.1f}%", end="\r")

        if show_progress and not progress_callback:
            print()  # New line after progress bar
        print(f"✔ Uploaded {local_path} → {sp_path}")

    def upload_file(
        self,
        local_path: str,
        sp_path: str,
        show_progress: bool = True,
        progress_callback: Optional[Callable[[int, int], None]] = None,
        overwrite: bool = False,
    ):
        """
        Upload a file to SharePoint (automatically chooses method based on size).
        Uses a chunked upload for large files defined as > 4MB.

        Behavior:
        - overwrite=False (default): if the SharePoint file exists, skip upload.
        - overwrite=True: overwrite the existing SharePoint file.

        Parameters:
        - local_path: Path to local file
        - sp_path: Destination path in SharePoint
        - show_progress: Whether to display built-in progress bar for large files (default: True)
        - progress_callback: Optional custom callback function for printing progress on large files
        - overwrite: Whether to overwrite existing file in SharePoint
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local file not found: {local_path}")

        sp_path = sp_path.strip("/")

        # Safe overwrite behavior
        if self.file_exists(sp_path):
            if not overwrite:
                print(f"⏭ Skipping upload; SharePoint file already exists at: {sp_path}")
                return
            else:
                print(f"⚠ Overwriting existing SharePoint file: {sp_path}")

        file_size = os.path.getsize(local_path)

        if file_size < 4 * 1024 * 1024:
            self.upload_small_file(local_path, sp_path)
        else:
            self.upload_large_file(
                local_path,
                sp_path,
                show_progress=show_progress,
                progress_callback=progress_callback,
            )

    def upload_folder(
        self,
        local_folder: str,
        sp_folder_path: str,
        overwrite: bool = False,
        recursive: bool = True,
        dry_run: bool = False,
    ):
        """
        Upload files from a local directory to SharePoint.

        Parameters:
        - local_folder: Local folder path
        - sp_folder_path: Target SharePoint folder path
        - overwrite: Whether to overwrite existing SharePoint files
        - recursive: If True, include subfolders recursively
        - dry_run: If True, do not upload anything—only print what would happen
        """

        manifest = self.describe_local_folder(local_folder, recursive=recursive)

        files = [x for x in manifest if not x["is_folder"]]
        folders = [x for x in manifest if x["is_folder"]]

        total_files = len(files)
        total_bytes = sum(x["size"] for x in files)

        print("\n========== UPLOAD SUMMARY ==========")
        print(f"Local source:      {local_folder}")
        print(f"SharePoint target:{sp_folder_path}")
        print(f"Recursive:        {recursive}")
        print(f"Overwrite:        {overwrite}")
        print(f"Dry run:          {dry_run}")
        print(f"Folders:          {len(folders)}")
        print(f"Files:            {total_files}")
        print(f"Total size:       {self._format_bytes(total_bytes)}")
        print("===================================\n")

        if total_files == 0:
            print("Nothing to upload.")
            return

        if dry_run:
            print("🧪 DRY RUN — no files will be uploaded.\n")
            for item in files:
                print(f"[DRY RUN] Would upload: {item['relative_path']} "
                    f"({self._format_bytes(item['size'])})")
            return

        normalized_target = sp_folder_path.strip("/")
        self.ensure_sharepoint_folder(normalized_target)
        base_local = Path(local_folder).expanduser().resolve()

        for item in sorted(manifest, key=lambda x: (not x["is_folder"], x["relative_path"])):
            target_path = "/".join(
                filter(None, [normalized_target, item["relative_path"]])
            ).strip("/")

            if item["is_folder"]:
                self.ensure_sharepoint_folder(target_path)
                continue

            local_file = base_local / item["relative_path"]
            self.upload_file(
                local_file.as_posix(),
                target_path,
                overwrite=overwrite,
            )

# -----------------------
# Other external helper functions
# -----------------------

def init_sharepoint_client(
    sharepoint_site: str,
    sp_client: Optional["GraphSharePointClient"],
) -> "GraphSharePointClient":
    """
    Initialize or reuse a GraphSharePointClient.

    Parameters
    - sharepoint_site : str
        Site key for GraphSharePointClient (e.g., 'PROGRAM').
    - sp_client : GraphSharePointClient or None
        If provided, this client is used directly (assumed already authenticated).
        If None, a new GraphSharePointClient is created and authenticated.

    Returns
    - GraphSharePointClient
        An authenticated client instance.

    Raises
    - RuntimeError
        If the client cannot be initialized or authenticated.
    """
    if sp_client is not None:
        print(f"Using provided SharePoint client for site '{sharepoint_site}'.")
        return sp_client

    try:
        client = GraphSharePointClient(sharepoint_site)
        client.authenticate()
        print(f"✓ Authenticated new SharePoint client for site '{sharepoint_site}'.")
        return client
    except Exception as e:
        raise RuntimeError(
            f"Error initializing or authenticating GraphSharePointClient for site '{sharepoint_site}'"
        ) from e

def normalize_sharepoint_path(raw_path: str) -> str:
    """
    Normalize a SharePoint path for use with GraphSharePointClient.

    Behavior:
    - Strips whitespace and leading/trailing slashes.
    - If path starts with 'sites/<siteName>/', strips that prefix.

    Examples
    --------
    >>> normalize_sharepoint_path('/sites/program/Shared Documents/foo/bar.csv')
    'Shared Documents/foo/bar.csv'

    >>> normalize_sharepoint_path('Shared Documents/foo/bar.csv')
    'Shared Documents/foo/bar.csv'
    """
    sp_path = raw_path.strip().strip("/")

    # Strip leading "sites/<site>/" if present
    if sp_path.lower().startswith("sites/"):
        parts = sp_path.split("/", 2)
        if len(parts) == 3:
            sp_path = parts[2]

    return sp_path