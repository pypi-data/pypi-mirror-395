# dataform-view-migrator

Export BigQuery VIEW SQL definitions into a Dataform project with a predictable layout and safe write policies.

This README focuses on using the tool. For development setup and project conventions, see DEVELOPMENT.md.

## Prerequisites
- Python 3.10+
- Auth via Application Default Credentials (ADC):
  - Set `GOOGLE_APPLICATION_CREDENTIALS` to a service account JSON, or
  - Run `gcloud auth application-default login`
- Optional: `uv` to run without manually activating a venv

## Install
- With `uv` (recommended): `uv sync`
- Or use your existing Python 3.10+ environment and install deps from `pyproject.toml`

## Commands

- `dataform-view-migrator` (or `python -m dataform_view_migrator`): prints quick usage and version
- `dataform-view-migrator ping-bq [--project <id>] [--location <REGION>] [--config <toml>]`
  - Verifies auth and prints the resolved BigQuery project. If `--location` is provided (or set in TOML), it performs a regional INFORMATION_SCHEMA dry-run; otherwise it lists datasets to verify access.
- `dataform-view-migrator migrate-views [options]`
  - Discovers BigQuery views and writes files into the Dataform repo path.

Run `--help` on any command for complete options.

## Configuration

- Copy `dataform_view_migrator.example.toml` to `dataform_view_migrator.toml` and edit.
- CLI flags override TOML values when explicitly provided.

Key options (flag → TOML):
- `--source-project` → `source_project` (required via config or flag)
- `--dest <path>` → `dest` (required via config or flag)
- `--datasets a,b` → `datasets_include = ["a","b"]`
- `--exclude-datasets x,y` → `datasets_exclude = ["x","y"]`
- `--location US` → `location = "US"`
- `--ext sql|sqlx` → `ext = "sqlx"` (default `sqlx`)
- `--overwrite skip|backup|force` → `overwrite = "skip"` (default `skip`)
- `--add-dataform-header/--no-add-dataform-header` → `add_dataform_header = true|false`
- `--dry-run/--no-dry-run` → `dry_run = false`
- Optional dataset folder remapping: `dataset_folders = { src = "src_views" }`

## Output Layout

- Files are written under `dest/<dataset>/<view_name>.<ext>` by default.
- Use `dataset_folders` in TOML to map dataset names to custom subfolders.
- Extension `ext` is `sqlx` by default; set `--ext sql` for plain SQL files.

### Dataform Header (optional)
When enabled, each file is prefixed with a Dataform config block:

```
config {
  type: "view",
  schema: "<dataset>",
  name: "<view>"
  # optional fields below when configured
  # description: "...",
  # tags: ["..."]
}
```

Control via `--add-dataform-header` (or `add_dataform_header = true`).
Customize with `dataform_header.description` and `dataform_header.tags` in TOML.

## Overwrite Policy

- `skip` (default): do not modify existing files; they are reported as `skipped`.
- `backup`: if a file exists, move it to `<name>.<ext>.bak[.N]` and write the new content.
- `force`: overwrite files in place.

All modes support `--dry-run` to preview actions as `would-create`, `would-update`, or `would-skip` without writing.

## Examples

- Verify auth/project using TOML defaults:
  - `uv run dataform-view-migrator ping-bq --config dataform_view_migrator.toml`
- Migrate all views to a Dataform repo (US region, backup existing):
  - `uv run dataform-view-migrator migrate-views --source-project my-proj --dest ../dataform --location US --overwrite backup`
- Include specific datasets and emit plain SQL:
  - `uv run dataform-view-migrator migrate-views --source-project my-proj --dest ../dataform --datasets sales,finance --ext sql`
- Dry-run to review changes only:
  - `uv run dataform-view-migrator migrate-views --config dataform_view_migrator.toml --dry-run`

## Output Report

After migration, a table of per-view results is printed (dataset, view, action, path, error) followed by a compact summary grouped by action. A non-zero exit code is returned if any views fail.

## Development

See DEVELOPMENT.md for environment setup, linting/formatting, tests, and project layout.

