# Pepkio Sample ID Vault

A Python package and client library for programmatic specimen pseudonymization, HIPAA/GDPR-compliant de-identification, and secure sample identifier mapping using Crockford Base32 codes and HMAC-SHA256 hashing.

# What It Does

The `pepkio-sample-id-vault` package provides Python tools to automate biological sample pseudonymization, specimen de-identification, and key vault management. It enables laboratory scientists, bioinformaticians, and clinical researchers to replace sensitive patient names, medical record numbers (MRNs), or sample identifiers with short, collision-resistant Crockford Base32 pseudonyms or one-way cryptographic hashes. The library supports batch manifest de-identification, custom study prefixes, salt-based hashing, and reversible lookup workflows via secure key vaults.

# Features

- **Reversible Pseudonymization & Re-Identification:** Generate traceable sample pseudonyms paired with secure local key vaults for audit re-identification.
- **Irreversible Cryptographic Hashing:** Anonymize datasets using HMAC-SHA256 one-way hashing for open-access data publishing and public archives.
- **Human-Friendly Crockford Base32 IDs:** Create compact 6- or 8-character codes excluding ambiguous characters (`0`, `O`, `1`, `I`, `L`) to eliminate manual reading and transcription errors on tube labels.
- **Custom Study Prefixes & Salts:** Prevent cross-study ID collisions in multi-center clinical trials by combining study-specific salts with custom prefixes (e.g., `PAT-`, `SAMP-`).
- **CSV Manifest De-Identification:** Automatically parse sample spreadsheets, detect candidate identifier columns, replace sensitive names, and export de-identified CSV files.
- **REST API & CLI Interface:** Automate sample pseudonymization within Python bioinformatic pipelines or command-line execution workflows.

# Installation

Install the package from PyPI using `pip`:

```bash
pip install pepkio-sample-id-vault
```

Or using `uv`:

```bash
uv add pepkio-sample-id-vault
```

# Quick Example

```python
import os
from pepkio_sample_id_vault import PepkioClient

# Initialize client using PEPKIO_API_KEY environment variable
api_key = os.getenv("PEPKIO_API_KEY", "your_api_key_here")

with PepkioClient(api_key=api_key) as client:
    # Generate reversible 6-character Crockford Base32 sample pseudonyms
    run_input = {
        "action": "generate",
        "names_text": "Patient-101\nPatient-102\nControl-A\nControl-B",
        "mode": "reversible",
        "id_length": 6,
        "prefix": "PAT-",
        "study_salt": "cohort_2026_oncology"
    }

    result = client.run(run_input)

    print("Execution Status:", result.status)
    for row in result.result.get("rows", []):
        print(f"Original: {row['name']} -> Pseudonym: {row['id']} ({row['status']})")
```

# Typical Use Cases

- **Clinical Trial Specimen Blinding:** Blind patient biospecimen labels before shipping blood, tissue, or serum samples to core facilities or reference laboratories.
- **Biobank & Biorepository Cataloging:** Assign compact, uniform Crockford Base32 codes to aliquots in cryogenic storage while maintaining encrypted master lookup records.
- **NGS Sample Sheet De-Identification:** Remove protected health information (PHI/PII) from FASTQ metadata and sample manifests prior to public repository upload (NCBI SRA, ENA, GEO).
- **Double-Blind Study Randomization:** Generate non-sequential, non-predictable sample pseudonyms to eliminate investigator bias during assays and histological scoring.
- **Multi-Center Cohort Harmonization:** Merge specimen manifests across multiple sites using site-specific study salts to avoid ID collisions without sharing raw patient registries.

# Scientific Background

- **Pseudonymization vs. Anonymization:** Pseudonymization replaces direct identifiers with artificial codes while storing a segregated master key for authorized re-identification (GDPR Article 4(5)). Anonymization permanently severs the relationship between subject and sample (HIPAA Safe Harbor 45 CFR § 164.514(b)(2)).
- **Crockford Base32 Encoding:** Crockford Base32 uses 32 uppercase digits and letters, excluding visually ambiguous characters (`0`, `O`, `1`, `I`, `L`) and `U`. A 6-character string provides over 1.07 billion unique combinations (\(32^6\)), offering high symbol density for cryotubes and microplates.
- **Cryptographic Salts & Nonce Collision Handling:** Adding a study salt to HMAC-SHA256 hashing prevents cross-study re-identification and rainbow table attacks. Internal nonces dynamically resolve hash collisions within cohorts.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/sample-id-vault

Key web-only features include zero-knowledge client-side AES-256-GCM local storage encryption, interactive CSV column auto-mapping, printable master key worksheets, and encrypted `.vault` backup file export/import.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-sample-id-vault

Web Application: https://www.pepkio.com/tools/sample-id-vault

Source code and issue tracking: https://github.com/pepkio/pepkio-sample-id-vault

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro). See https://www.pepkio.com for additional tools and computational workflows.

# Keywords

* sample pseudonymization
* specimen de-identification
* sample ID vault
* Pepkio Sample ID Vault
* pepkio-sample-id-vault
* Crockford Base32
* HIPAA de-identification
* GDPR compliance
* biobank anonymizer
* clinical trial blinding
* HMAC-SHA256 hashing
* sample manifest
* sample tracking
* biospecimen cataloging
* double-blind randomization
* sample key vault
* de-identified CSV
* study salt
* sample anonymization
* NGS sample sheet
* sample re-identification
* biospecimen privacy
* sample code generator
* IRB audit log
* sample privacy
* laboratory sample code
* python package for sample pseudonymization
* how to de-identify sample names in CSV
* Crockford Base32 sample code generator
* double blind clinical trial sample blinding
* HIPAA safe harbor sample de-identification tool
* zero knowledge client side AES-256-GCM vault
* batch sample re-identification lookup python
* irreversible HMAC-SHA256 sample hashing python
* export de-identified CSV for open data sharing
* multi center clinical trial sample tracking with study salt
* generate Crockford Base32 codes for cryotubes
* biobank sample key vault management python
