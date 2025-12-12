import configparser
import io
import json
import logging
import os
import shutil
import sys
import tempfile
from io import BytesIO
from pathlib import Path
from typing import Callable, List
from typing import IO, Final, Optional, Union, Tuple, Iterator

import msal
import requests
from msal.application import ClientApplication
from msal_extensions import build_encrypted_persistence, FilePersistence, PersistedTokenCache
from office365.graph_client import GraphClient
from office365.onedrive.driveitems.conflict_behavior import ConflictBehavior
from office365.onedrive.driveitems.driveItem import DriveItem
from office365.onedrive.driveitems.uploadable_properties import DriveItemUploadableProperties
from office365.onedrive.files.system_info import FileSystemInfo
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.upload_session import UploadSessionQuery
from typing_extensions import override

_GRAPH_CLIENT: GraphClient
_SHAREPOINT_HOST: str


def init_spio(cfg: dict):
    """
    Initialize Microsoft Graph API using provided configuration settings.

    Call this method at the beginning of your application to set up the Microsoft Graph API connection.


    Parameters:
    - `cfg` (dict): Configuration dictionary containing settings for Graph API.

    The `cfg` dictionary can include the following keys (with examples):
    - 'graph_url': Microsoft Graph API endpoint (default: 'https://graph.microsoft.com/')           # Optional
    - 'sharepoint_host': SharePoint host URL (default: 'vitoresearch.sharepoint.com')               # Optional
    - 'user_account': Microsoft Graph username (e.g., 'john.smith@vito.be')                         # Required

    Additionally, the 'msal' key can include the following subkeys for MSAL (Microsoft Authentication Library) settings:
    - 'client_id': MSAL client ID                                                                   # Optional
    - 'authority': MSAL authority URL                                                               # Optional
    - 'auth_method': Authentication method ('device' or 'interactive', default: 'device')           # Optional
    - 'scopes': List of MSAL scopes (default: ["Files.ReadWrite", "User.Read"])                     # Optional, see:  https://learn.microsoft.com/en-us/graph/permissions-reference
    - 'token_cache': Path to the token cache file (default: "{USER_HOME}/msal_token_cache.bin")     # Optional


    All the configurable settings (except 'user_account') have default values in marvin.sherepoint.default_config.ini.

    In most cases you will only have to provide your Microsoft Graph username:
    ```python
    init_spio({"user_account": "john.smith@vito.be"})
    ```

    Or if you work with Python config object:

    ```python
    from config import settings
    init_spio(config)   # config should contain a value for "user_account"
    ```
    """
    # add the default settings if there are missing settings in 'cfg'
    dflt_cfg = _default_settings()

    def _get(key):
        return cfg.get(key, dflt_cfg[key])

    user_account = _get('user_account')
    sharepoint_host = _get('sharepoint_host')
    graph_url = _get('graph_url')
    msal_cfg = dflt_cfg.get('msal', {})
    msal_cfg.update(cfg.get('msal', {}))

    global _GRAPH_CLIENT, _SHAREPOINT_HOST
    _GRAPH_CLIENT = _create_graph_client(user_account, graph_url, msal_cfg)
    _SHAREPOINT_HOST = sharepoint_host


def copy_file(remote_file_source: DriveItem, remote_folder_destination: DriveItem) -> ClientResult:
    """
        Copy a file from one location to another in the Microsoft Cloud.

        Parameters:
        - `remote_file_source` (DriveItem): Source file to be copied.
        - `remote_folder_destination` (DriveItem): Destination folder.

        Returns:
        - `ClientResult`: Result of the copy operation.

        Raises:
        - `Exception`: If source is not a file or destination is not a folder.

        Example Usage:
        ```python
        from marvin.sharepoint.mr_sharepoint import *

        result = copy_file(find_item_in_my_onedrive('/path/to/file.txt'), find_item_in_my_onedrive('/path/to/destination/folder'))
        ```
        """
    if not remote_file_source.is_file:
        raise Exception(f"'{remote_file_source}' is not a file.")
    if not remote_folder_destination.is_folder:
        raise Exception(f"'{remote_folder_destination}' is not a folder.")

    destination_reference = {'id': remote_folder_destination.id}
    # return remote_file_source.copy(parent=remote_folder_destination, conflict_behavior=ConflictBehavior.Rename).execute_query()
    return remote_file_source.copy(name=remote_file_source.name, parent=destination_reference, conflict_behavior=ConflictBehavior.Replace).execute_query()

def assert_file_exists(folder: DriveItem, file_name: str) -> DriveItem:
    """
    Assert that a file exists in a specified folder in the Microsoft Cloud.

    Returns:
    - `DriveItem`: The existing or created file.
    """
    try:
        drive_item = find_item_by_rel_path(folder, file_name)
        if drive_item is not None:
            if drive_item.is_file:
                return drive_item
            else:
                raise Exception(f"'{drive_item}' is a folder.")
    except:
        # ignore exception
        ...
    create_file(folder, file_name, b'')
    return find_item_by_rel_path(folder, file_name)


def create_file(folder: DriveItem, file_name: str, content):
    """
    Create a new file in a specified folder in the Microsoft Cloud.

    Parameters:
    - `folder` (DriveItem): Destination folder.
    - `file_name` (str): Name of the new file.
    - `content`: (Binary )Content to be written to the file.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    create_file(find_item_in_my_onedrive('/path/to/folder'), "new_file.txt", "Hello, World!")
    ```
    """
    logging.debug(f"create file: {file_name} in folder: {folder.web_url}")

    # create local tempfile and upload it to the folder
    with tempfile.TemporaryDirectory() as tmp_dir:
        try:
            tmp_file = Path(tmp_dir) / file_name
            with open(tmp_file, 'wb') as f:
                f.write(content)
            upload_file_silent(tmp_file, folder)
        finally:
            shutil.rmtree(tmp_dir)

    print("file created: " + file_name)


