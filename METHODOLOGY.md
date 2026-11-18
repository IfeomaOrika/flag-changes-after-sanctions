# Methodology

## 1. Research design

This project examines the flag histories of 663 vessels listed under the UK Sanctions List. Using data from Global Fishing Watch (GFW), it investigates whether these vessels appeared under different flags in their Automatic Identification System (AIS) identity records after being sanctioned. It also examines instances where different vessel identities appeared to exist at the same time.

The analysis compares two releases of GFW's Global Vessel Identity dataset, v4.0 and v5.0, to determine whether differences between the datasets affect the identification and classification of these cases.

The project focuses on changes in AIS-reported identity. Such changes are not, on their own, proof that a vessel's legal registration or nationality changed.

## 2. Data sources

The analysis uses the UK Sanctions List, dated 28 August 2026, and two releases of the GFW Global Vessel Identity dataset: v4.0 and v5.0.

Both GFW versions were queried using the same 663 IMO numbers. All 663 queries were successful in each version. The v4.0 data were retrieved on 11 November 2026 between 18:40:56 and 18:55:11 UTC, while v5.0 was retrieved on the same date between 21:24:38 and 21:50:14 UTC.

## 3. Preparation of the sanctions data

The UK Sanctions List contained 888 entries relating to 663 unique IMO numbers. Since the IMO number provides a consistent identifier for matching vessels across the different datasets, it was used as the primary identifier for the analysis.

Duplicate entries were consolidated to produce one record per IMO number, retaining the relevant designation details and flag information.

## 4. Establishing the baseline flag

The flag recorded for each vessel at the date of its designation was used as the baseline for identifying subsequent flag changes. The baseline was established using the following rules:

- A single distinct flag recorded across the designation date was adopted as the baseline.
- Where multiple distinct flags covered the designation date, the baseline was classified as ambiguous.
- Where no record covered the designation date, the most recent valid record before that date was used as a provisional baseline.
- Where no earlier record was available, the vessel was classified as having insufficient baseline information.

## 5. Identifying post-designation flag changes

A candidate flag change was identified where a valid AIS identity record beginning strictly after the designation date reported a flag different from the vessel's baseline flag. Where multiple qualifying records existed, the earliest was selected as the candidate.

The time between designation and the start of the candidate record was also calculated. Vessels without a qualifying record were classified as having no different post-designation flag observed.

## 6. Identifying competing AIS identities

Each candidate was checked for overlap with other AIS identity records reporting a different flag or SSVID. An overlap was recorded only where the identity intervals shared a positive duration; records that met only at an endpoint were excluded.

Where an overlap existed, the candidate was classified as having a competing AIS identity. This indicates conflicting identity information in the dataset but does not establish the cause of the conflict.

## 7. Registry correlation

Candidate AIS identities were compared with GFW registry identity records to determine whether corresponding registry evidence existed.

A registry record was considered a match only where it shared the candidate's IMO number, SSVID and flag, and its identity period overlapped the candidate's AIS record. Registry-owner records were excluded, and the mere presence of registry information was not treated as confirmation of a candidate flag.

## 8. Classification framework

Each vessel was assigned one of seven classifications based on its baseline, candidate flag, competing AIS identities and registry evidence:

- **AIS-only candidate, no detected overlapping identity conflict:** A different post-designation flag was identified, but no competing identity or exact registry match was found.
- **Registry-correlated candidate, no competing AIS identity:** The candidate had an exact registry match, with no competing identity detected.
- **Candidate registry-correlated but competing AIS identity present:** The candidate had an exact registry match, but another identity overlapped its record.
- **Conflicting AIS identity, no exact candidate registry match:** A competing identity was detected, but no exact registry match for the candidate was found.
- **No different post-designation flag observed:** No qualifying change from the baseline was identified.
- **Ambiguous baseline:** Multiple distinct flags covered the designation date.
- **Insufficient baseline:** No valid record was available to establish a baseline.

## 9. Comparing GFW versions

The same sanctions lookup and classification rules were applied independently to v4.0 and v5.0. The resulting vessel-level records were then compared to identify changes in classification, candidate flag, SSVID and candidate record date.

This comparison showed whether v5.0 introduced new candidates, identified different candidates for previously analysed vessels or no longer supported candidates found in v4.0.

## 10. Limitations

AIS identity records do not establish a vessel's legal registration or nationality. A different AIS-reported flag is therefore treated as a candidate change, not proof of legal re-registration.

Similarly, competing AIS identities indicate inconsistencies in the available records but do not establish their cause or demonstrate deliberate identity manipulation.

The absence of a candidate does not prove that a vessel never changed flags. It means that no qualifying change was identified in the available data. In addition, differences between v4.0 and v5.0 may reflect additions or revisions to historical identity records rather than new real-world events.

## 11. Results

The final classifications for the two GFW releases were as follows:

| Classification | GFW v4.0 | GFW v5.0 |
|---|---:|---:|
| AIS-only candidate, no detected overlapping identity conflict | 220 | 223 |
| Candidate registry-correlated but competing AIS identity present | 5 | 5 |
| Conflicting AIS identity, no exact candidate registry match | 153 | 167 |
| Registry-correlated candidate, no competing AIS identity | 13 | 13 |
| No different post-designation flag observed | 256 | 239 |
| Ambiguous baseline | 15 | 15 |
| Insufficient baseline | 1 | 1 |
| **Total vessels** | **663** | **663** |
| **Total candidate classifications** | **391** | **408** |

GFW v5.0 produced 408 candidate classifications, compared with 391 in v4.0. A total of 24 vessels changed classification between the two releases. The comparison demonstrates that the choice of dataset version affects the identification and classification of candidate post-designation flag changes.
