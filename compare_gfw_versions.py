import csv
import json
from pathlib import Path
from datetime import datetime, date
from collections import Counter

BASE = Path(".")
OUT = BASE / "comparison_v4_v5"
OUT.mkdir(exist_ok=True)

VERSIONS = {
    "v4.0": BASE / "gfw_refresh" / "raw_json",
    "v5.0": BASE / "gfw_refresh_v5" / "raw_json",
}

EXPECTED = {
    "v4.0": "public-global-vessel-identity:v4.0",
    "v5.0": "public-global-vessel-identity:v5.0",
}


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def clean_imo(value):
    return "".join(c for c in str(value or "") if c.isdigit())


def overlaps(a, b):
    """Strict positive-duration overlap. Boundary contact is not overlap."""
    if a["start"] is None or b["start"] is None:
        return False

    if a["end"] is not None and a["end"] <= b["start"]:
        return False
    if b["end"] is not None and b["end"] <= a["start"]:
        return False

    return True


def load_lookup():
    path = OUT / "sanctions_lookup.csv"
    result = {}

    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            imo = clean_imo(row["imo"])
            designation = date.fromisoformat(row["designation_date"])

            if imo in result:
                raise ValueError(f"Duplicate sanctions lookup IMO: {imo}")

            result[imo] = {
                "imo": imo,
                "unique_id": row["unique_id"],
                "designation": designation,
                "current_flag": row["current_believed_flag"],
                "previous_flags": row["previous_flags"],
            }

    if len(result) != 663:
        raise ValueError(f"Expected 663 sanctions records, found {len(result)}")

    return result


def load_version(folder, expected_dataset):
    files = sorted(folder.glob("*.json"))

    if len(files) != 663:
        raise ValueError(f"{folder}: expected 663 JSON files, found {len(files)}")

    ais = {}
    registry = {}
    unreadable = 0
    wrong_version = []

    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:
            unreadable += 1
            print("UNREADABLE:", path, exc)
            continue

        if data.get("dataset_requested") != expected_dataset:
            wrong_version.append(path.name)

        query_imo = clean_imo(data.get("query_imo"))

        for entry in data.get("entries", []):
            for section, destination in [
                ("selfReportedInfo", ais),
                ("registryInfo", registry),
            ]:
                for record in entry.get(section) or []:
                    imo = clean_imo(record.get("imo")) or query_imo
                    flag = (record.get("flag") or "").strip()
                    ssvid = str(record.get("ssvid") or "").strip()

                    start = parse_dt(record.get("transmissionDateFrom"))
                    end = parse_dt(record.get("transmissionDateTo"))

                    # Records without a usable flag or start date
                    # cannot establish an identity interval.
                    if not imo or not flag or start is None:
                        continue

                    item = {
                        "imo": imo,
                        "flag": flag,
                        "ssvid": ssvid,
                        "start": start,
                        "end": end,
                        "id": str(record.get("id") or ""),
                    }

                    destination.setdefault(imo, {})[
                        (
                            item["id"], item["ssvid"], item["flag"],
                            item["start"], item["end"]
                        )
                    ] = item

    if unreadable:
        raise ValueError(f"{folder}: {unreadable} unreadable files")

    if wrong_version:
        raise ValueError(
            f"{folder}: unexpected dataset versions in {wrong_version[:5]}"
        )

    ais = {imo: list(records.values()) for imo, records in ais.items()}
    registry = {imo: list(records.values()) for imo, records in registry.items()}

    return ais, registry


def registry_matches(candidate, records):
    matches = []

    if not candidate["ssvid"]:
        return matches

    for record in records:
        if (
            record["imo"] == candidate["imo"]
            and record["ssvid"] == candidate["ssvid"]
            and record["flag"] == candidate["flag"]
            and overlaps(candidate, record)
        ):
            matches.append(record)

    return matches


