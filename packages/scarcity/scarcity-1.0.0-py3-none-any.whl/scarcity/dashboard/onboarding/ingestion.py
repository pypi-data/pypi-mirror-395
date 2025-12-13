"""CSV ingestion helpers for onboarding clients."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import BinaryIO, Iterable, List, Sequence

from . import clients, domains
from .state import (
    STATE,
    STATE_LOCK,
    ClientState,
    UploadColumn,
    UploadRecord,
    generate_id,
    hash_api_key,
)

UPLOAD_ROOT = Path("artifacts/uploads")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

SAMPLE_LIMIT = 500
CSV_ENCODING_CANDIDATES: tuple[str, ...] = ("utf-8", "utf-8-sig", "latin-1")
CSV_BINARY_SIGNATURES: dict[bytes, str] = {
    b"PK\x03\x04": "Excel workbook (.xlsx)",
    b"\xD0\xCF\x11\xE0": "legacy Excel workbook (.xls)",
    b"%PDF": "PDF document",
}


def _copy_to_disk(stream: BinaryIO, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    stream.seek(0)
    with destination.open("wb") as handle:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    stream.seek(0)


def _normalise(name: str) -> str:
    return name.strip().lower()


def _is_datetime(value: str) -> bool:
    value = value.strip()
    if not value:
        return False
    # Quick checks for ISO-like timestamps.
    if value.count("-") >= 2 and "T" in value:
        return True
    if value.count("/") == 2:
        return True
    return False


def _is_float(value: str) -> bool:
    value = value.strip()
    if not value:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def _is_int(value: str) -> bool:
    value = value.strip()
    if not value or not _is_float(value):
        return False
    try:
        parsed = float(value)
        return parsed.is_integer()
    except ValueError:
        return False


def _infer_dtype(values: Iterable[str]) -> str:
    tests = list(values)
    tests = [value for value in tests if value not in (None, "", "null", "NULL")]
    if not tests:
        return "string"
    if all(_is_datetime(value) for value in tests if value):
        return "datetime"
    if all(_is_int(value) for value in tests):
        return "integer"
    if all(_is_float(value) for value in tests):
        return "float"
    if any(_is_datetime(value) for value in tests):
        return "datetime"
    return "string"


def _infer_role(name: str, dtype: str) -> str:
    normalised = _normalise(name)
    if (
        "time" in normalised
        or "date" in normalised
        or "timestamp" in normalised
        or "year" in normalised
    ):
        return "time"
    if "id" in normalised or normalised.endswith("_id"):
        return "identifier"
    if dtype in {"float", "integer"}:
        return "metric"
    return "dimension"

def _reject_binary_payload(path: Path) -> None:
    with path.open("rb") as raw:
        prefix = raw.read(8)
    for signature, label in CSV_BINARY_SIGNATURES.items():
        if prefix.startswith(signature):
            raise ValueError(f"Uploaded file appears to be {label}. Please export it as CSV.")
    if b"\x00" in prefix:
        raise ValueError("Uploaded file contains binary markers. Please upload a plain-text CSV.")


def _read_csv_with_encoding(path: Path, encoding: str) -> tuple[list[str], list[list[str]], int]:
    with path.open("r", newline="", encoding=encoding) as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("CSV file is empty.")

        samples: list[list[str]] = []
        rows = 0
        for row in reader:
            rows += 1
            if len(samples) < SAMPLE_LIMIT:
                samples.append(row)
    return header, samples, rows


def _analyse_csv(path: Path) -> tuple[int, List[UploadColumn], str]:
    _reject_binary_payload(path)
    last_decode_error: UnicodeDecodeError | None = None
    header: list[str] = []
    samples: list[list[str]] = []
    rows: int = 0
    for encoding in CSV_ENCODING_CANDIDATES:
        try:
            header, samples, rows = _read_csv_with_encoding(path, encoding)
            break
        except UnicodeDecodeError as exc:
            last_decode_error = exc
    else:
        raise ValueError(
            "CSV file could not be decoded. Please save it as UTF-8 (recommended) or Latin-1."
        ) from last_decode_error

    if rows == 0 and not samples:
        raise ValueError("CSV file contains no data rows.")

    columns: list[UploadColumn] = []
    for idx, raw_name in enumerate(header):
        values = [row[idx] if idx < len(row) else "" for row in samples]
        dtype = _infer_dtype(values)
        role = _infer_role(raw_name, dtype)
        nulls = sum(1 for value in values if not value or value in ("null", "NULL"))
        total = max(len(values), 1)
        null_pct = (nulls / total) * 100.0
        columns.append(
            UploadColumn(
                name=raw_name.strip(),
                suggested_dtype=dtype,
                role=role,
                null_pct=round(null_pct, 2),
            )
        )

    signature = ",".join(f"{col.name}:{col.suggested_dtype}" for col in columns)
    schema_hash = hash_api_key(signature) if signature else generate_id("schema")

    return rows, columns, schema_hash


def create_upload(client_id: str, domain_id: str, filename: str, stream: BinaryIO) -> UploadRecord:
    """Persist the uploaded CSV and run schema inference."""

    client = clients.get_client(client_id)
    if not client:
        raise ValueError("Client not found.")
    if client.domain_id != domain_id:
        raise ValueError("Client not associated with domain.")

    if not domains.get_domain(domain_id):
        raise ValueError("Domain not found.")

    upload_id = generate_id("upload")
    path = UPLOAD_ROOT / domain_id / f"{upload_id}.csv"
    _copy_to_disk(stream, path)

    rows, columns, schema_hash = _analyse_csv(path)

    record = UploadRecord(
        id=upload_id,
        client_id=client_id,
        domain_id=domain_id,
        filename=filename,
        path=str(path),
        rows=rows,
        columns=columns,
        schema_hash=schema_hash,
        status="validating",
    )

    with STATE_LOCK:
        STATE.uploads[upload_id] = record

    return record


def get_upload(upload_id: str) -> UploadRecord:
    with STATE_LOCK:
        record = STATE.uploads.get(upload_id)
        if not record:
            raise ValueError("Upload not found.")
        return record


def preview_schema(upload_id: str) -> UploadRecord:
    """Return the upload record for schema preview."""

    return get_upload(upload_id)


def commit_upload(upload_id: str, mapping: Sequence[dict[str, str]]) -> UploadRecord:
    """Validate the mapping and mark upload as accepted."""

    record = get_upload(upload_id)

    csv_columns = {col.name for col in record.columns}
    if not mapping:
        raise ValueError("Mapping must contain at least one column.")
    mapped_cols = set()
    has_time = False
    has_metric = False

    for entry in mapping:
        column = entry.get("csv_col")
        logical = entry.get("logical_field", "")
        dtype = entry.get("dtype", "")
        if column not in csv_columns:
            raise ValueError(f"Column '{column}' not found in upload.")
        mapped_cols.add(column)

        lower_logical = logical.lower()
        if "time" in lower_logical or "date" in lower_logical:
            has_time = True
        if dtype in {"float", "integer", "metric"} or "metric" in lower_logical:
            has_metric = True

    if not has_time:
        raise ValueError("At least one column must be mapped as a time field.")
    if not has_metric:
        raise ValueError("At least one column must be mapped as a metric.")

    domains.update_schema(record.domain_id, record.schema_hash)
    clients.set_state(record.client_id, ClientState.SYNCING)

    with STATE_LOCK:
        record.status = "accepted"

    return record