def clear_folder(drive_item: DriveItem):
    """
    Clear a folder in the Microsoft Cloud.

    Parameters:
    - `drive_item` (DriveItem): The folder to be cleared.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    clear_folder(find_item_in_my_onedrive('/path/to/folder'))
    ```
    """
    logging.debug(f"delete folder: {drive_item.web_url}")
    if drive_item.is_folder:
        children = drive_item.children.get().execute_query()
        for child in children:
            child_clone = find_item_by_url(child.web_url)  # FIXME: This is a workaround, in some cases 'download_folder(child)' and  'child.download(local_file)' throw an error: office365.runtime.client_request_exception.ClientRequestException: ('invalidRequest', 'Invalid request', '400 Client Error: Bad Request for url: https://graph.microsoft.com/v1.0/shares/u!aH...hZA=/driveItem/01TPTZXJTBYIK5VLBPPFHYQGIOXWHHOCQC/children')
            child_clone.delete_object().execute_query()
    else:
        raise Exception(f"'{drive_item}' is not a folder.")


def delete_folder(drive_item: DriveItem):
    """
    Delete a folder from the Microsoft Cloud.

    Parameters:
    - `drive_item` (DriveItem): The folder to be deleted.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    delete_folder(find_item_in_my_onedrive('/path/to/folder'))
    ```
    """
    logging.debug(f"delete folder: {drive_item.web_url}")
    if drive_item.is_folder:
        resp = drive_item.delete_object().execute_query()
    else:
        raise Exception(f"'{drive_item}' is not a folder.")


def delete_file(drive_item: DriveItem):
    """
    Delete a file from the Microsoft Cloud.

    Parameters:
    - `drive_item` (DriveItem): The file to be deleted.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    delete_file(find_item_in_my_onedrive('/path/to/file'))
    ```
    """
    logging.debug(f"delete file: {drive_item.web_url}")
    if drive_item.is_file:
        resp = drive_item.delete_object().execute_query()
    else:
        raise Exception(f"'{drive_item}' is not a file.")

def create_text_file(folder: DriveItem, file_name: str, content: str, encoding='utf-8'):
    """
    Create a new text file in a specified folder in the Microsoft Cloud.

    Parameters:
    - `folder` (DriveItem): Destination folder.
    - `file_name` (str): Name of the new file.
    - `content` (str): Text content to be written to the file.
    - `encoding` (str): Encoding for the text content (default: 'utf-8').

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    create_text_file(find_item_in_my_onedrive('/path/to/folder'), "new_text_file.txt", "Hello, World!")
    ```
    """
    create_file(folder, file_name, bytes(content, encoding=encoding))


def create_folder(name_folder: str, remote_parent_folder: DriveItem) -> DriveItem:
    """
    Create a new folder in a specified parent folder in the Microsoft Cloud.

    Parameters:
    - `name_folder` (str): Name of the new folder.
    - `remote_parent_folder` (DriveItem): Parent folder.

    Returns:
    - `DriveItem`: Newly created folder.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    # create a new folder "NewFolder" in root of you OneDrive.
    new_folder = create_folder("NewFolder", find_item_in_my_onedrive('/'))
    ```
    """
    return remote_parent_folder.create_folder(name_folder, conflict_behavior=ConflictBehavior.Replace).execute_query()


def download_file_silent(remote_file: DriveItem, local_folder, chunk_size=1024 * 1024) -> Path:
    """
    Download a file from Microsoft Cloud to a local folder silently (without progress call back).

    Parameters:
    - `remote_file` (DriveItem): Source file to be downloaded.
    - `local_folder` (str): Local folder to save the downloaded file.
    - `chunk_size` (int): Size of each download chunk in bytes (default: 1 MB).

    Returns:
    - `Path`: Local path of the downloaded file.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    local_path = download_file_silent(find_item_in_my_onedrive('/path/to/one_drive/file.xlsx'), '/your/local/folder')
    ```
    """
    def _empty_call_back(arg):
        pass
    return download_file(remote_file, local_folder, chunk_size=chunk_size, progress_call_back=_empty_call_back)


def download_file(remote_file: DriveItem, local_folder, chunk_size=1024 * 1024,  progress_call_back: Callable = None) -> Path:
    """
    Download a file from Microsoft Cloud to a local folder with the option to track the download progress.

    Parameters:
    - `remote_file` (DriveItem): Source file to be downloaded.
    - `local_folder` (str): Local folder to save the downloaded file.
    - `chunk_size` (int): Size of each download chunk in bytes (default: 1 MB).
    - `progress_callback` (Callable): Callback function to track download progress.  (default: A logging.info() call back)

    Returns:
    - `Path`: Local path of the downloaded file.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    local_path = download_file_silent(find_item_in_my_onedrive('/path/to/one_drive/file.xlsx'), '/your/local/folder')
    ```
    """
    path_local_folder = _to_path(local_folder)
    if not path_local_folder.exists():
        raise Exception(f"local_folder {local_folder} does not exist.")
    if not path_local_folder.is_dir():
        raise Exception(f"local_folder {local_folder} is not a folder.")

    file_name = remote_file.name
    file_size = remote_file.properties.get('size', None)

    def _print_progress(x):
        if file_size is None:
            logging.info(f"{x} bytes of file '{file_name}' is downloaded to '{local_folder}'")
        else:
            logging.info(f"{((100.0 * x) / file_size):.1f}% of file '{file_name}' is downloaded to '{local_folder}'")

    chunk_downloaded_callback = progress_call_back if progress_call_back is not None else _print_progress

    local_path = Path(local_folder, file_name)
    with open(local_path, "wb") as local_file:
        remote_file.download_session(
            local_file, chunk_downloaded_callback, chunk_size=chunk_size
        ).execute_query()
    return local_path


