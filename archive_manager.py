from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_FIELDS: Dict[str, str] = {
    "Index": "Archival index code",
    "Title": "Document title",
    "time": "Published time",
    "author_or_publisher": "Author or publication name",
}


@dataclass
class ArchiveRecord:
    """A single archive document record."""

    Index: str
    Title: str
    time: str
    author_or_publisher: str
    content_mode: str
    content: str
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Index": self.Index,
            "Title": self.Title,
            "time": self.time,
            "author_or_publisher": self.author_or_publisher,
            "content_mode": self.content_mode,
            "content": self.content,
            "custom_fields": self.custom_fields,
            "created_at": self.created_at,
        }


class ArchiveDatabase:
    """JSON-backed archive database with user-defined schema fields."""

    def __init__(self, db_path: str = "archive_db.json") -> None:
        self.db_path = Path(db_path)
        self.data: Dict[str, Any] = {
            "schema": {
                "basic_fields": DEFAULT_FIELDS,
                "custom_fields": {},
            },
            "records": [],
        }
        self.load()

    def load(self) -> None:
        if self.db_path.exists():
            self.data = json.loads(self.db_path.read_text(encoding="utf-8"))

    def save(self) -> None:
        self.db_path.write_text(
            json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def add_custom_field(self, varname: str, description: str) -> None:
        self.data["schema"]["custom_fields"][varname] = description
        self.save()

    def add_record(self, record: ArchiveRecord) -> None:
        self.data["records"].append(record.to_dict())
        self.save()

    def find_by_index(self, index: str) -> Optional[Dict[str, Any]]:
        for record in self.data["records"]:
            if record.get("Index") == index:
                return record
        return None

    def list_records(self) -> List[Dict[str, Any]]:
        return list(self.data["records"])


class ArchiveCLI:
    """Simple interactive CLI for managing archive metadata."""

    def __init__(self, db: ArchiveDatabase) -> None:
        self.db = db

    def run(self) -> None:
        menu = {
            "1": self.show_schema,
            "2": self.create_custom_field,
            "3": self.create_record,
            "4": self.show_records,
            "5": self.search_by_index,
        }

        while True:
            print("\nArchive Management Menu")
            print("1) Show current field schema")
            print("2) Add custom field")
            print("3) Add archive record")
            print("4) List records")
            print("5) Find record by Index")
            print("0) Exit")

            choice = input("Select an option: ").strip()
            if choice == "0":
                print("Bye.")
                return

            action = menu.get(choice)
            if action:
                action()
            else:
                print("Invalid choice.")

    def show_schema(self) -> None:
        schema = self.db.data["schema"]
        print("\nBasic fields:")
        for name, desc in schema["basic_fields"].items():
            print(f"- {name}: {desc}")

        print("Custom fields:")
        if not schema["custom_fields"]:
            print("- (none)")
        else:
            for name, desc in schema["custom_fields"].items():
                print(f"- {name}: {desc}")

    def create_custom_field(self) -> None:
        varname = input("Custom field varname (e.g., department): ").strip()
        description = input("Description: ").strip()
        if not varname:
            print("Field varname cannot be empty.")
            return
        self.db.add_custom_field(varname, description)
        print(f"Custom field '{varname}' saved.")

    def create_record(self) -> None:
        print("\nFill in basic fields")
        index = input("Index: ").strip()
        title = input("Title: ").strip()
        time = input("Published time: ").strip()
        author_or_publisher = input("Author or publisher: ").strip()

        content_mode = input("Store content as (text/file): ").strip().lower()
        if content_mode not in {"text", "file"}:
            print("Invalid content mode; choose 'text' or 'file'.")
            return

        if content_mode == "text":
            content = input("Enter text content: ").strip()
        else:
            content = input("Enter local file path: ").strip()

        custom_values: Dict[str, Any] = {}
        for field_name in self.db.data["schema"]["custom_fields"].keys():
            custom_values[field_name] = input(f"{field_name}: ").strip()

        record = ArchiveRecord(
            Index=index,
            Title=title,
            time=time,
            author_or_publisher=author_or_publisher,
            content_mode=content_mode,
            content=content,
            custom_fields=custom_values,
        )
        self.db.add_record(record)
        print("Record saved.")

    def show_records(self) -> None:
        records = self.db.list_records()
        if not records:
            print("No records yet.")
            return
        for idx, record in enumerate(records, start=1):
            print(f"\n[{idx}] {record['Index']} | {record['Title']}")
            print(json.dumps(record, indent=2, ensure_ascii=False))

    def search_by_index(self) -> None:
        index = input("Index to find: ").strip()
        record = self.db.find_by_index(index)
        if not record:
            print("Not found.")
            return
        print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    database = ArchiveDatabase("archive_db.json")
    ArchiveCLI(database).run()
