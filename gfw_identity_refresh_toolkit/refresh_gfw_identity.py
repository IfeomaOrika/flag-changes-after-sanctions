#!/usr/bin/env python3
"""Refresh GFW vessel identity and registry records for the UK-sanctioned vessel list.

This script does NOT overwrite the original project data. It writes raw API responses
and flattened CSVs into a separate output directory.

Required environment variable: GFW_TOKEN
Optional: GFW_DATASET (default: public-global-vessel-identity:v4.0)

Usage:
  python refresh_gfw_identity.py --limit 5       # test first five unique IMOs
  python refresh_gfw_identity.py                 # process all unique IMOs
  python refresh_gfw_identity.py --dataset public-global-vessel-identity:v5.0
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

API_URL = "https://gateway.api.globalfishingwatch.org/v3/vessels/search"
DEFAULT_DATASET = "public-global-vessel-identity:v4.0"
PAGE_SIZE = 50
TIMEOUT = 60


def safe_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value)


def read_sanctioned_vessels(path: Path) -> list[dict[str, str]]:
    """Read the UK Sanctions List CSV, whose first row is a report-date note."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        first = next(reader, None)
        second = next(reader, None)
        if not second or "IMO number" not in second:
            raise ValueError(
                "Could not locate the 'IMO number' header on the second row of "
                f"{path}. First row was: {first!r}"
            )
        headers = second
        imo_index = headers.index("IMO number")
        name_indices = [headers.index(f"Name {n}") for n in range(1, 7) if f"Name {n}" in headers]
        date_index = headers.index("Date Designated") if "Date Designated" in headers else None
        flag_index = headers.index("Current believed flag of ship") if "Current believed flag of ship" in headers else None
        records: dict[str, dict[str, str]] = {}
        for row in reader:
            if len(row) <= imo_index:
                continue
            imo_raw = (row[imo_index] or "").strip()
            imo = re.sub(r"(?i)^IMO\s*", "", imo_raw).strip()
            if not imo or not imo.isdigit():
                continue
            sanctions_name = ""
            for name_index in name_indices:
                if len(row) > name_index and row[name_index].strip():
                    sanctions_name = row[name_index].strip()
                    break
            records.setdefault(imo, {
                "imo": imo,
                "sanctions_name": sanctions_name,
                "date_designated": row[date_index].strip() if date_index is not None and len(row) > date_index else "",
                "uk_current_believed_flag": row[flag_index].strip() if flag_index is not None and len(row) > flag_index else "",
            })
    return list(records.values())


