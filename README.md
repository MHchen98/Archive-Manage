diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..3d0acbd9c1b93cb21e9bceae3599c3bb93b61e14
--- /dev/null
+++ b/README.md
@@ -0,0 +1,51 @@
+# Archive Management (Python)
+
+Starter implementation for an archive management system with:
+
+- Basic required fields (`Index`, `Title`, `time`, `author_or_publisher`)
+- User-defined custom fields for additional metadata classification
+- Content stored either as direct text (`content_mode = text`) or as a local file path (`content_mode = file`)
+- JSON-backed storage (`archive_db.json`)
+- Interactive command-line interface
+
+## Run
+
+```bash
+python3 archive_manager.py
+```
+
+## JSON structure
+
+The database file uses this structure:
+
+```json
+{
+  "schema": {
+    "basic_fields": {
+      "Index": "Archival index code",
+      "Title": "Document title",
+      "time": "Published time",
+      "author_or_publisher": "Author or publication name"
+    },
+    "custom_fields": {
+      "department": "Owning department"
+    }
+  },
+  "records": [
+    {
+      "Index": "A-001",
+      "Title": "Annual report",
+      "time": "2025-01-01",
+      "author_or_publisher": "Archive Office",
+      "content_mode": "text",
+      "content": "Summary...",
+      "custom_fields": {
+        "department": "Finance"
+      },
+      "created_at": "2026-01-01T10:00:00"
+    }
+  ]
+}
+```
+
+This is a foundation focused on database structure and metadata workflow; you can later swap in a GUI (e.g., Tkinter, web UI) while keeping the same JSON schema.
