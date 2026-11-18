# Flag Hopping After Sanctions

An examination of post-designation flag changes among 663 vessels on the UK Sanctions List, using two releases of Global Fishing Watch's Global Vessel Identity dataset (v4.0 and v5.0).

## The Question

Article 91 of the United Nations Convention on the Law of the Sea (UNCLOS) requires a genuine link between a ship and the state whose flag it flies. Yet the Convention does not define that link in detail or establish a clear mechanism for verifying it.

This project examines what happens to vessels after they are designated under the UK Sanctions List. Do they subsequently appear under different flags in their AIS identity records? How soon do those changes appear? And what happens when different vessel identities are reported over overlapping periods?

The project also examines whether these findings change when the same vessels are analysed using different releases of Global Fishing Watch's vessel identity dataset.

## What it does

The analysis begins with the UK Sanctions List and identifies 663 unique vessels using their IMO numbers. Each IMO number is then used to retrieve the vessel's identity history from Global Fishing Watch (GFW).

For each vessel, the analysis establishes a baseline flag at the date of designation. It then identifies the earliest valid AIS identity record beginning strictly after that date and reporting a different flag.

Each candidate is checked against other AIS identity records for overlapping periods in which a different flag or SSVID is reported. Only overlaps with a positive duration are counted.

Each candidate is also compared with GFW registry identity records. A match requires the same IMO number, SSVID and flag, together with an overlapping identity period. Registry-owner records are excluded.

The same analysis is performed independently on GFW's Global Vessel Identity dataset v4.0 and v5.0. Comparing the results makes it possible to identify changes in the flags reported, the timing of candidate changes and the classification of individual vessels.

The IMO number remains the primary identifier throughout the analysis, allowing vessel histories to be compared even where names, flags or other identity details differ.

## Findings

The analysis identified 391 candidate post-designation flag changes in GFW v4.0 and 408 in v5.0. The difference reflects changes in the identity records available across the two releases, rather than necessarily indicating new real-world flag changes.

The classifications were as follows:

| Classification | GFW v4.0 | GFW v5.0 |
|---|---:|---:|
| AIS-only candidate, no detected overlapping identity conflict | 220 | 223 |
| Registry-correlated candidate, no competing AIS identity | 13 | 13 |
| Candidate registry-correlated but competing AIS identity present | 5 | 5 |
| Conflicting AIS identity, no exact candidate registry match | 153 | 167 |
| No different post-designation flag observed | 256 | 239 |
| Ambiguous baseline | 15 | 15 |
| Insufficient baseline | 1 | 1 |
| **Total vessels** | **663** | **663** |
| **Candidate classifications** | **391** | **408** |

A total of 24 vessels changed classification between the two releases. Eighteen vessels moved from having no observed different post-designation flag in v4.0 to having a candidate in v5.0. Five candidates previously classified as AIS-only were reclassified because v5.0 contained an overlapping competing identity. One candidate identified in v4.0 was no longer identified in v5.0.

The difference is not limited to the number of candidates. The number of vessels classified as having conflicting AIS identities without an exact registry match increased from 153 in v4.0 to 167 in v5.0. This illustrates why the version of an identity dataset matters: changes to historical records can affect not only whether a candidate is identified, but also how consistent its reported identity appears.

These findings concern AIS identity records and their classification. They should not be read as a count of legally completed flag transfers.

## Worked example

Wisdoms Daughter (IMO 9332834) was designated by the UK on 24 February 2025 while its recorded flag was Gabon.

Eighteen days later, its identity appeared under Panama. Subsequent records associated the vessel with Djibouti, Palau, Gambia, Sierra Leone and Equatorial Guinea. Over the same period, the vessel was also recorded under different names, including Sooraj and Mystery.

The IMO number provides the link across these records, allowing the vessel's reported identity to be followed despite changes in its name and flag. The sequence illustrates how quickly a vessel's AIS-reported identity can change after designation, and why tracking vessels by name or flag alone can produce an incomplete history.

These records show changes in reported identity. They do not, by themselves, establish when or whether the vessel's legal registration changed.

## Running it

The comparison script analyses the previously retrieved Global Fishing Watch identity records for both dataset versions.

From the project root, run:

```bash
python3 compare_gfw_versions.py
```

The script reads the raw JSON responses from `gfw_refresh/raw_json/` and `gfw_refresh_v5/raw_json/`, applies the classification rules independently to each dataset version and generates the vessel-level analysis and comparison files in `comparison_v4_v5/`.

The raw responses must be available in their respective directories before running the comparison.

## Files

| File or directory | Purpose |
|---|---|
| `uk_sanctions.csv` | Source UK Sanctions List data |
| `gfw_refresh/` | GFW v4.0 data retrieval files and raw API responses |
| `gfw_refresh_v5/` | GFW v5.0 data retrieval files and raw API responses |
| `comparison_v4_v5/` | Clean sanctions lookup, version-specific analysis results and comparison outputs |
| `compare_gfw_versions.py` | Applies the classification rules to both GFW versions and compares the results |
| `METHODOLOGY.md` | Explains the research design, data preparation, classification rules and limitations |
| `README.md` | Project overview, findings and instructions |

The principal analysis outputs are:

| Output | Purpose |
|---|---|
| `comparison_v4_v5/sanctions_lookup.csv` | One consolidated sanctions record for each of the 663 IMO numbers |
| `comparison_v4_v5/analysis_v4.0.csv` | Vessel-level classifications using GFW v4.0 |
| `comparison_v4_v5/analysis_v5.0.csv` | Vessel-level classifications using GFW v5.0 |
| `comparison_v4_v5/comparison_v4_v5.csv` | Comparison of classifications and candidate identities across both releases |

## Limitations

The analysis identifies changes in AIS-reported vessel identity. It does not establish that a vessel legally changed its registration or nationality. A different AIS-reported flag may reflect a genuine registration change, an administrative update, an inaccurate broadcast or an error in the underlying data.

An overlapping identity record indicates that different vessel identities were reported during the same period. It does not establish why the records overlap or whether the vessel deliberately manipulated its identity. Similarly, a match with GFW registry information provides additional identity evidence but does not, by itself, establish the legal validity of a vessel's registration.

The dates used in the analysis are those recorded in GFW's identity histories. They indicate when a particular identity was reported as valid in the dataset, not necessarily when a legal registration took effect. The calculated time between designation and an observed flag change should therefore be interpreted with this distinction in mind.

The comparison is also limited by the scope and quality of the available data. Differences between v4.0 and v5.0 may result from additions or revisions to historical records. They do not necessarily represent new events involving the vessels.

Finally, the sample covers vessels identified through the UK Sanctions List. The findings should not automatically be generalised to vessels sanctioned by other jurisdictions or to the wider global shipping fleet.

The full research design, classification rules and methodological limitations are set out in `METHODOLOGY.md`.

## Data sources

**UK Sanctions List**

https://www.gov.uk/government/publications/the-uk-sanctions-list

Published by the Foreign, Commonwealth and Development Office. The analysis uses the list dated 28 August 2026.

**Global Fishing Watch**

https://globalfishingwatch.org/our-apis/

The analysis uses two releases of the Global Vessel Identity dataset:

- `public-global-vessel-identity:v4.0`
- `public-global-vessel-identity:v5.0`

Both datasets were retrieved on 11 November 2026. The same 663 IMO numbers were queried against each release.

GFW data is used under its applicable data terms and licence conditions. This project is an independent research exercise.