def analyse_one(imo, sanctions, ais, registry):
    designation = sanctions["designation"]
    records = ais.get(imo, [])
    registry_records = registry.get(imo, [])

    # Valid identity records are already restricted to nonblank flags
    # and parseable start dates.
    covering = [
        r for r in records
        if r["start"].date() <= designation
        and (r["end"] is None or r["end"].date() >= designation)
    ]

    baseline_source = ""

    if covering:
        baseline_flags = sorted({r["flag"] for r in covering})

        if len(baseline_flags) != 1:
            return base_result(
                imo, sanctions, "ambiguous_baseline", "designation_date",
                "; ".join(baseline_flags)
            )

        baseline = baseline_flags[0]
        baseline_source = "designation_date"

    else:
        earlier = [
            r for r in records
            if r["end"] is not None and r["end"].date() < designation
        ]

        if not earlier:
            return base_result(
                imo, sanctions, "insufficient_baseline",
                "none", ""
            )

        latest_end = max(r["end"] for r in earlier)
        latest = [r for r in earlier if r["end"] == latest_end]
        latest_flags = sorted({r["flag"] for r in latest})

        if len(latest_flags) != 1:
            return base_result(
                imo, sanctions, "ambiguous_baseline",
                "latest_prior_record", "; ".join(latest_flags)
            )

        baseline = latest_flags[0]
        baseline_source = "latest_prior_record"

    candidates = [
        r for r in records
        if r["start"].date() > designation
        and r["flag"] != baseline
    ]

    if not candidates:
        result = base_result(
            imo, sanctions, "no_different_post_designation_flag_observed",
            baseline_source, baseline
        )
        return result

    earliest_start = min(r["start"] for r in candidates)
    earliest = [r for r in candidates if r["start"] == earliest_start]

    # Do not arbitrarily select between different flags or SSVIDs
    # appearing at the same earliest timestamp.
    candidate_pairs = sorted({
        (r["flag"], r["ssvid"]) for r in earliest
    })

    if len(candidate_pairs) > 1:
        result = base_result(
            imo, sanctions, "ambiguous_earliest_candidate",
            baseline_source, baseline
        )
        result["candidate_start"] = earliest_start.isoformat()
        result["candidate_options"] = " | ".join(
            f"{flag} [{ssvid}]" for flag, ssvid in candidate_pairs
        )
        return result

    candidate = earliest[0]

    conflicts = [
        r for r in records
        if r["flag"] != candidate["flag"]
        and overlaps(candidate, r)
    ]

    candidate_registry = registry_matches(candidate, registry_records)

    competing_registry = []
    for conflict in conflicts:
        competing_registry.extend(
            registry_matches(conflict, registry_records)
        )

    if conflicts and candidate_registry:
        classification = (
            "candidate_registry_correlated_but_competing_AIS_identity_present"
        )
    elif conflicts:
        classification = (
            "conflicting_AIS_identity_no_exact_candidate_registry_match"
        )
    elif candidate_registry:
        classification = (
            "registry_correlated_candidate_no_competing_AIS_identity"
        )
    else:
        classification = (
            "AIS_only_candidate_no_detected_overlapping_identity_conflict"
        )

    delay = (
        candidate["start"] -
        datetime.combine(designation, datetime.min.time(),
                         tzinfo=candidate["start"].tzinfo)
    ).total_seconds() / 86400

    result = base_result(
        imo, sanctions, classification, baseline_source, baseline
    )

    result.update({
        "candidate_flag": candidate["flag"],
        "candidate_ssvid": candidate["ssvid"],
        "candidate_start": candidate["start"].isoformat(),
        "candidate_end": (
            candidate["end"].isoformat() if candidate["end"] else ""
        ),
        "days_after_designation": round(delay, 4),
        "overlapping_conflict_count": len(conflicts),
        "candidate_registry_match_count": len(candidate_registry),
        "competing_registry_match_count": len(competing_registry),
        "competing_registry_supported": bool(competing_registry),
    })

    return result