def download_folder(remote_parent_folder: DriveItem, local_folder, chunk_size=1024 * 1024) -> Path:
    """
    Download the contents of a remote folder in the Microsoft Cloud to a local folder.
    """

    # Convert local_folder to a Path object if it's not already
    local_folder = Path(local_folder) if not isinstance(local_folder, Path) else local_folder

    # Create the local folder if it doesn't exist
    local_folder.mkdir(parents=True, exist_ok=True)

    # Get the children (files and folders) of the remote parent folder
    children = remote_parent_folder.children.get().execute_query()

    for child in children:
        # Construct the local path for this child
        local_child_path = local_folder / child.name
        child_clone = find_item_by_url(child.web_url)  # FIXME: This is a workaround, in some cases 'download_folder(child)' and  'child.download(local_file)' throw an error: office365.runtime.client_request_exception.ClientRequestException: ('invalidRequest', 'Invalid request', '400 Client Error: Bad Request for url: https://graph.microsoft.com/v1.0/shares/u!aH...hZA=/driveItem/01TPTZXJTBYIK5VLBPPFHYQGIOXWHHOCQC/children')

        if child_clone.is_folder:
            # If the child is a folder, recursively download it

            download_folder(child_clone, local_child_path, chunk_size)
        else:
            # If the child is a file, download it
            with open(local_child_path, "wb") as local_file:
                child_clone.download(local_file).execute_query()

    return local_folder

def upload_file_silent(local_file, remote_folder: DriveItem, chunk_size=1024 * 1024) -> DriveItem:
    """
    Upload a file to the Microsoft Cloud silently (without progress call back).

    Parameters:
    - `local_file`: Local file to be uploaded.
    - `remote_folder` (DriveItem): Destination folder on OneDrive.
    - `chunk_size` (int): Size of each upload chunk in bytes (default: 1 MB).

    Returns:
    - `DriveItem`: Location of the upload file in the Cloud.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *
    from pathlib import Path

    upload_result = upload_file_silent(Path('rel/to/local_file.txt'), find_item_by_url('https://vitoresearch.sharepoint.com/:w:/r/sites/unit-rma/Shared%20Documents/RMA-IT/Temporary/'))
    ```
    """
    def _empty_call_back(arg):
        pass
    return upload_file(local_file, remote_folder, chunk_size=chunk_size, progress_call_back=_empty_call_back)


def upload_file(local_file, remote_folder: DriveItem, chunk_size=1024 * 1024, progress_call_back: Callable = None) -> DriveItem:
    """
    Upload a file to the Microsoft Cloud (with progress call back).

    Parameters:
    - `local_file`: Local file to be uploaded.
    - `remote_folder` (DriveItem): Destination folder on OneDrive.
    - `chunk_size` (int): Size of each upload chunk in bytes (default: 1 MB).
    - `progress_callback` (Callable): Callback function to track the upload progress. (default: A logging.info() call back)

    Returns:
    - `DriveItem`: Location of the upload file in the Cloud.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *
    from pathlib import Path

    upload_result = upload_file(Path('rel/to/local_file.txt'), find_item_by_url('https://vitoresearch.sharepoint.com/:w:/r/sites/unit-rma/Shared%20Documents/RMA-IT/Temporary/'))
    ```
    """
    logging.debug(f"upload_file()  local_file: {local_file} remote_folder: {remote_folder.web_url}")
    path_local_file = _to_path(local_file)
    if not path_local_file.exists():
        raise Exception(f"local_file {local_file} does not exist.")
    if not path_local_file.is_file():
        raise Exception(f"local_file {local_file} is not a file.")

    file_name = path_local_file.name
    file_size = path_local_file.stat().st_size
    chunk_uploaded_callback = progress_call_back if progress_call_back is not None \
        else lambda x: logging.info(f"{((100.0 * x) / file_size):.1f}% of file '{file_name}' is uploaded to '{remote_folder.resource_path}'")

    remote_file = (
        remote_folder.resumable_upload(
            str(path_local_file), chunk_size=chunk_size, chunk_uploaded=chunk_uploaded_callback
        )
        .get()
        .execute_query()
    )
    return remote_file


def upload_folder(local_folder, remote_parent_folder: DriveItem):
    """
    Upload the contents of a local folder to a remote folder in the Microsoft Cloud.

    Parameters:
    - `local_folder`: Local folder to be uploaded.
    - `remote_parent_folder` (DriveItem): Destination parent folder in the Microsoft Cloud.

    Raises:
    - `Exception`: If local_folder does not exist or is not a folder.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *
    from pathlib import Path

    upload_folder(Path('/to/local/folder'), find_item_in_my_onedrive('/path/to/destination/folder'))
    ```
    """
    path_local_folder = _to_path(local_folder)

    if not path_local_folder.exists():
        raise Exception(f"local_folder {local_folder} does not exist.")
    if not path_local_folder.is_dir():
        raise Exception(f"local_folder {local_folder} is not a folder.")

    remote_folder = create_folder(path_local_folder.name, remote_parent_folder)

    for path in path_local_folder.iterdir():
        if path.is_file():
            upload_file(path, remote_folder)
        elif path.is_dir():
            upload_folder(path, remote_folder)


