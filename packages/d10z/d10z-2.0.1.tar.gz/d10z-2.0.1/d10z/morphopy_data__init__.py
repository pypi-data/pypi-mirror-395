 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/morphopy/data/__init__.py b/morphopy/data/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..23956c6ec4a8b6bf5d7e418021c68ab3e5036a9e
--- /dev/null
+++ b/morphopy/data/__init__.py
@@ -0,0 +1 @@
+"""Packaged data assets for MorphoPy."""
 
EOF
)