def base_result(imo, sanctions, classification, baseline_source, baseline):
    return {
        "imo": imo,
        "unique_id": sanctions["unique_id"],
        "designation_date": sanctions["designation"].isoformat(),
        "sanctions_current_flag": sanctions["current_flag"],
        "sanctions_previous_flags": sanctions["previous_flags"],
        "classification": classification,
        "baseline_source": baseline_source,
        "baseline_flag": baseline,
        "candidate_flag": "",
        "candidate_ssvid": "",
        "candidate_start": "",
        "candidate_end": "",
        "days_after_designation": "",
        "overlapping_conflict_count": 0,
        "candidate_registry_match_count": 0,
        "competing_registry_match_count": 0,
        "competing_registry_supported": False,
        "candidate_options": "",
    }


def write_csv(path, rows):
    if not rows:
        return

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    sanctions = load_lookup()
    analyses = {}

    for version, folder in VERSIONS.items():
        print(f"\nLoading {version}...")
        ais, registry = load_version(folder, EXPECTED[version])

        results = [
            analyse_one(imo, record, ais, registry)
            for imo, record in sorted(sanctions.items())
        ]

        analyses[version] = {r["imo"]: r for r in results}

        write_csv(OUT / f"analysis_{version}.csv", results)

        counts = Counter(r["classification"] for r in results)

        print(f"{version} classifications:")
        for classification, count in sorted(counts.items()):
            print(f"  {classification}: {count}")

        candidates = [
            r for r in results if r["candidate_flag"]
        ]

        delays = [
            r["days_after_designation"]
            for r in candidates
            if r["days_after_designation"] != ""
        ]

        print("  Candidate records:", len(candidates))
        print("  Overlapping AIS conflicts:",
              sum(r["overlapping_conflict_count"] > 0 for r in candidates))
        print("  Candidate registry correlations:",
              sum(r["candidate_registry_match_count"] > 0 for r in candidates))
        print("  Competing-side registry support:",
              sum(r["competing_registry_supported"] for r in candidates))

        if delays:
            ordered = sorted(delays)
            middle = len(ordered) // 2
            median = (
                ordered[middle] if len(ordered) % 2
                else (ordered[middle - 1] + ordered[middle]) / 2
            )
            print("  Median days after designation:", round(median, 4))
            print("  Within 30 days:", sum(x <= 30 for x in delays))
            print("  Within 90 days:", sum(x <= 90 for x in delays))

    comparison = []

    for imo in sorted(sanctions):
        a = analyses["v4.0"][imo]
        b = analyses["v5.0"][imo]

        comparison.append({
            "imo": imo,
            "unique_id": a["unique_id"],
            "v4_classification": a["classification"],
            "v5_classification": b["classification"],
            "classification_changed": (
                a["classification"] != b["classification"]
            ),
            "v4_baseline_flag": a["baseline_flag"],
            "v5_baseline_flag": b["baseline_flag"],
            "v4_candidate_flag": a["candidate_flag"],
            "v5_candidate_flag": b["candidate_flag"],
            "candidate_flag_changed": (
                a["candidate_flag"] != b["candidate_flag"]
            ),
            "v4_candidate_ssvid": a["candidate_ssvid"],
            "v5_candidate_ssvid": b["candidate_ssvid"],
            "candidate_ssvid_changed": (
                a["candidate_ssvid"] != b["candidate_ssvid"]
            ),
            "v4_candidate_start": a["candidate_start"],
            "v5_candidate_start": b["candidate_start"],
            "v4_registry_matches": a["candidate_registry_match_count"],
            "v5_registry_matches": b["candidate_registry_match_count"],
            "v4_conflicts": a["overlapping_conflict_count"],
            "v5_conflicts": b["overlapping_conflict_count"],
        })

    write_csv(OUT / "comparison_v4_v5.csv", comparison)

    print("\nCOMPARISON SUMMARY")
    print("Vessels compared:", len(comparison))
    print("Classification changes:",
          sum(r["classification_changed"] for r in comparison))
    print("Candidate flag differences:",
          sum(r["candidate_flag_changed"] for r in comparison))
    print("Candidate SSVID differences:",
          sum(r["candidate_ssvid_changed"] for r in comparison))

    print("\nOUTPUT FILES")
    for name in [
        "analysis_v4.0.csv",
        "analysis_v5.0.csv",
        "comparison_v4_v5.csv",
    ]:
        print(OUT / name)


if __name__ == "__main__":
    main()