def find_item_by_url(shared_url: str, graph_client: GraphClient = None) -> DriveItem:
    """
    Retrieve a DriveItem in the Microsoft Cloud using a shared URL.

    Parameters:
    - `shared_url` (str): The shared URL of the file on OneDrive.
    - `graph_client` (GraphClient, optional): The GraphClient instance. Defaults to None.  In this case the default GraphClient that was created during the init_graph() call will be used.

    Returns:
    - `DriveItem`: The DriveItem corresponding to the shared URL.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *
      
    item = find_item_by_url("https://example.sharepoint.com/:x:/r/sites/site_name/file_path")
    ```
    """
    return _get_client(graph_client).shares.by_url(shared_url).drive_item.get().execute_query()


def find_item_in_site(name_site: str, rel_path: str, sharepoint_host: str = None, graph_client: GraphClient = None) -> DriveItem:
    """
    Retrieve a DriveItem within a SharePoint site.

    Parameters:
    - `name_site` (str): The name of the SharePoint site.
    - `rel_path` (str): The relative path of the file within the site.
    - `sharepoint_host` (str, optional): The SharePoint host URL (default: None). In this case the 'sharepoint_host' that was configured during the init_graph() call will be used.
    - `graph_client` (GraphClient, optional): The GraphClient instance. Defaults to None.  In this case the default GraphClient that was created during the init_graph() call will be used.

    Returns:
    - `DriveItem`: The DriveItem corresponding to the specified site and path.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    item = find_item_in_site('unit-rma', 'RMA-IT/Temporary/mr_sharepoint')
    ```
    """
    host = sharepoint_host if sharepoint_host is not None else _SHAREPOINT_HOST
    site_url = f'{host}:/sites/{name_site}:'
    site = _get_client(graph_client).sites[site_url].get().execute_query()
    site_root = _get_client(graph_client).sites[site.id].drive.root
    return find_item_by_rel_path(site_root, rel_path)


def find_item_in_my_onedrive(rel_path: str, graph_client: GraphClient = None) -> DriveItem:
    """
    Retrieve a DriveItem within the user's OneDrive using its relative path.

    Parameters:
    - `rel_path` (str): The relative path of the file within the OneDrive.
    - `graph_client` (GraphClient, optional): The GraphClient instance. Defaults to None.  In this case the default GraphClient that was created during the init_graph() call will be used.

    Returns:
    - `DriveItem`: The DriveItem corresponding to the specified relative path.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    item = find_item_in_my_onedrive('/path/to/file.txt')
    ```

    """
    onedrive_root = _get_client(graph_client).me.drive.root
    return find_item_by_rel_path(onedrive_root, rel_path)


def find_item_by_rel_path(root: DriveItem, rel_path: str) -> DriveItem:
    """
    Retrieve a DriveItem based on its relative path from another specified root DriveItem.

    Parameters:
    - `root` (DriveItem): The root DriveItem to start the search.
    - `rel_path` (str): The relative path of the file within the root.

    Returns:
    - `DriveItem`: The DriveItem corresponding to the specified relative path.

    Example Usage:
    ```python
    from marvin.sharepoint.mr_sharepoint import *

    root = find_item_in_my_onedrive('/path')
    item = find_item_by_rel_path(root, 'to/file.txt')
    ```
    """
    return root.get_by_path(rel_path).get().execute_query()


def _get_client(graph_client: GraphClient) -> GraphClient:
    return graph_client if graph_client is not None else _GRAPH_CLIENT


def _to_path(path) -> Path:
    if isinstance(path, Path):
        return path
    return Path(path)


def _create_graph_client(account: str, graph_url: str, cfg_msal: dict) -> GraphClient:
    """
    :param account: The SharePoint username (name.familyname@vito.be)
    :param cfg_msal: should contain  'client_id', 'authority'
    optional: 'token_cache', 'auth_method', 'scopes'
    :return: A GraphClient instance
    """
    client_id = cfg_msal['client_id']
    authority = cfg_msal['authority']

    token_cache = cfg_msal.get('token_cache', Path(Path.home(), 'msal_token_cache.bin'))
    auth_method = cfg_msal.get('auth_method', 'device')  # 'interactive' or 'device'

    scopes = cfg_msal.get('scopes', None)
    if scopes is None:
        scopes = [graph_url + permission for permission in ('Sites.Read.All', 'User.Read', 'AllSites.Read', 'MyFiles.Read', 'MyFiles.Write')]

    app: ClientApplication = msal.PublicClientApplication(client_id=client_id, authority=authority, token_cache=_get_token_cache(token_cache))
    client = GraphClient(lambda: _get_token(app, account, auth_method, scopes))
    return client


def _get_token(app, account, method, scopes):
    cached_accounts = app.get_accounts()
    token = None
    if cached_accounts:
        logging.debug('Try using token from cache')
        token = app.acquire_token_silent(account=cached_accounts[0], scopes=scopes)
    if token is None:  # either no cached account, or token refresh failed
        if method == 'interactive':
            token = app.acquire_token_interactive(scopes=scopes, login_hint=account)
        else:
            flow = app.initiate_device_flow(scopes=scopes)
            if 'user_code' not in flow:
                raise ValueError(f'Failed to create device flow.  Err: {json.dumps(flow, indent=4)}')
            print(flow['message'])
            sys.stdout.flush()
            input('Press enter after signing in from other device/browser to proceed, CTRL+C to abort.')
            token = app.acquire_token_by_device_flow(flow)
        logging.debug('Acquired new token: %s', token)
    return token


