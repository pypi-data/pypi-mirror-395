 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/morphopy/data/samples/__init__.py b/morphopy/data/samples/__init__.py
new file mode 100644
index 0000000000000000000000000000000000000000..fa9076e065bf295b46b158a3b30443509cd3edb2
--- /dev/null
+++ b/morphopy/data/samples/__init__.py
@@ -0,0 +1 @@
+"""Bundled MorphoPy sample datasets."""
 
EOF
)