 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/morphopy/downloader.py b/morphopy/downloader.py
new file mode 100644
index 0000000000000000000000000000000000000000..b42df81c9b60af59901633d6877484c88a1dddcd
--- /dev/null
+++ b/morphopy/downloader.py
@@ -0,0 +1,76 @@
+from __future__ import annotations
+
+import shutil
+import urllib.error
+import urllib.request
+from pathlib import Path
+from typing import Optional
+
+from .data_registry import DatasetEntry, get_dataset
+
+
+DEFAULT_BASE_URL = (
+    "https://raw.githubusercontent.com/jamilaltha/TTA-Universal-Data/main/morphopy/data/samples"
+)
+
+
+def get_default_base_url() -> str:
+    """Return the default GitHub base URL for sample data."""
+
+    return DEFAULT_BASE_URL
+
+
+def _copy_packaged_sample(dataset: DatasetEntry, destination: Path) -> Path:
+    """Copy the bundled sample file into the destination directory."""
+
+    from importlib import resources
+
+    destination.parent.mkdir(parents=True, exist_ok=True)
+    with resources.open_binary("morphopy.data.samples", dataset.sample_file) as source:
+        with destination.open("wb") as target:
+            shutil.copyfileobj(source, target)
+    return destination
+
+
+def download_dataset(
+    identifier: str | int,
+    target_dir: Optional[Path] = None,
+    base_url: Optional[str] = None,
+    *,
+    overwrite: bool = False,
+) -> Path:
+    """Download a dataset sample from GitHub or copy the bundled fallback.
+
+    Parameters
+    ----------
+    identifier:
+        Dataset slug (e.g., ``"particle_physics_lhc"``) or numeric ID.
+    target_dir:
+        Folder where the file will be placed. Defaults to ``~/.morphopy``.
+    base_url:
+        Remote base URL where the dataset files live. If omitted, uses the
+        packaged GitHub sample location. This can be pointed to your own
+        repository hosting full-resolution assets.
+    overwrite:
+        When ``True``, redownloads even if the target file already exists.
+    """
+
+    dataset = get_dataset(identifier)
+    target_dir = target_dir or Path.home() / ".morphopy"
+    target_dir.mkdir(parents=True, exist_ok=True)
+
+    filename = dataset.download_name
+    target_path = target_dir / filename
+
+    if target_path.exists() and not overwrite:
+        return target_path
+
+    base_url = base_url or get_default_base_url()
+    remote_url = f"{base_url.rstrip('/')}/{dataset.sample_file}"
+
+    try:
+        urllib.request.urlretrieve(remote_url, target_path)
+        return target_path
+    except (urllib.error.URLError, urllib.error.HTTPError):
+        # Fall back to bundled sample data if remote pull fails.
+        return _copy_packaged_sample(dataset, target_path)
 
EOF
)