def _get_token_cache(location):
    persistence = _build_persistence(location)
    logging.debug('Type of persistence: %s\nPersistence encrypted? %s',
                 persistence.__class__.__name__, persistence.is_encrypted)
    return PersistedTokenCache(persistence)

def _build_persistence(location, fallback_to_plaintext=False):
    """Build a suitable persistence instance based your current OS"""
    # Note: This sample stores both encrypted persistence and plaintext persistence
    # into same location, therefore their data would likely override with each other.
    try:
        return build_encrypted_persistence(location)
    except:  # pylint: disable=bare-except
        # On Linux, encryption exception will be raised during initialization.
        # On Windows and macOS, they won't be detected here,
        # but will be raised during their load() or save().
        if not fallback_to_plaintext:
            raise
        logging.warning("Encryption unavailable. Opting in to plain text.")
        return FilePersistence(location)


def _recursive_merge(dct1, dct2):
    merged = dct1.copy()
    for key, value in dct2.items():
        if key in merged:
            if value is None or isinstance(value, (bool, float, int, str)):
                # Use value from dct2 for scalar types
                merged[key] = value
            elif isinstance(value, list):
                # Merge lists without duplicates
                merged[key] = list(set(merged[key] + value))
            else:
                # Recursive merge for nested dictionaries
                merged[key] = _recursive_merge(merged[key], value)
        else:
            # Key not in dct1, add it to the merged dictionary
            merged[key] = value
    return merged


def _default_settings() -> dict:
    return _read_ini(Path(Path(__file__).parent, 'default_config.ini'))


def _read_ini(ini_file, default_section='default') -> dict:
    config_dict = {}
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(ini_file)
    for section in config.sections():
        config_dict[section] = {}
        for option in config.options(section):
            val = config.get(section, option).strip()
            if _is_json_list(val):
                config_dict[section][option] = _convert_to_list(val)
            else:
                config_dict[section][option] = val

    dflt_dict = config_dict.get(default_section, None)
    if isinstance(dflt_dict, dict):
        for key, val in dflt_dict.items():
            if key not in config_dict:
                config_dict[key] = val
            else:
                raise Exception(f'Key {key} in default section is not unique.')
        del config_dict[default_section]
    return config_dict

def _is_json_list(input_string):
    try:
        json_list = json.loads(input_string)
        return isinstance(json_list, list)
    except json.JSONDecodeError:
        return False

def _convert_to_list(input_string):
    try:
        return json.loads(input_string)
    except json.JSONDecodeError:
        raise ValueError("Input string is not a valid JSON")



class _DriveItemWrapper:

    def __init__(self, _drive_item: DriveItem):
        self.drive_item = _drive_item

    def file_size(self) -> int:
        return self.drive_item.properties.get('size', None)

    def download_range(self, io_object: IO, start: int, end: int, chunk_size=1024 * 1024):
        """
        Download a specific byte range from start to end.

        :type io_object: typing.IO
        :param int start: The start byte.
        :param int end: The end byte.
        :param int chunk_size: The number of bytes it should read into memory.
        """
        # print("download_range() start: ", start, " end: ", end)

        def _construct_request(request):
            # type: (RequestOptions) -> None
            request.stream = True
            request.headers['Range'] = f'bytes={start}-{end}'

        def _process_response(response):
            # type: (requests.Response) -> None
            bytes_read = 0
            for chunk in response.iter_content(chunk_size=chunk_size):
                bytes_read += len(chunk)
                io_object.write(chunk)

        self.drive_item.get_content().before_execute(_construct_request)
        self.drive_item.context.after_execute(_process_response)
        return self

    def upload_range(self, io_object: IO, start: int, end: int, chunk_size=1024 * 1024):
        """
        TODO: Fix me
        Upload a specific byte range from start to end.

        :type io_object: typing.IO
        :param int start: The start byte.
        :param int end: The end byte.
        :param int chunk_size: The number of bytes it should read into memory.
        """

        def _create_request(request):
            request.url += "?@microsoft.graph.conflictBehavior={0}".format('replace')

        def create_upload_session(item):
            qry = UploadSessionQuery(self.drive_item, {"item": item})
            self.drive_item.context.add_query(qry)
                # .before_query_execute(_create_request)
            return qry.return_type

        fsi = FileSystemInfo()
        props = DriveItemUploadableProperties(fsi, name="your_filename.ext")

        props = DriveItemUploadableProperties()

        upload_session = create_upload_session(props).execute_query()

        def upload_chunk(upload_url, byte_range, data):
            headers = {
                # 'Content-Disposition': f'attachment; filename=""your_filename.ext"',
                'Content-Length': str(len(data)),
                'Content-Range': f'bytes {byte_range[0]}-{byte_range[1]}/{self.file_size()}'
            }
            response = requests.put(upload_url, headers=headers, data=data)
            response.raise_for_status()

        # Read and upload the byte range
        io_object.seek(start)
        while start <= end:
            bytes_to_read = min(chunk_size, end - start + 1)
            chunk = io_object.read(bytes_to_read)
            if not chunk:
                break

            upload_chunk(upload_session.value.uploadUrl, (start, start + len(chunk) - 1), chunk)
            start += len(chunk)
        # Finish the upload session
        upload_session.finish_upload(start, end).execute_query()
        return self


