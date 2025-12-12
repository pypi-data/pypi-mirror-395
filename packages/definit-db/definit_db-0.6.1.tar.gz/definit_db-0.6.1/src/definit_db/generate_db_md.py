import importlib
import os
from pathlib import Path

from definit_db.data.track import get_track_list
from definit_db.data.track.track import Track
from definit_db.definition.definition import Definition
from definit_db.definition.field import Field

_FIELDS = [Field.MATHEMATICS, Field.COMPUTER_SCIENCE]
_DEFINIT_DB_PACKAGE_ROOT = Path(os.path.dirname(__file__))
_PATH_DATA_MD = _DEFINIT_DB_PACKAGE_ROOT / "data_md"
_PATH_DATA_FIELD_MD = _PATH_DATA_MD / "field"
_PATH_DATA_TRACK_MD = _PATH_DATA_MD / "track"
_MODULE_FIELD = "definit_db.data.field"


def get_field_index(field: Field):
    module = importlib.import_module(f"{_MODULE_FIELD}.{field}.index")
    return getattr(module, "field_index")


def definition_to_md(defn: Definition) -> str:
    return f"# {defn.key.name}\n\n{defn.content}\n"


def get_md_path(defn: Definition, field: Field) -> str:
    mod = type(defn).__module__
    rel_mod = mod.split(f"{_MODULE_FIELD}.", 1)[-1]
    prefix = f"{field}."

    if rel_mod.startswith(prefix):
        rel_mod = rel_mod[len(prefix) :]

    rel_mod = rel_mod.replace(".", os.sep)

    if rel_mod.endswith("__init__"):
        rel_mod = rel_mod[: -len("__init__")]

    md_dir = os.path.join(_PATH_DATA_FIELD_MD, field, os.path.dirname(rel_mod))
    os.makedirs(md_dir, exist_ok=True)
    md_path = os.path.join(md_dir, f"{defn.key.name}.md")
    return md_path


def write_index_md(field: Field, field_index: list[Definition]) -> None:
    lines: list[str] = []

    for defn in field_index:
        mod = type(defn).__module__
        rel_mod = mod.split(f"{_MODULE_FIELD}.", 1)[-1]
        prefix = f"{field}."

        if rel_mod.startswith(prefix):
            rel_mod = rel_mod[len(prefix) :]

        rel_mod = rel_mod.replace(".", "/")

        if rel_mod.endswith("__init__"):
            rel_mod = rel_mod[: -len("__init__")]

        if rel_mod.startswith("definitions/"):
            rel_mod = rel_mod[len("definitions/") :]

        rel_path = rel_mod.strip("/")
        lines.append(f"- [{defn.key.name}]({rel_path})")

    md_dir = os.path.join(_PATH_DATA_FIELD_MD, field)
    os.makedirs(md_dir, exist_ok=True)
    md_path = os.path.join(md_dir, "index.md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _dump_track_md(track: Track, out_path: Path) -> None:
    """Dump the track as an .md file in the same form as index.md (see attachments)."""
    lines: list[str] = []

    for key in get_track_list(track):
        # Compose relative path: <field>/<name>
        lines.append(f"- [{key.name}]({key.field.lower()}/{key.name})")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    # Write Markdown files for each definition in the specified fields
    for field in _FIELDS:
        field_index = get_field_index(field)
        for defn in field_index:
            if not isinstance(defn, Definition):
                continue
            md_path = get_md_path(defn, field)
            md_content = definition_to_md(defn)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_content)
        # Write the index Markdown file for the field
        write_index_md(field, field_index)

    # Write Markdown files for each track
    _PATH_DATA_TRACK_MD.mkdir(parents=True, exist_ok=True)

    for track in Track:
        _dump_track_md(track=track, out_path=_PATH_DATA_TRACK_MD / f"{track}.md")


if __name__ == "__main__":
    main()
