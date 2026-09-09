# Flag Changes After Sanctions Designation

Measures how quickly vessels sanctioned by the United Kingdom appear under a different flag, using public sanctions records and Global Fishing Watch vessel identity data.

## The Question

Article 91 of UNCLOS requires a genuine link between a ship and the state whose flag it flies. The Convention does not define the requirement in detail or provide a clear mechanism for enforcing it.
This project asks what that looks like in practice.

When a ship is sanctioned, does it change flag? And how quickly does the change appear?

## What it does

I took the UK Sanctions List and kept every entry with a valid seven-digit IMO number. I then queried Global Fishing Watch (GFW) for each vessel's identity history.

For each ship, I recorded:

the flag before designation

the first different flag observed after designation

the number of days between designation and that change

whether GFW has registry confirmation for the new flag


Each ship counts once, based on its first observed flag change.

## Findings

The dataset contains 663 sanctioned vessels. Twenty stopped transmitting around their designation date and could not be followed afterwards, leaving 643 observable vessels.

404 of 643 (62.8%) appeared under a different flag after designation

107 changed within 30 days

273 changed within 90 days

Median time to the first observed change: 55 days

367 of the 404 (90.8%) new flags were self-reported only, with no registry confirmation in GFW

The fastest observed changes appeared one to three days after designation, shorter than the normal process for completing a flag transfer

New flags concentrated in a small group of registries, including Gambia, Sierra Leone, Comoros, Cameroon, Djibouti, Barbados and Equatorial Guinea

Taken together, the speed of the changes and the lack of registry confirmation point to the same conclusion: flag-state registration operates with very little external verification at exactly the point where verification would matter most.

The 239 vessels with no observed flag change were mostly North Korean flagged. Their lack of reflagging matters because flag hopping depends on having another registry willing to take the vessel. Where that option is unavailable, a ship cannot respond to sanctions by changing flag.

## Worked example

Wisdoms Daughter, IMO 9332834, was designated by the UK on 24 February 2025 while flying Gabon.

It appeared under Panama 18 days later, then Djibouti, Palau, Gambia, Sierra Leone and Equatorial Guinea in turn. As of August 2026, it transmits as Spessartin under a Russian flag. That is seven flag changes in eighteen months. It was also renamed twice during the same period, first to Sooraj and then to Mystery.

The vessel had already stopped being registry-confirmed before designation. Every identity record from January 2023 onwards is self-reported, including two earlier flags under Saint Kitts and Nevis and Mongolia. Its IMO number never changed, so the vessel can be followed through every name and flag in the sequence, and the designation continues to attach to it.

## Running it

Requires Python 3 and a Global Fishing Watch API token.
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv
echo "GFW_TOKEN=your_token_here" > .env

Download the UK Sanctions List CSV from gov.uk and save it as uk_sanctions.csv in the project root.

Then run:
python3 query_vessels.py
python3 save_results.py
python3 split_no_change.py

query_vessels.py queries GFW for each sanctioned vessel. It makes one API call per vessel with a half-second pause and takes roughly six minutes.

## Files

File
Purpose
query_vessels.py
Pulls sanctioned vessels and queries GFW for each
save_results.py
Calculates days to the first flag change and writes flag_hops.csv
split_no_change.py
Separates vessels that kept their flag from those that went silent
parse_vessel.py
Prints the full identity history for a single IMO
METHODOLOGY.md
Documents the decisions, definitions and limits behind the analysis
results.json
Raw GFW responses for all 663 vessels
flag_hops.csv
The 404 observed flag changes

## Limits

The data shows what vessels did after designation, not why they did it.

A flag change following a sanction is consistent with evasion. It can also follow deregistration by the original flag state, a sale, or a routine registration event that happened to fall in the same period. Establishing intent for an individual vessel would require evidence outside AIS data.

The dates in this analysis are the dates the changes became visible in GFW data. They are not necessarily the dates on which legal registration took place. The measured interval can therefore be longer than the actual time between the legal change and the designation.
The dataset covers UK sanctions only. Adding US and EU sanctions would produce a broader sample and could change the results.

GFW data is derived from AIS and other vessel information. Vessels can stop transmitting or manipulate their AIS broadcasts, and GFW states that its data may contain errors. Individual records therefore need to be treated with caution. The main finding rests on the pattern across the full dataset.

METHODOLOGY.md sets out the methodology and limitations in full.


## Data sources

UK Sanctions List 
​​https://www.gov.uk/government/publications/the-uk-sanctions-list 
Published by the Foreign, Commonwealth and Development Office.


Global Fishing Watch
https://globalfishingwatch.org/our-apis/ 
Powered by Global Fishing Watch. Dataset: public-global-vessel-identity:v4.0, accessed 2026-08-25. Used for non-commercial research under CC BY-NC 4.0.
