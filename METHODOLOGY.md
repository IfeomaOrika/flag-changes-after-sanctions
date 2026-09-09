# Methodology

## 1. Research design
This project asks whether ships sanctioned by the United Kingdom change their flag afterwards and how quickly those changes become visible.

I measured the time between each ship’s designation date and the first time Global Fishing Watch (GFW) recorded the same ship under a different flag. I identified ships by their IMO number, which stays with the vessel even when its name, owner, manager, or flag changes.

Each ship contributes one observation: the time between designation and its first observed flag change, where a change occurred.

The analysis is descriptive. It shows what happened to the ships after designation and measures how quickly those changes appeared in the data. It does not establish why an individual ship changed its flag.

## 2. What counts as a flag change

I counted a flag change when GFW recorded the same IMO number under a different reported flag after the ship's designation date.

The measure comes from GFW's vessel identity data and reflects the flag associated with the vessel in that data. It does not establish the date of legal registration, a change in ownership or management, or the ship's physical location at the time.

For each ship, I recorded the flag before designation, the first different flag after designation, the date GFW first recorded that flag, the number of days between designation and the recorded change, and GFW's source classification for the new flag.

## 3. Why I recorded the first change
I recorded only the first flag change after designation for each ship.
Wisdom's Daughter, for example, changed flag eight times after February 2025. It counts once in this analysis.

Counting every change would give ships that changed flags repeatedly more weight in the results. I wanted each ship to contribute equally and wanted the measure to answer one simple question: how quickly did a sanctioned ship first appear under a different flag?

Later changes can also have different causes. They may follow port refusals, insurance problems, further sanctions, or other pressure that developed after the original designation. The first observed change is therefore the clearest point for measuring the ship's initial response.

## 4. IMO numbers

The International Maritime Organization (IMO) is the United Nations agency responsible for international shipping regulation. It assigns ships permanent seven-digit IMO numbers, which remain with the vessel throughout its life.
The number stays the same when a ship is sold, renamed, or reflagged. That makes it possible to follow the same vessel across different names and flags.
I used the IMO number to match the UK sanctions records with GFW identity histories and to make sure I was following the same vessel over time.

## 5. Study population

The UK sanctions list contains individuals, companies, and other entities alongside designated vessels. I kept entries with a valid seven-digit IMO number because the research requires a reliable way to follow a vessel before and after designation.

I deduplicated repeated entries and aliases using the IMO number.

This produced 663 unique sanctioned vessels.

I excluded entries without a valid IMO number because a vessel name alone is not reliable enough for this analysis. Ships can change names, and different vessels can have the same or similar names.

## 6. Designation date

I used the date on which the UK government officially designated each vessel as the starting point for the analysis. The date came from the Date Designated field in the UK Sanctions List.

This date creates the boundary between the pre-designation and post-designation periods.

For example, a vessel designated on 24 February 2025 has observations before that date treated as pre-designation. Changes recorded after that date are potential post-designation responses.

## 7. Days to first flag change

I calculated days-to-hop as the number of calendar days between the designation date and the first date GFW recorded the same IMO number under a different flag.

The measure tells me when the change became visible in GFW data. It does not give me the exact date on which the legal registration was completed.

This matters because the legal process behind a flag transfer can begin before the change appears in AIS or GFW. A ship may also spend time without transmitting after changing its flag, which would make the observed interval longer than the actual interval.

The fastest changes in the dataset appear one to three days after designation. A complete flag transfer would normally involve steps such as deregistration, an application to the new flag state, documentation, and the issue or transfer of certificates. 

A change appearing one day after designation therefore strongly suggests that the new flag arrangement was already underway or had already been completed when the designation became public.

There is another possibility: GFW's recorded date may not match the date of the underlying legal event. That can happen with individual records, which is why I treat the GFW date as the observation date rather than assuming it is the legal registration date.

## 8. Self-reported and registry-confirmed flags

GFW assigns a source to each vessel identity record.

Where GFW identifies a flag through a registry record, I classify the flag as registry-confirmed. Where the flag appears in the vessel's reported identity without corresponding registry confirmation in GFW, I classify it as self-reported.

There were 404 post-designation flag changes in this dataset. 37 were registry-confirmed, and 367 were self-reported only. That is 90.8% of observed flag changes for which GFW holds no registry confirmation of the new flag.

For those records, I cannot establish from GFW alone that the vessel obtained legal registration from the new flag state. There are at least two possible explanations. The registry may hold a record that GFW cannot access or match, or the vessel may have reported a flag that it had not been granted.

I therefore keep self-reported and registry-confirmed flags separate throughout the analysis.

A self-reported flag raises a separate question from the speed of the change: whether the vessel held a valid flag at all. Establishing that for any individual vessel would require checking the relevant registry directly or obtaining other evidence of registration. At this scale, though, the proportion is a finding in its own right. Article 91 of UNCLOS requires a genuine link between a vessel and its flag state. For 367 of the 404 changes observed here, the publicly available data does not establish that any link exists, genuine or otherwise.

## 9. Ships with no observed flag change

Of the 663 ships, 404 showed a flag change after designation. The remaining 259 required a closer look.
239 continued to appear in the data after designation under the same flag. 

Most of these vessels were North Korean-flagged. Their lack of reflagging is significant because it shows that flag hopping depends on having another registry willing or able to take the vessel.

For vessels operating under flags with few or no viable alternatives, sanctions may leave them with little opportunity to change nationality. The absence of a flag change therefore does not necessarily mean that a vessel faced no pressure or had no reason to change. In some cases, the option may simply have been unavailable.

The other 20 vessels stopped appearing around the time of designation. Because their subsequent activity could not be observed, I cannot determine whether they changed flags, stopped transmitting, were scrapped, were seized, or left the observable dataset for another reason.

I therefore treat these 20 vessels as unresolved rather than as vessels that kept their flags.

This leaves 643 observable vessels for the main comparison. Of those, 404 showed a post-designation flag change.
404 ÷ 643 = 62.8%.

I report the 20 unresolved vessels separately rather than treating them as evidence of either a flag change or no change.

## 10. What the data cannot show


The data shows what happened to the vessels after designation. It cannot, by itself, tell me why a particular vessel changed its flag.

A post-sanction flag change could be connected to sanctions evasion. It could also follow deregistration by the original flag state, a sale of the vessel, a change in commercial arrangements, or a routine registration event that happened to fall after designation.

AIS and vessel identity data cannot distinguish between these explanations.
Establishing intent for an individual vessel would require evidence from outside this dataset, such as ownership records, registry applications, registration dates, sale documents, insurance records or communications between vessel owners and registries.
The dataset does show a clear pattern: 404 vessels recorded a post-designation flag change, 107 did so within 30 days, 273 within 90 days, and the median time to the first observed change was 55 days.

That pattern is consistent with a systematic response to sanctions designation.

There are two further limitations. First, the dataset covers UK sanctions only. Adding US and EU sanctions could produce a larger sample and could change the results. Second, GFW relies heavily on AIS-derived information. Ships can stop transmitting or manipulate their broadcasts, and GFW notes that its data can contain errors.

For that reason, I treat individual records with caution. The main finding rests on the pattern across the full dataset rather than on any single vessel.

