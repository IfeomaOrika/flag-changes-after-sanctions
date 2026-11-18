GFW IDENTITY REFRESH — STEP-BY-STEP

PURPOSE
This is a separate data retrieval step. It does not modify flag_hops.csv, results.json,
or any of your existing project files. It retrieves full AIS self-reported identity
records and registry-derived identity records for the 663 unique IMO numbers in
uk_sanctions.csv.

IMPORTANT
- Do not send your GFW API token to anyone, including ChatGPT.
- Keep the token in your local .env file.
- The script writes new files into gfw_refresh/ and raw_json/.
- The first run uses GFW dataset v4.0 to make comparison with the September 2026
  project snapshot more meaningful. We will separately compare v5.0.
- GFW's API terms describe the API as available for non-commercial purposes. Check
  the applicable terms before using the data for commercial work.

STEP 1 — PUT THE SCRIPT IN YOUR PROJECT FOLDER
Copy refresh_gfw_identity.py into the same folder as uk_sanctions.csv and .env.

STEP 2 — CHECK YOUR .env FILE
Your .env file should contain this line (with your own token):

GFW_TOKEN=PASTE_YOUR_OWN_TOKEN_HERE

Do not paste your real token into this chat or commit .env to GitHub.
Your existing .gitignore already excludes .env.

STEP 3 — INSTALL THE TWO PYTHON PACKAGES
Open Terminal in the project folder and run:

python -m pip install requests python-dotenv

STEP 4 — TEST FIVE VESSELS FIRST
Run:

python refresh_gfw_identity.py --limit 5

If the command succeeds, a new gfw_refresh folder should appear. It should contain:
- manifest.json
- self_reported_identity.csv
- registry_identity.csv
- registry_owners.csv
- registry_authorizations.csv
- errors.csv
- raw_json/ (one raw API response per IMO)

STEP 5 — SEND ME THE TEST OUTPUT
Do not run all 663 yet. First, send me the contents of manifest.json and tell me
whether errors.csv contains any rows. Do not send your .env file or API token.

AFTER THE TEST
I will check that the API response contains the expected fields and that the
registry records can be matched to the correct vessel and date. Only then will
we run the full 663-vessel retrieval.

DATASET VERSION
Default: public-global-vessel-identity:v4.0
To run the separate v5.0 comparison later:

python refresh_gfw_identity.py --dataset public-global-vessel-identity:v5.0 --output gfw_refresh_v5

Do not merge v4.0 and v5.0 outputs. Keep them separate and record their manifests.