class Location:
    """
    Represents the location of a SPIO path.

    Attributes:
        MY_DRIVE (str): The path refers to a location in your OneDrive.
        SHARED (str): The path is a shared link.

    Examples:
        ```python
        # To use the path for your OneDrive:
        spio = SPIO('/path/to/SampleData.csv', Location.MY_DRIVE)

        # To use a shared link path:
        spio = SPIO('https://vitoresearch.sharepoint.com/:x:/r/sites/unit-rma/Shared%20Documents/RMA-IT/Temporary/mr_sharepoint/SampleData/SampleData.xlsx', Location.SHARED)
          # or (because SHARED is the default location)
        spio = SPIO('https://vitoresearch.sharepoint.com/:x:/r/sites/unit-rma/Shared%20Documents/RMA-IT/Temporary/mr_sharepoint/SampleData/SampleData.xlsx')
        ```
    """

    def __init__(self):
        pass

    SHARED = "#shared_url#"
    MY_DRIVE = "#my_drive#"


class SPIO(io.IOBase):
    """
        A class that wraps a SharePoint URL into a BytesIO object.

        Args:
            path (str): The SharePoint URL.
            location (str, optional): The location of the path (MY_DRIVE or SHARED). Defaults to Location.SHARED.
            gc (GraphClient, optional): The GraphClient instance. Defaults to None.  In this case the default GraphClient that was created during the init_graph() call will be used.

        Examples:
        ```python
            # Create an SPIO object for a shared link
            spio = SPIO('https://vitoresearch.sharepoint.com/:x:/r/sites/unit-rma/Shared%20Documents/RMA-IT/Temporary/mr_sharepoint/SampleData/SampleData.xlsx')

            # Create an SPIO object for a OneDrive location
            spio = SPIO('/path/to/SampleData.csv', Location.MY_DRIVE)

            # writing to a SPIO object
            with SPIO('path/to/hi.txt', Location.MY_DRIVE) as file:
                file.write_line('Hello, SPIO!\n')
                file.write_line('This is a sample text.')

            # with pandas, you can directly read from SPIO object into pd.DataFrame
            df = pd.read_csv(SPIO('https://vitoresearch.sharepoint.com/:x:/r/sites/unit-rma/Shared%20Documents/RMA-IT/Temporary/mr_sharepoint/SampleData/SampleData.csv'), sep=';')

            # and write a pd.DataFrame to a SPIO object
            df.to_excel(SPIO('/path/to/SampleData.xlsx', Location.MY_DRIVE))
        ```
    """

    _NO_DRIVE_ITEM: Final = object()

    DEFAULT_CHUNK_SIZE: Final = 8 * 1024 * 1024

    def __init__(self, path, location: str = Location.SHARED, read_chunks=-1, mem_buffered=True, writable=True, write_on_flush=True, gc: GraphClient = None):
        """
        Initialize the SPIO object.

        """
        super().__init__()
        if mem_buffered:
            self._io_delegate = BytesIO()
        else:
            self._io_delegate = tempfile.NamedTemporaryFile(delete=True, prefix="SPIO_", suffix=".bin")

        self.graph_client = gc if gc is not None else _GRAPH_CLIENT
        if self.graph_client is None:
            raise Exception("GRAPH_CLIENT is None. Use init_graph() first.")
        self.path = path
        self.location = location
        self.read_chunks = read_chunks
        self._writable = writable
        self._download_complete = False
        self._downloaded_until = 0
        self._read_until = 0
        self._drive_item = None
        self._closed = False
        self._written = False
        self._delegate_exposed = False
        self._flushed = 0
        self._write_on_flush = write_on_flush
        self._checked_writable = None
        self._temp_copies: List[Path] = []

    @property
    def web_url(self):
        drive_item = self.get_drive_item()
        return drive_item.web_url if drive_item is not None else None

    @property
    def name(self):
        drive_item = self.get_drive_item()
        return drive_item.name if drive_item is not None else None

    def copy_file(self, assert_fully_downloaded=True) -> Path:
        """
        Returns the path to a local temporary copy the file.
        """
        temp_dir = Path(tempfile.mkdtemp(prefix="SPIO_"))
        try:
            temp_file = Path(temp_dir, self.get_drive_item().name)
            with open(temp_file, 'wb') as open_file:
                shutil.copyfileobj(self.copy_bytes_io(assert_fully_downloaded), open_file)
        finally:
            self._temp_copies.append(temp_dir)
        return temp_file

    def copy_text(self, assert_fully_downloaded=True, encoding='utf-8') -> str:
        """
        Returns: A copy of the underlying io buffer to a new string
        """
        return self.copy_bytes(assert_fully_downloaded).decode(encoding)

    def copy_bytes(self, assert_fully_downloaded=True) -> bytes:
        """
        Returns: A aopy of the underlying  io buffer to a new BytesIO object.
        """
        if assert_fully_downloaded:
            self._assert_fully_downloaded()
        tell = self._io_delegate.tell()
        self._io_delegate.seek(0)
        data = self._io_delegate.read()
        self._io_delegate.seek(tell)
        return data

    def copy_bytes_io(self, assert_fully_downloaded=True) -> io.BytesIO:
        """
        Returns: A aopy of the underlying io buffer to a new BytesIO object.
        """
        return BytesIO(self.copy_bytes(assert_fully_downloaded))

    def io_delegate(self):
        if not self._delegate_exposed:
            self._delegate_exposed = True
            self._hook_io_delegate()
        return self._io_delegate

    def write_to(self, dest) -> str:
        """
        Write the content of the SPIO object to a file.

        Args:
            dest: Destination

        Returns:
            str: The file path.
        """
        tell = self._io_delegate.tell()
        self._io_delegate.seek(0)
        # dest_name = None
        try:
            if hasattr(dest, 'write') and hasattr(dest, 'name'):
                # shutil.copyfileobj(self._io_delegate, dest)
                dest.write(self.read())
                dest_name = dest.name
                # dest.close()
            else:
                path = dest if isinstance(dest, Path) else Path(dest)
                with open(path, 'wb') as f:
                    f.write(self.read())
                dest_name = str(path)
        finally:
            self._io_delegate.seek(tell)
        return dest_name

    @property
    def chunk_size(self):
        return self.read_chunks if self.read_chunks > 0 else 8 * 1024 * 1024

    @property
    def chunked_read(self):
        return self.read_chunks > 0

    @override
    def seek(self, *args) -> int:
        # print(f"seek: {args}")
        if len(args) == 2 and args[1] == io.SEEK_END:
            self._assert_fully_downloaded()
        return self._io_delegate.seek(*args)

    @override
    def read(self, *args) -> bytes:
        # print(f"read: {args}")
        if len(args) == 1:
            size = args[0]
            if size is None:
                self._read_until = self.get_drive_item().properties.get('size', None)
            else:
                self._read_until += size

            if not self.chunked_read and self._downloaded_until == 0:  # download the full file from the start
                self._assert_fully_downloaded()
            else:
                self._assert_downloaded(until=self._read_until)   # download the full file piece by piece
            data = self._io_delegate.read(size)
            return data
        else:
            self._assert_fully_downloaded()
            return self._io_delegate.read(*args)


    @override
    def readline(self, __size: Optional[int] = -1) -> bytes:
        # Check if the size parameter is provided
        size = __size if __size is not None else -1
        line = bytearray()

        # Keep reading until a newline character or size limit is reached
        while size != 0:
            char = self.read(1)
            if not char:
                break
            line.extend(char)
            if char == b'\n':
                if line.endswith(b'\r\n') or line.endswith(b'\n'):
                    break
            elif char == b'\r':
                if size != 0:
                    next_char = self.read(1)
                    if next_char == b'\n':
                        line.extend(next_char)
                    else:
                        self.seek(-1, io.SEEK_CUR)  # Move the cursor back
                break
            size -= 1
        return bytes(line)

    @override
    def readlines(self, __hint: Optional[int] = None) -> list[bytes]:
        lines = []
        total_size = 0
        size_hint = __hint if __hint is not None else -1

        while size_hint < 0 or total_size < size_hint:
            line = self.readline()
            if not line:
                break
            lines.append(line)
            total_size += len(line)

        return lines

    @override
    def close(self) -> None:
        if not self.closed:
            logging.debug("close()")
            self._closed = True
            if self._written:
                self._write_to_sharepoint()
            self._io_delegate.close()
            del self._io_delegate
            for tmpdir in self._temp_copies:
                try:
                    logging.debug(f"unlinking {tmpdir}")
                    shutil.rmtree(tmpdir)
                except Exception as e:
                    logging.error(f"Error deleting temp dir {tmpdir}: {e}")

    @override
    def flush(self, flush_delegate=True) -> None:
        logging.debug(f"flush()")
        # TODO: only upload the data that was not written since the last flush... Fix _DriveItemWrapper.upload_range()
        if flush_delegate:
            self._io_delegate.flush()
        if self._written:
            self._write_to_sharepoint()

    def _write_to_sharepoint(self):
        drive_item_parent, file_name = self._try_create_parent_drive_item()
        # tell = self._io_delegate.tell()
        buffer_size = self._io_delegate.seek(0, 2)
        if self._flushed != buffer_size:
            data = self.copy_bytes(assert_fully_downloaded=False)
            logging.info(f"write file to sharepoint()")
            create_file(drive_item_parent, file_name, data)
            self._drive_item_might_be_created()
            self._flushed = buffer_size

    @property
    @override
    def closed(self) -> bool:
        return self._closed

    @override
    def readable(self) -> bool:
        drive_item = self.get_drive_item()
        if drive_item is None:
            return False
        return True

    @override
    def write(self, *args) -> int:
        logging.debug(f"write: {len(args)}")
        self._raise_if_not_writble()
        self._written = True
        if len(args) == 1:
            arg = args[0]
            if not isinstance(arg, bytes):
                arg = bytes(str(arg), encoding='utf-8')
            wrote = self._io_delegate.write(arg)
            logging.debug(f"write: {wrote}")
            return wrote
        return 0

    @override
    def writelines(self, *args) -> None:
        self._raise_if_not_writble()
        self._io_delegate.writelines(*args)
        self._written = True

    def write_line(self, line: str, encoding='utf-8', linesep=None) -> None:
        if linesep is None:
            linesep = os.linesep
        if not line.endswith(linesep):
            # If not, append it
            line += linesep
        self.write(bytes(line, encoding=encoding))

    def write_lines(self, lines: list[str], encoding='utf-8', linesep=None) -> None:
        for line in lines:
            self.write_line(line, encoding=encoding, linesep=linesep)
        self.flush()

    def _raise_if_not_writble(self):
        if not self.writable():
            raise Exception("The SPIO is not writable.")

    @override
    def writable(self) -> bool:
        if self._checked_writable is None:
            self._checked_writable = self._check_writable()
        return self._checked_writable

    def get_drive_item(self) -> Optional[DriveItem]:
        if self._drive_item is None:
            self._drive_item = self._find_drive_item()
        return None if self._drive_item == SPIO._NO_DRIVE_ITEM else self._drive_item

    def __str__(self) -> str:
        return f"SPIO(path='{self.path}', location='{self.location}')"

    @property
    def mode(self):
        return "w+b" if self._writable else "rb"

    @override
    def fileno(self) -> int:
        raise Exception("fileno() is not supported.")


    # IO delegates

    @override
    def isatty(self) -> bool:
        return self._io_delegate.isatty()

    @override
    def tell(self) -> int:
        return self._io_delegate.tell()

    @override
    def seekable(self) -> bool:
        return self._io_delegate.seekable()

    @override
    def truncate(self, __size: Optional[int]) -> int:
        return self._io_delegate.truncate(__size)

    def _drive_item_might_be_created(self):
        if self._drive_item == SPIO._NO_DRIVE_ITEM:
            self._drive_item = None

    def _hook_io_delegate(self):
        native_write = self._io_delegate.write
        native_flush = self._io_delegate.flush

        def _write_hook(*args, **kwargs):
            self._written = True
            return native_write(*args, **kwargs)

        def _close_hook():
            if not self._closed:
                return self.close()

        def _flush_hook():
            native_flush()
            return self.flush(flush_delegate=False)

        self._io_delegate.write = _write_hook
        self._io_delegate.close = _close_hook
        self._io_delegate.flush = _flush_hook

    def _check_writable(self) -> bool:
        if not self._writable:
            return False
        drive_item = self.get_drive_item()
        if drive_item is not None:
            return True
        drive_item_parent, _ = self._try_create_parent_drive_item()
        if drive_item_parent is not None:
            return True
        return False

    def _find_drive_item(self) -> Union[DriveItem, object]:
        try:
            if self.location == Location.SHARED:
                drive_item = find_item_by_url(self.path, self.graph_client)
            elif self.location == Location.MY_DRIVE:
                drive_item = find_item_in_my_onedrive(self.path, self.graph_client)
            else:
                drive_item = find_item_in_site(_SHAREPOINT_HOST, self.path, self.location, self.graph_client)

            return SPIO._NO_DRIVE_ITEM if drive_item is None else drive_item
        except:
            return SPIO._NO_DRIVE_ITEM

    def _try_create_parent_drive_item(self) -> Tuple:
        try:
            parent, file_name = self._get_parent_and_name(self.path)
            if self.location == Location.SHARED:
                drive_item = find_item_by_url(parent, self.graph_client)
            elif self.location == Location.MY_DRIVE:
                drive_item = find_item_in_my_onedrive(parent, self.graph_client)
            else:
                drive_item = find_item_in_site(_SHAREPOINT_HOST, parent, self.location, self.graph_client)
            return drive_item, file_name
        except:
            return None, None

    def _get_parent_and_name(self, url):
        url_string = str(url).replace('\\', '/')
        last_slash_index = url_string.rfind('/')
        parent_url = url_string[:last_slash_index]
        name_url = url_string[last_slash_index + 1:]
        return parent_url, name_url

    def _assert_fully_downloaded(self):
        drive_item_file_size = self.get_drive_item().properties.get('size', None)
        self._assert_downloaded(until=drive_item_file_size)

    def _assert_downloaded(self, raise_when_drive_item_not_found: bool = True, until: int = None):
        if self._need_download(raise_when_drive_item_not_found, until):
            drive_item = self.get_drive_item()
            if drive_item is not None:
                drive_item_wrapper = _DriveItemWrapper(drive_item)
                # self._downloaded = True
                if until is None:
                    until = drive_item_wrapper.file_size()

                if until is None:
                    logging.debug(f"full download: {drive_item.web_url}")
                    drive_item.download(self._io_delegate)
                    self._download_complete = True
                else:
                    if until < self._downloaded_until + self.chunk_size:
                        until = self._downloaded_until + self.chunk_size

                    if until > drive_item_wrapper.file_size():
                        until = drive_item_wrapper.file_size()

                    if until > self._downloaded_until:
                        curr_pos = self.tell()
                        self.seek(self._downloaded_until)  # set the seek to the last downloaded position
                        drive_item_wrapper.download_range(self._io_delegate, self._downloaded_until, until, chunk_size=self.chunk_size)
                        self.graph_client.execute_query()
                        self.seek(curr_pos)

                    self._downloaded_until = until
                    self._download_complete = until == drive_item_wrapper.file_size()
            else:
                logging.debug(f"The file on SharePoint does not exist ({self.__str__()}).")
                if raise_when_drive_item_not_found:
                    raise Exception(f"Cannot find a SharePoint drive item for {self.__str__()}.")

    def _need_download(self, raise_when_drive_item_not_found: bool = True, until: int = None):
        if self._download_complete:
            return False
        if until is None:
            until = self._get_file_size(raise_when_drive_item_not_found)
        if until is None:
            return True
        return self._downloaded_until < until

    def _get_file_size(self, raise_when_drive_item_not_found: bool):
        drive_item = self.get_drive_item()
        if drive_item is not None:
            return drive_item.properties.get('size', None)
        if raise_when_drive_item_not_found:
            raise Exception(f"Cannot find a SharePoint drive item for {self.__str__()}.")
        else:
            return 0

    @override
    def __iter__(self) -> Iterator[bytes]:
        self.seek(0)
        return self

    @override
    def __next__(self) -> bytes:
        line = self.readline()
        if line == b'':
            raise StopIteration
        return line

    @override
    def __enter__(self) -> 'SPIO':
        return self

    @override
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    @override
    def __del__(self) -> None:
        try:
            self.close()
        except Exception as e:
            logging.error(f"Error closing SPIO object: {e}")

