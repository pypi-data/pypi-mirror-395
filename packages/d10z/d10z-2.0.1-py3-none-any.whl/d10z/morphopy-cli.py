 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/morphopy/cli.py b/morphopy/cli.py
new file mode 100644
index 0000000000000000000000000000000000000000..523146c773bf87d5db98d591ebb07c8b70fa6098
--- /dev/null
+++ b/morphopy/cli.py
@@ -0,0 +1,77 @@
+from __future__ import annotations
+
+import argparse
+from pathlib import Path
+
+from .data_registry import get_dataset, list_datasets
+from .downloader import download_dataset, get_default_base_url
+
+
+def _format_entry(entry) -> str:
+    return (
+        f"[{entry.id}] {entry.name}\n"
+        f"  slug: {entry.slug}\n"
+        f"  scale: {entry.scale}\n"
+        f"  status: {entry.status} | metric: {entry.metric}\n"
+        f"  description: {entry.description}\n"
+    )
+
+
+def main(argv: list[str] | None = None) -> int:
+    parser = argparse.ArgumentParser(description="MorphoPy dataset helper")
+    subparsers = parser.add_subparsers(dest="command", required=True)
+
+    subparsers.add_parser("list", help="List available datasets")
+
+    info_parser = subparsers.add_parser("info", help="Show details for a dataset")
+    info_parser.add_argument("identifier", help="Dataset ID or slug")
+
+    download_parser = subparsers.add_parser("download", help="Download a dataset sample")
+    download_parser.add_argument("identifier", help="Dataset ID or slug")
+    download_parser.add_argument(
+        "--dest",
+        type=Path,
+        default=None,
+        help="Destination directory (defaults to ~/.morphopy)",
+    )
+    download_parser.add_argument(
+        "--base-url",
+        default=None,
+        help=(
+            "Base URL for dataset hosting. Defaults to the GitHub sample"
+            " location so you can swap in your own repository later."
+        ),
+    )
+    download_parser.add_argument(
+        "--overwrite", action="store_true", help="Redownload even if cached"
+    )
+
+    args = parser.parse_args(argv)
+
+    if args.command == "list":
+        for entry in list_datasets():
+            print(_format_entry(entry))
+        return 0
+
+    if args.command == "info":
+        entry = get_dataset(args.identifier if not args.identifier.isdigit() else int(args.identifier))
+        print(_format_entry(entry))
+        print(f"Default base URL: {get_default_base_url()}")
+        return 0
+
+    if args.command == "download":
+        identifier = args.identifier if not args.identifier.isdigit() else int(args.identifier)
+        path = download_dataset(
+            identifier=identifier,
+            target_dir=args.dest,
+            base_url=args.base_url,
+            overwrite=args.overwrite,
+        )
+        print(f"Saved to {path}")
+        return 0
+
+    return 1
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
 
EOF
)