def request_page(
    session: requests.Session,
    token: str,
    imo: str,
    dataset: str,
    since: str | None = None,
) -> dict[str, Any]:
    params = {
        "query": imo,
        "datasets[0]": dataset,
        "limit": PAGE_SIZE,
        "includes[0]": "OWNERSHIP",
        "includes[1]": "AUTHORIZATIONS",
    }

    if since:
        params["since"] = since

    headers = {"Authorization": f"Bearer {token}"}
    last_error: Exception | None = None

    for attempt in range(5):
        try:
            response = session.get(
                API_URL,
                params=params,
                headers=headers,
                timeout=TIMEOUT,
            )

            if response.status_code == 429 or response.status_code >= 500:
                wait = min(30, 2 ** attempt)
                print(
                    f"  HTTP {response.status_code}; retrying in {wait}s",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue

            response.raise_for_status()
            return response.json()

        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            wait = min(30, 2 ** attempt)
            if attempt < 4:
                time.sleep(wait)

    raise RuntimeError(
        f"GFW request failed for IMO {imo}: {last_error}"
    )


def fetch_all_pages(
    session: requests.Session,
    token: str,
    imo: str,
    dataset: str,
) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    total: int | None = None
    since: str | None = None
    seen_cursors: set[str] = set()

    while True:
        page = request_page(session, token, imo, dataset, since)
        page_entries = page.get("entries", []) or []
        entries.extend(page_entries)

        if total is None:
            total = page.get("total")

        next_since = page.get("since")

        if (
            not next_since
            or not page_entries
            or next_since in seen_cursors
            or (total is not None and len(entries) >= total)
        ):
            break

        seen_cursors.add(next_since)
        since = next_since

    return {
        "dataset_requested": dataset,
        "query_imo": imo,
        "total_reported": total,
        "entries": entries,
    }


def flatten_entry(imo: str, entry_index: int, entry: dict[str, Any], section: str, records: list[dict[str, Any]]) -> None:
    values = entry.get(section, []) or []
    if isinstance(values, dict):
        values = [values]
    for item_index, item in enumerate(values):
        if not isinstance(item, dict):
            continue
        row: dict[str, Any] = {
            "query_imo": imo,
            "entry_index": entry_index,
            "entry_dataset": entry.get("dataset", ""),
            "entry_registry_info_total_records": entry.get("registryInfoTotalRecords", ""),
            "record_section": section,
            "record_index": item_index,
        }
        for key, value in item.items():
            row[key] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
        records.append(row)


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        path.write_text("", encoding="utf-8")
        return
    columns: list[str] = []
    seen = set()
    for row in records:
        for key in row:
            if key not in seen:
                seen.add(key)
                columns.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Refresh GFW AIS and registry identity records.")
    parser.add_argument("--input", default="uk_sanctions.csv", help="UK sanctions CSV path")
    parser.add_argument("--output", default="gfw_refresh", help="Separate output directory")
    parser.add_argument("--dataset", default=os.getenv("GFW_DATASET", DEFAULT_DATASET), help="GFW identity dataset")
    parser.add_argument("--limit", type=int, default=0, help="Only process first N unique IMOs (0 = all)")
    parser.add_argument("--pause", type=float, default=0.25, help="Pause between vessel searches")
    args = parser.parse_args()

    token = os.getenv("GFW_TOKEN")
    if not token:
        print("ERROR: GFW_TOKEN is not set. Add it to your local .env file; do not share it.", file=sys.stderr)
        return 2

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Cannot find {input_path}. Run this script from the project folder or pass --input.", file=sys.stderr)
        return 2

    vessels = read_sanctioned_vessels(input_path)
    if args.limit > 0:
        vessels = vessels[:args.limit]
    output_dir = Path(args.output)
    raw_dir = output_dir / "raw_json"
    raw_dir.mkdir(parents=True, exist_ok=True)

    started = datetime.now(timezone.utc)
    session = requests.Session()
    self_reported_rows: list[dict[str, Any]] = []
    registry_rows: list[dict[str, Any]] = []
    owner_rows: list[dict[str, Any]] = []
    authorization_rows: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    print(f"Dataset: {args.dataset}")
    print(f"Unique IMO numbers to query: {len(vessels)}")
    print(f"Output: {output_dir.resolve()}")

    for index, vessel in enumerate(vessels, start=1):
        imo = vessel["imo"]
        print(f"[{index}/{len(vessels)}] IMO {imo} — {vessel.get('sanctions_name', '')}")
        try:
            payload = fetch_all_pages(session, token, imo, args.dataset)
            payload["sanctions_record"] = vessel
            payload["retrieved_at_utc"] = datetime.now(timezone.utc).isoformat()
            (raw_dir / f"{imo}.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            for entry_index, entry in enumerate(payload.get("entries", [])):
                for section, target in (
                    ("selfReportedInfo", self_reported_rows),
                    ("registryInfo", registry_rows),
                    ("registryOwners", owner_rows),
                    ("registryPublicAuthorizations", authorization_rows),
                ):
                    flatten_entry(imo, entry_index, entry, section, target)
            time.sleep(max(0, args.pause))
        except Exception as exc:
            errors.append({"imo": imo, "sanctions_name": vessel.get("sanctions_name", ""), "error": str(exc)})
            print(f"  ERROR: {exc}", file=sys.stderr)

    write_csv(output_dir / "self_reported_identity.csv", self_reported_rows)
    write_csv(output_dir / "registry_identity.csv", registry_rows)
    write_csv(output_dir / "registry_owners.csv", owner_rows)
    write_csv(output_dir / "registry_authorizations.csv", authorization_rows)
    write_csv(output_dir / "errors.csv", errors)

    manifest = {
        "dataset_requested": args.dataset,
        "retrieved_at_utc_started": started.isoformat(),
        "retrieved_at_utc_finished": datetime.now(timezone.utc).isoformat(),
        "input_file": str(input_path),
        "unique_imos_requested": len(vessels),
        "successful_imo_queries": len(vessels) - len(errors),
        "failed_imo_queries": len(errors),
        "self_reported_identity_rows": len(self_reported_rows),
        "registry_identity_rows": len(registry_rows),
        "registry_owner_rows": len(owner_rows),
        "registry_authorization_rows": len(authorization_rows),
        "note": "Raw responses are preserved per IMO. Registry records must be matched by IMO/SSVID/record identifiers and overlapping dates; do not treat registryInfoTotalRecords > 0 as confirmation of every AIS-reported flag.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("\nRefresh complete.")
    print(json.dumps(manifest, indent=2))
    if errors:
        print(f"\n{len(errors)} queries failed. See {output_dir / 'errors.csv'}.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
