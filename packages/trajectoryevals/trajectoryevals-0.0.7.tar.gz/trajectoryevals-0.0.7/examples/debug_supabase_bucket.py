"""
Simple debugging script to inspect Supabase storage buckets.

Usage:
    uv run sdk/examples/debug_supabase_bucket.py

Environment variables required:
    TRAJECTORY_API_KEY       - Your application API key (for authenticated access)
    BACKEND_URL              - Backend API URL (default: http://localhost:8000)

Optional environment variables:
    WORKDAY_INSTANCE_BUCKET  - Bucket name (default: "app_data")
    WORKDAY_INSTANCE_PREFIX  - Prefix/path within the bucket (default: "workday")
    SUPABASE_URL             - Supabase project URL (for direct storage test)
    SUPABASE_SERVICE_KEY     - Service role key (for direct storage test)

Note: This script uses backend API endpoints which handle authentication
and filtering via TRAJECTORY_API_KEY. Optionally, you can also test direct
storage access using SUPABASE_SERVICE_KEY.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

import dotenv
import requests

dotenv.load_dotenv()


def test_direct_storage_access(
    supabase_url: str, service_key: str, bucket: str, prefix: str = ""
):
    """Test direct Supabase storage access using service key"""
    print("\n" + "=" * 60)
    print("[TEST] Direct Storage Access (using SERVICE_KEY)")
    print("=" * 60)

    # Clean bucket name
    bucket_clean = bucket.rstrip("/")
    storage_url = f"{supabase_url}/storage/v1/object/list/{bucket_clean}"

    # Build request body (Storage API uses POST with JSON body, not GET with params)
    body = {}
    if prefix:
        # Add trailing slash for directory listing
        body["prefix"] = (
            prefix.rstrip("/") + "/" if not prefix.endswith("/") else prefix
        )

    # Storage API headers
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }

    print(f"[TEST] URL: {storage_url}")
    print(f"[TEST] Request Body: {body}")
    print("[TEST] Headers: apikey, Authorization, Content-Type\n")

    try:
        # CRITICAL: Supabase Storage API list endpoint uses POST, not GET
        response = requests.post(
            storage_url,
            headers=headers,
            json=body,  # Use json body instead of query params
            timeout=30,
        )

        print(f"[TEST] Status Code: {response.status_code}")

        if response.status_code == 404:
            print(f"[TEST] ERROR: Bucket '{bucket_clean}' not found")
            print(f"[TEST] Response: {response.text}")

            # Try to list all buckets
            print("\n[TEST] Attempting to list all buckets...")
            buckets_url = f"{supabase_url}/storage/v1/bucket"
            buckets_response = requests.get(buckets_url, headers=headers, timeout=10)
            if buckets_response.status_code == 200:
                buckets = buckets_response.json()
                bucket_names = [b.get("name") for b in buckets if isinstance(b, dict)]
                print(f"[TEST] Available buckets: {bucket_names}")
            else:
                print(
                    f"[TEST] Could not list buckets: {buckets_response.status_code} - {buckets_response.text}"
                )
            return []

        if response.status_code >= 400:
            print(f"[TEST] ERROR: {response.status_code} - {response.text}")
            return []

        files = response.json()
        if not isinstance(files, list):
            print(f"[TEST] WARNING: Expected list, got {type(files)}")
            print(f"[TEST] Response: {files}")
            return []

        print(f"[TEST] Success! Found {len(files)} items")

        # Show all items with their types
        folders = [f for f in files if isinstance(f, dict) and f.get("id") is None]
        db_files = [
            f
            for f in files
            if isinstance(f, dict) and f.get("name", "").endswith(".db")
        ]
        other_files = [
            f
            for f in files
            if isinstance(f, dict)
            and f.get("id") is not None
            and not f.get("name", "").endswith(".db")
        ]

        if folders:
            print(f"\n[TEST] Found {len(folders)} folders:")
            for f in folders[:10]:
                name = f.get("name", "")
                print(f"  📁 {name}/")
            if len(folders) > 10:
                print(f"  ... and {len(folders) - 10} more")

        if db_files:
            print(f"\n[TEST] Found {len(db_files)} .db files:")
            for f in db_files[:10]:
                name = f.get("name", "")
                size = f.get("metadata", {}).get("size", "?")
                updated = f.get("updated_at", "?")
                print(f"  💾 {name} (size: {size}, updated: {updated})")
            if len(db_files) > 10:
                print(f"  ... and {len(db_files) - 10} more")

        if other_files:
            print(f"\n[TEST] Found {len(other_files)} other files:")
            for f in other_files[:5]:
                name = f.get("name", "")
                size = f.get("metadata", {}).get("size", "?")
                print(f"  📄 {name} (size: {size})")
            if len(other_files) > 5:
                print(f"  ... and {len(other_files) - 5} more")

        if not folders and not db_files and not other_files:
            print(f"\n[TEST] No items found at prefix: '{prefix}'")
            print("[TEST] Try listing without prefix or check if the path is correct")

        return files

    except Exception as e:
        print(f"[TEST] Exception: {e}")
        import traceback

        traceback.print_exc()
        return []


def main() -> None:
    trajectory_api_key = os.environ.get("TRAJECTORY_API_KEY")
    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")
    prefix = os.environ.get("WORKDAY_INSTANCE_PREFIX", "workday")
    bucket = os.environ.get("WORKDAY_INSTANCE_BUCKET", "app_data")

    # Optional: Direct storage access test
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_service_key = os.environ.get("SUPABASE_SERVICE_KEY")

    # Test direct storage access if service key is provided
    if supabase_url and supabase_service_key:
        test_direct_storage_access(supabase_url, supabase_service_key, bucket, prefix)

    if not trajectory_api_key:
        if not supabase_service_key:
            raise SystemExit(
                "Missing TRAJECTORY_API_KEY environment variable. "
                "This script requires either:\n"
                "  - TRAJECTORY_API_KEY (for backend API access), or\n"
                "  - SUPABASE_SERVICE_KEY (for direct storage test)"
            )
        else:
            print("\n[info] No TRAJECTORY_API_KEY provided, skipping backend API test")
            return

    print("\n" + "=" * 60)
    print("[TEST] Backend API Access (using TRAJECTORY_API_KEY)")
    print("=" * 60)
    print(f"[debug] Using backend API: {backend_url}")
    print(f"[debug] Prefix filter: {prefix!r}\n")

    # List databases using backend API (handles authentication and filtering)
    try:
        response = requests.get(
            f"{backend_url}/api/databases/",
            headers={"Authorization": f"Bearer {trajectory_api_key}"},
            timeout=30,
        )

        if response.status_code == 401:
            print("[error] Authentication failed: Invalid API key")
            return
        elif response.status_code != 200:
            print(
                f"[error] Failed to list databases: {response.status_code} - {response.text}"
            )
            return

        databases = response.json()

        # Filter by prefix if specified
        if prefix:
            databases = [
                db
                for db in databases
                if db.get("path", "").startswith(prefix)
                or db.get("folder", "").startswith(prefix)
            ]

        if not databases:
            print("[debug] No databases found (matching prefix filter if specified).")
            return

        print(f"[debug] Found {len(databases)} accessible databases:")
        for db in databases:
            path = db.get("path", "")
            name = db.get("name", "")
            access_type = db.get("access_type", "read")
            size = db.get("metadata", {}).get("size", "?")
            print(f"  • {path} (access: {access_type}, size: {size})")

        # Test downloading files
        if databases:
            print("\n[TEST] Testing file downloads...")
            test_download_files(
                backend_url, trajectory_api_key, databases[:3]
            )  # Download first 3 files

    except requests.exceptions.RequestException as e:
        print(f"[error] Failed to connect to backend: {e}")
        print(f"[error] Make sure the backend is running at {backend_url}")
    except Exception as e:
        print(f"[error] Unexpected error: {e}")


def test_download_files(backend_url: str, api_key: str, databases: list[dict]) -> None:
    """Test downloading database files to a temporary directory"""
    print("\n" + "=" * 60)
    print("[TEST] File Download Test")
    print("=" * 60)

    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="trajectory_db_test_"))
    print(f"[TEST] Created temp directory: {temp_dir}")

    headers = {"Authorization": f"Bearer {api_key}"}
    downloaded_count = 0
    failed_count = 0

    try:
        for db in databases:
            path = db.get("path", "")
            if not path:
                continue

            # Get filename from path
            filename = path.split("/")[-1]
            if not filename.endswith(".db"):
                filename = f"{filename}.db"

            local_path = temp_dir / filename

            print(f"\n[TEST] Downloading: {path}")
            print(f"[TEST] Saving to: {local_path}")

            try:
                download_url = f"{backend_url}/api/databases/{path}"
                response = requests.get(
                    download_url, headers=headers, timeout=60, stream=True
                )

                if response.status_code == 200:
                    with open(local_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    file_size = local_path.stat().st_size
                    print(f"[TEST] ✅ Downloaded {filename} ({file_size} bytes)")
                    downloaded_count += 1
                elif response.status_code == 401:
                    print("[TEST] ❌ Authentication failed")
                    failed_count += 1
                elif response.status_code == 403:
                    print(f"[TEST] ❌ Access denied for {path}")
                    failed_count += 1
                else:
                    print(
                        f"[TEST] ❌ Failed: HTTP {response.status_code} - {response.text[:100]}"
                    )
                    failed_count += 1

            except Exception as e:
                print(f"[TEST] ❌ Exception: {e}")
                failed_count += 1

        print("\n[TEST] Download Summary:")
        print(f"[TEST]   ✅ Successfully downloaded: {downloaded_count}")
        print(f"[TEST]   ❌ Failed: {failed_count}")
        print(f"[TEST]   📁 Files saved in: {temp_dir}")
        print("[TEST]   💡 Note: Temp directory will be cleaned up on exit")

    except Exception as e:
        print(f"[TEST] ❌ Error during download test: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Optionally clean up - comment out if you want to keep files for inspection
        # print(f"\n[TEST] Cleaning up temp directory: {temp_dir}")
        # shutil.rmtree(temp_dir, ignore_errors=True)
        pass


if __name__ == "__main__":
    main()
