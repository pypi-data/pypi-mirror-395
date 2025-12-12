import os
import json
import hashlib
import zipfile
from datetime import datetime
from typing import Optional
import shutil


def check_assets_exist(
    base_path: str, required_dirs: list[str]
) -> tuple[bool, list[str]]:
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = os.path.join(base_path, dir_name)
        if not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            missing_dirs.append(dir_name)
            continue
        has_files = any(files for _, _, files in os.walk(dir_path))
        if not has_files:
            missing_dirs.append(dir_name)
    return len(missing_dirs) == 0, missing_dirs


def prompt_user_confirmation(message: str) -> bool:
    print(f"\n{message}")
    while True:
        response = input("Continue? (yes/no): ").lower().strip()
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False
        print("Please answer 'yes' or 'no'")


def download_file(url: str, destination: str) -> None:
    import urllib.request

    def progress_hook(block_num, block_size, total_size):
        if total_size > 0:
            downloaded = block_num * block_size
            percent = min(100, (downloaded / total_size) * 100)
            bar_length = 50
            filled_length = int(bar_length * downloaded // total_size)
            bar = "=" * filled_length + "-" * (bar_length - filled_length)
            print(f"\rDownloading: [{bar}] {percent:.1f}%", end="", flush=True)

    urllib.request.urlretrieve(url, destination, progress_hook)
    print()


def extract_zip(zip_path: str, extract_to: str) -> None:
    print("Extracting assets...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    macosx_path = os.path.join(extract_to, "__MACOSX")
    if os.path.exists(macosx_path) and os.path.isdir(macosx_path):
        shutil.rmtree(macosx_path)
    os.remove(zip_path)


def calculate_directory_hash(dir_path: str) -> str:
    hash_md5 = hashlib.md5()
    for root, dirs, files in sorted(os.walk(dir_path)):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
    return hash_md5.hexdigest()


def count_files_in_directory(dir_path: str) -> int:
    return sum(len(files) for _, _, files in os.walk(dir_path))


def generate_manifest(
    base_path: str,
    version: str,
    directories: list[str],
    output_path: Optional[str] = None,
) -> dict:
    manifest = {
        "version": version,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "files": {},
    }

    for dir_name in directories:
        dir_path = os.path.join(base_path, dir_name)
        if os.path.exists(dir_path):
            manifest["files"][dir_name] = {
                "count": count_files_in_directory(dir_path),
                "checksum": calculate_directory_hash(dir_path),
            }

    if output_path:
        with open(output_path, "w") as f:
            json.dump(manifest, f, indent=2)

    return manifest


def fetch_manifest(url: str) -> Optional[dict]:
    import urllib.request
    import urllib.error
    import time

    try:
        cache_buster = f"?_={int(time.time())}"
        request = urllib.request.Request(
            url + cache_buster,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError):
        return None


def save_local_manifest(manifest: dict, manifest_path: str) -> None:
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)


def load_local_manifest(manifest_path: str) -> Optional[dict]:
    if not os.path.exists(manifest_path):
        return None
    try:
        with open(manifest_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def compare_versions(version1: str, version2: str) -> int:
    def parse_version(v: str) -> tuple:
        return tuple(map(int, v.split(".")))

    try:
        v1_parts = parse_version(version1)
        v2_parts = parse_version(version2)

        if v1_parts < v2_parts:
            return -1
        elif v1_parts > v2_parts:
            return 1
        else:
            return 0
    except (ValueError, AttributeError):
        return 0


def compare_manifests(local_manifest: dict, remote_manifest: dict) -> tuple[bool, str]:
    """
    Compare local and remote manifests comprehensively.

    Returns:
        tuple[bool, str]: (needs_update, reason)
            - needs_update: True if local assets need updating
            - reason: Human-readable reason for the update
    """
    if not local_manifest or not remote_manifest:
        return True, "Missing manifest"

    local_version = local_manifest.get("version", "0.0.0")
    remote_version = remote_manifest.get("version", "0.0.0")

    version_diff = compare_versions(local_version, remote_version)
    if version_diff < 0:
        return (
            True,
            f"Version outdated (local: {local_version}, remote: {remote_version})",
        )

    local_files = local_manifest.get("files", {})
    remote_files = remote_manifest.get("files", {})

    if set(local_files.keys()) != set(remote_files.keys()):
        missing = set(remote_files.keys()) - set(local_files.keys())
        extra = set(local_files.keys()) - set(remote_files.keys())
        if missing:
            return True, f"Missing directories: {', '.join(missing)}"
        if extra:
            return True, f"Extra directories: {', '.join(extra)}"

    for dir_name, remote_info in remote_files.items():
        local_info = local_files.get(dir_name, {})

        if local_info.get("count") != remote_info.get("count"):
            return (
                True,
                f"File count mismatch in {dir_name} (local: {local_info.get('count')}, remote: {remote_info.get('count')})",
            )

        if local_info.get("checksum") != remote_info.get("checksum"):
            return True, f"Checksum mismatch in {dir_name}"

    return False, "Assets are up to date"


def verify_manifest_checksums(base_path: str, manifest: dict) -> tuple[bool, list[str]]:
    mismatched = []
    for dir_name, info in manifest.get("files", {}).items():
        dir_path = os.path.join(base_path, dir_name)
        if not os.path.exists(dir_path):
            mismatched.append(dir_name)
            continue
        actual_checksum = calculate_directory_hash(dir_path)
        if actual_checksum != info.get("checksum"):
            mismatched.append(dir_name)
    return len(mismatched) == 0, mismatched
