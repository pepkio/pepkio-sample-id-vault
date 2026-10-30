# Sample ID Vault

Browser-based sample pseudonymization and de-identification engine for generating short, unique sample codes and secure local key vaults in life science research.

# Overview

Modern biomedical and clinical research requires rigorous management of patient confidentiality, participant privacy, and specimen tracking. When handling biological specimens, clinical trial samples, genomic datasets, or biobank aliquots, researchers must remove personally identifiable information (PII) and protected health information (PHI) before downstream processing, sequencing, or data sharing. However, traditional manual methods for sample de-identification—such as ad-hoc spreadsheets or sequential numbering—often introduce security risks, data entry errors, key loss, and potential re-identification vulnerabilities.

The **Sample ID Vault** (also known as `pepkio-sample-id-vault`) solves these challenges by providing a secure, browser-based and programmatic engine for sample pseudonymization, specimen de-identification, and key vault management. Designed for life science researchers, bioinformaticians, clinical trial coordinators, and laboratory technicians, the tool generates short, human-readable, collision-resistant pseudonym identifiers using human-friendly Crockford Base32 encoding or irreversible HMAC-SHA256 cryptographic hashing.

In the browser, Sample ID Vault executes 100% client-side, ensuring that sensitive subject names, medical record numbers (MRNs), or sample manifests never leave the user's local machine. Master re-identification keys are stored in a password-protected local vault encrypted with AES-256-GCM and key stretching via PBKDF2 (100,000 iterations). For automated computational pipelines, the Python package provides direct REST API integration with structured JSON outputs.

The hosted [Sample ID Vault](https://www.pepkio.com/tools/sample-id-vault) web application runs directly in the browser with no installation or user account required. Source code and Python client updates are maintained at [github.com/pepkio/pepkio-sample-id-vault](https://github.com/pepkio/pepkio-sample-id-vault).

Common search terms and alternative terminology for this tool include sample pseudonymization software, biological specimen de-identification, biobank sample anonymizer, IRB sample ID generator, HIPAA sample de-identification tool, Crockford Base32 ID generator, clinical trial sample blinding, sample manifest anonymization, and bioinformatic specimen code vault.

# Features

- **Reversible & Irreversible Pseudonymization:** Choose between reversible mapping (with secure local vault key storage for audit re-identification) and irreversible one-way cryptographic hashing (HMAC-SHA256) for open data publishing.
- **Crockford Base32 Code Generation:** Generates 6-character or 8-character alphanumeric IDs that exclude visually ambiguous characters (`0`, `O`, `1`, `I`, `L`) and prevent accidental offensive word formation.
- **Custom Prefixes & Study Salts:** Apply custom study prefixes (e.g., `PAT-`, `SAMP-`, `BIO-`) and cryptographic study salts to ensure unique, non-colliding IDs across different clinical cohorts or multi-center trials.
- **Zero-Knowledge Client-Side Encryption:** Web application uses AES-256-GCM encryption with PBKDF2 (100,000 SHA-256 iterations) to store master lookup vaults entirely in browser `localStorage`. Sensitive sample names are never transmitted to cloud servers.
- **CSV Column Auto-Mapping & Validation:** Upload sample manifests or metadata tables in CSV format; the tool automatically detects candidate sample identifier columns and validates row counts.
- **De-Identified Dataset Export:** Export processed CSV files where original sample names are replaced with pseudonym IDs while preserving non-identifying metadata (e.g., age, sex, tissue type, treatment arm, sequencing metrics).
- **Batch Re-Identification Lookup:** Perform rapid reverse lookup on pseudonymized IDs using password-authenticated key vaults or exported key CSV files.
- **Encrypted Vault Backup & Migration:** Export and import password-encrypted `.vault` backup files to enable secure cross-workstation transfers or long-term archival storage.
- **IRB & GDPR Compliance Audit Logging:** Generate structured JSON/CSV audit logs recording vault metadata, creation timestamps, parameter configurations, and total entry counts for institutional compliance reviews.
- **Python Client & CLI:** Complete Python client (`pepkio-sample-id-vault`) and command-line interface supporting batch script execution, pipeline integration, and automated CI/CD workflows.

# Common Use Cases

- **Clinical Trial Specimen Blinding:** Blind patient biospecimens before transferring blood, tissue, or serum samples to reference laboratories or core facilities for testing.
- **Biobank & Biorepository Sample Cataloging:** Assign uniform, short, human-readable IDs to biological aliquots stored in liquid nitrogen or ultra-low freezers while maintaining a central encrypted key vault.
- **NGS Sample Sheet De-Identification:** Anonymize fastq metadata and sample sheets prior to uploading sequencing runs to public archives (NCBI SRA, ENA, GEO) or multi-institutional repositories.
- **Double-Blind Randomized Controlled Studies:** Generate randomized, non-sequential sample IDs for drug treatment and placebo cohorts to prevent investigator bias during assays and histological scoring.
- **Multi-Center Collaborative Cohorts:** Combine sample data from multiple clinical centers using site-specific study salts to avoid ID collisions without sharing sensitive master patient registers across sites.
- **Open Science & Supplementary Data Publishing:** Replace internal sample nomenclature with irreversible cryptographic hashes in published supplementary tables and open datasets.

# Why This Tool Exists

Life science laboratories frequently struggle with managing sample identification safely and efficiently:

1. **Risks of Spreadsheet Formula Pseudonymization:** Researchers often use Microsoft Excel or Google Sheets formulas (such as `RAND()`, `CONCATENATE()`, or simple row index offsets) to generate sample codes. These methods lack cryptographic randomness, create duplicate ID collisions in large cohorts, and leave sensitive master keys unencrypted on shared network drives.
2. **Accidental Exposure of Sensitive Data:** Storing raw patient identifiers alongside genomic or phenotypic data creates significant HIPAA and GDPR compliance risks. Inadvertent sharing of unencrypted spreadsheets during collaborations can result in data breaches.
3. **Transcription & Readability Errors:** Standard UUIDs or 32-character MD5 hashes are excessively long for physical tube labeling, pipette work, and manual transcription. Conversely, sequential numbers (e.g., `Sample1`, `Sample2`) expose sample order and invite guessing or unblinding in blinded studies.
4. **Third-Party Cloud Security Concerns:** Many web-based utilities upload user data to third-party servers for processing, which violates strict institutional review board (IRB) data privacy policies for protected health information.

The [Sample ID Vault web application](https://www.pepkio.com/tools/sample-id-vault) addresses these limitations by performing all cryptographic operations, vault encryption, and CSV transformations client-side within the web browser. For programmatic workflows, the official Python library provides authenticated API endpoints, consistent error handling, and structured data models.

# Installation

Install the official Python package from PyPI using `pip`:

```bash
pip install pepkio-sample-id-vault
```

Alternatively, install using `uv`:

```bash
uv add pepkio-sample-id-vault
```

The package is available on PyPI at [pypi.org/project/pepkio-sample-id-vault/](https://pypi.org/project/pepkio-sample-id-vault/).

# Quick Start

## Python Client Usage

Use `PepkioClient` to interact programmatically with the Sample ID Vault engine:

```python
import os
from pepkio_sample_id_vault import PepkioClient

# Initialize client (uses PEPKIO_API_KEY environment variable by default)
api_key = os.getenv("PEPKIO_API_KEY", "your_api_key_here")

with PepkioClient(api_key=api_key) as client:
    # Fetch tool manifest
    manifest = client.get_manifest()
    print("Tool Title:", manifest.get("title"))

    # Generate reversible 6-character Crockford Base32 sample IDs
    sample_names = "Patient-101\nPatient-102\nControl-A\nControl-B"
    run_input = {
        "action": "generate",
        "names_text": sample_names,
        "mode": "reversible",
        "id_length": 6,
        "prefix": "PAT-",
        "study_salt": "cohort_2026_oncology"
    }

    result = client.run(run_input)
    
    print("Status:", result.status)
    print("Skipped Blank Lines:", result.result.get("skipped_blank"))
    
    # Iterate through generated pseudonym rows
    for row in result.result.get("rows", []):
        print(f"Original: {row['name']} -> Pseudonym: {row['id']} (Status: {row['status']})")
```

## Irreversible Hashing Example

To perform one-way anonymization for public data sharing:

```python
from pepkio_sample_id_vault import PepkioClient

with PepkioClient(api_key="your_api_key_here") as client:
    result = client.run({
        "action": "generate",
        "names_text": "Biospecimen-Alpha\nBiospecimen-Beta",
        "mode": "irreversible",
        "study_salt": "public_release_salt_v1",
        "prefix": "ANON-"
    })
    
    for row in result.result.get("rows", []):
        print(f"Original Name: {row['name']} -> One-Way Hash ID: {row['id']}")
```

## Command-Line Interface (CLI)

The package includes a command-line tool `pepkio-sample-id-vault`:

```bash
# Fetch and print tool manifest
pepkio-sample-id-vault manifest

# List available example inputs
pepkio-sample-id-vault manifest --examples

# Run a built-in manifest example
pepkio-sample-id-vault run --example generate_reversible

# Run with custom JSON payload
pepkio-sample-id-vault run --input-json '{
  "action": "generate",
  "names_text": "Sample_01\nSample_02\nSample_03",
  "mode": "reversible",
  "id_length": 6,
  "prefix": "SAMP-",
  "study_salt": "lab_experiment_42"
}'
```

# Example Output

The API returns a structured JSON envelope containing the `run_id`, execution `status`, calculated `result`, and execution metadata.

### Input JSON (`action: "generate", mode: "reversible"`):

```json
{
  "action": "generate",
  "names_text": "Patient-001 Smith\nPatient-002 Jones\nControl-Alpha\n",
  "id_length": 6,
  "prefix": "PAT-",
  "study_salt": "demo-study-salt-2026",
  "mode": "reversible"
}
```

### Output JSON Response:

```json
{
  "run_id": "run_a8f9c2d1b3e4",
  "status": "completed",
  "result": {
    "rows": [
      {
        "name": "Patient-001 Smith",
        "id": "PAT-HSWFQZ",
        "status": "new"
      },
      {
        "name": "Patient-002 Jones",
        "id": "PAT-3K8M9P",
        "status": "new"
      },
      {
        "name": "Control-Alpha",
        "id": "PAT-V4N7R2",
        "status": "new"
      }
    ],
    "skipped_blank": 0
  },
  "error": null,
  "result_url": "https://tools.pepkio.com/api/tools/v1/runs/run_a8f9c2d1b3e4",
  "permalink": "https://tools.pepkio.com/r/run_a8f9c2d1b3e4"
}
```

### Action Capabilities Summary Table

| Action | Mode Support | Required Inputs | Primary Output | Use Case |
| --- | --- | --- | --- | --- |
| `generate` | Reversible / Irreversible | `names_text`, `id_length`, `prefix`, `study_salt` | `rows` array (`name`, `id`, `status`) | Generate pseudonym IDs from sample list |
| `lookup` | Reversible | `lookup_ids`, `vault` object | `rows` array (`id`, `name`, `found`) | Re-identify sample IDs using key vault |
| `parse_csv` | Both | `csv_text` | `headers`, `row_count`, `suggested_name_column` | Validate CSV manifest before processing |
| `build_key_csv` | Reversible | `id_by_name` mapping | CSV text file mapping names to IDs | Export secure master re-identification key |
| `build_deidentified_csv` | Both | `csv_text`, `name_column`, `id_by_name` | De-identified CSV string with masked IDs | Prepare dataset for research data sharing |
| `build_audit_log` | Reversible / Irreversible | `vault` object | JSON/CSV compliance record | Generate IRB/GDPR compliance logs |

# Scientific Background

## Regulatory Context: Pseudonymization vs Anonymization

In biomedical research and healthcare compliance, data protection standards clearly distinguish between pseudonymized and anonymized data:

- **Pseudonymization (GDPR Article 4(5)):** The processing of personal data in such a manner that the data can no longer be attributed to a specific data subject without the use of additional information. This additional information (the key vault) must be kept separately and subject to technical and organizational measures. Reversible mode in Sample ID Vault satisfies GDPR pseudonymization criteria by isolating the master key vault in password-encrypted local storage.
- **De-Identification (HIPAA Safe Harbor 45 CFR § 164.514(b)(2)):** Removal of 18 specific categories of direct and indirect identifiers (including names, medical record numbers, social security numbers, and precise dates). Irreversible mode provides cryptographic de-identification suitable for public dataset distribution.

## Crockford Base32 Encoding

For physical specimen tubes and microplates, generated IDs must be short, legible, and resistant to human reading errors. Sample ID Vault employs **Crockford Base32** encoding, created by Douglas Crockford. Crockford Base32 uses a 32-character symbol set consisting of uppercase digits and letters:

\[
\mathcal{S} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, \text{A}, \text{B}, \text{C}, \text{D}, \text{E}, \text{F}, \text{G}, \text{H}, \text{J}, \text{K}, \text{M}, \text{N}, \text{P}, \text{Q}, \text{R}, \text{S}, \text{T}, \text{V}, \text{W}, \text{X}, \text{Y}, \text{Z}\}
\]

### Key Scientific Advantages over Standard Base64 or Hexadecimal:
1. **Exclusion of Ambiguous Symbols:** The letters `I`, `L`, and `O` are excluded to avoid confusion with digits `1` and `0`. The letter `U` is excluded to prevent accidental formation of offensive English words.
2. **Case Insensitivity:** Decoding accepts both lowercase and uppercase characters, allowing researchers to read or transcribe labels without case errors.
3. **High Information Density:** A 6-character Crockford Base32 string encodes \(32^6 = 1,073,741,824\) unique combinations (\(> 10^9\)), providing ample space for large sample repositories while remaining brief enough for cryogenic tube labels.

## Cryptographic Study Salts and Collision Resistance

To prevent dictionary attacks, rainbow table lookups, and cross-study sample matching, Sample ID Vault incorporates a user-defined **Study Salt** (\(S\)) into the hash calculation.

For an input sample name \(N\), prefix \(P\), study salt \(S\), and cryptographic hash function \(H\):

\[
\text{Raw Hash} = H(S \parallel N \parallel S)
\]

where \(\parallel\) denotes string concatenation.

The raw bytes of the hash are subsequently mapped into Crockford Base32 representation and prepended with prefix \(P\). 

### Collision Probability Mathematics:

The probability \(P_{\text{collision}}\) of experiencing at least one ID collision among \(k\) sample names drawn from an ID space of size \(N_{\text{space}} = 32^L\) (where \(L\) is the ID character length) is approximated by the Birthday Problem formula:

\[
P_{\text{collision}} \approx 1 - \exp\left( -\frac{k(k - 1)}{2 \times N_{\text{space}}} \right)
\]

For a cohort of \(k = 10,000\) samples using a 6-character Crockford Base32 ID length (\(N_{\text{space}} \approx 1.07 \times 10^9\)):

\[
P_{\text{collision}} \approx 1 - \exp\left( -\frac{10^4 \times 10^4}{2 \times 1.07 \times 10^9} \right) \approx 1 - \exp(-0.0467) \approx 0.0456 \quad (4.56\%)
\]

To eliminate potential collisions, Sample ID Vault dynamically detects duplicate hash outputs within a cohort and increments an internal nonce counter to guarantee 100% unique ID assignment across all processed rows.

## Client-Side Zero-Knowledge Encryption Architecture

When using the web application, sample keys and vault registers are encrypted locally using **AES-256-GCM** (Advanced Encryption Standard in Galois/Counter Mode).

1. **Key Derivation (PBKDF2):** The user's vault master password is passed through Password-Based Key Derivation Function 2 (PBKDF2) using SHA-256 with 100,000 iterations and a cryptographically secure random 16-byte salt:
   \[
   K_{\text{AES}} = \text{PBKDF2}\left(\text{Password}, \text{Salt}_{\text{vault}}, \text{iterations}=100000, \text{key\_len}=256 \text{ bits}\right)
   \]
2. **Authenticated Encryption (AES-GCM):** The vault JSON payload is encrypted with \(K_{\text{AES}}\) using a random 12-byte initialization vector (IV). AES-GCM provides both confidentiality and data integrity authentication.
3. **Local Persistence:** Encrypted payloads are stored in the browser's `localStorage`. Decryption occurs exclusively in browser memory when the user inputs their master password.

# Frequently Asked Questions

### What is sample pseudonymization in life science research?
Sample pseudonymization is the process of replacing sensitive sample identifiers (such as patient names, medical record numbers, or personal details) with artificial identifiers or pseudonyms. This allows researchers to analyze biological specimens and clinical data without exposing participant identity, while maintaining a secure key to re-identify samples if necessary for clinical oversight or safety audits.

### How does sample de-identification differ from full anonymization?
Pseudonymization is a reversible process where original identifiers are replaced by unique codes, but a master key vault is retained in encrypted storage to permit authorized re-identification. Full anonymization (irreversible mode) permanently destroys the relationship between the sample and the subject, making reverse lookup mathematically impossible.

### What is Crockford Base32 encoding and why is it used for biospecimen IDs?
Crockford Base32 is a human-friendly character encoding system that uses 32 digits and uppercase letters. It excludes visually ambiguous characters (`0`, `O`, `1`, `I`, `L`) and the letter `U` to prevent reading errors on tube labels, microplates, and manual laboratory logs while maximizing character density.

### What is a study salt and why is it required for generating sample IDs?
A study salt is a secret or study-specific string mixed into the cryptographic hash calculation. It ensures that the same sample name produces entirely different pseudonym IDs across different clinical studies or institutions, preventing unauthorized cross-study matching and protecting against rainbow table attacks.

### How do I anonymize a CSV dataset for open data sharing or publication?
Use the `build_deidentified_csv` action in the Python API or upload your CSV to the web application. Select the sample identifier column; the tool replaces that column with generated pseudonym IDs (or irreversible hashes) while leaving all research data columns (e.g., gene expression, assay values, age, group) intact.

### How does HMAC-SHA256 hashing ensure irreversible sample de-identification?
In irreversible mode, Sample ID Vault computes a Keyed-Hash Message Authentication Code using SHA-256 (HMAC-SHA256) combined with your study salt. Because cryptographic hash functions are one-way mathematical functions, the original sample name cannot be calculated from the output hash.

### How can I re-identify sample IDs back to original subject names for clinical audits?
Re-identification is performed using the `lookup` action or the web vault interface. By supplying the generated pseudonym IDs alongside the password-authenticated key vault or master key CSV, authorized personnel can retrieve the original subject names.

### Is sample data uploaded to external servers when using Sample ID Vault?
No. In the web application at [pepkio.com/tools/sample-id-vault](https://www.pepkio.com/tools/sample-id-vault), all sample name processing, pseudonym generation, and vault encryption occur 100% client-side within your web browser using JavaScript. No raw sample names or master passwords are ever transmitted across the network.

### How does AES-256-GCM client-side encryption protect master key vaults?
The web vault encrypts sample registers using AES-256-GCM encryption key derived from your master password via PBKDF2 with 100,000 iterations of SHA-256. This authenticated encryption standard ensures that even if someone accesses your browser local storage or exported `.vault` file, they cannot read sample names without your master password.

### How do I handle sample ID generation for double-blind clinical studies?
Generate pseudonym IDs using reversible mode with a 6-character Crockford Base32 format and export the master key CSV to an independent data safety monitoring board (DSMB) or unblinded trial coordinator. Researchers conducting assays receive only the blinded sample IDs.

### What are the HIPAA Safe Harbor requirements for sample de-identification?
The HIPAA Privacy Rule Safe Harbor standard (45 CFR § 164.514(b)(2)) requires removing 18 explicit categories of health information identifiers, including patient names, geographic subdivisions, dates, and medical record numbers. Sample ID Vault removes direct sample names and replaces them with random or hashed pseudonyms compliant with Safe Harbor guidelines.

### How do I integrate sample ID pseudonymization into Python bioinformatic pipelines?
Install `pepkio-sample-id-vault` via `pip` or `uv`, initialize `PepkioClient`, and call `client.run()` with your sample list and parameters. The resulting JSON payload provides structured sample rows that can be converted directly into pandas DataFrames or fed into downstream analysis scripts.

### What is the difference between 6-character and 8-character pseudonym IDs?
A 6-character Crockford Base32 string provides over 1.07 billion unique ID combinations (\(32^6\)), suitable for most laboratory sample collections up to tens of thousands of aliquots. An 8-character ID string provides over 1.09 trillion unique combinations (\(32^8\)), recommended for large biorepositories, national biobanks, or high-throughput multi-center studies.

### How do I export an encrypted `.vault` backup file?
In the web application, click the "Export Vault Backup" button after generating or unlocking your vault. This downloads a password-encrypted `.vault` file containing your encrypted sample registers and study salt configuration, which can be safely stored on secure drives or transferred to another workstation.

### Can Sample ID Vault generate audit logs for IRB compliance reviews?
Yes. The `build_audit_log` action generates a formal compliance record in JSON or CSV format detailing vault metadata, total sample counts, salt parameters, creation dates, and encryption standards for submission to Institutional Review Boards (IRB) or ethics committees.

### Does Sample ID Vault enforce unique ID generation across duplicate sample names?
When multiple rows contain identical original sample names within the same run, Sample ID Vault assigns the exact same pseudonym ID to ensure internal consistency across replicates. If distinct sample names yield a hash collision, the algorithm automatically resolves the collision by applying an incremental nonce.

# Web Application

The hosted version of [Sample ID Vault](https://www.pepkio.com/tools/sample-id-vault) provides an interactive web interface for zero-knowledge sample de-identification and key management directly in the browser.

The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

Key web application features include:
- **Zero-Knowledge Local Storage:** Password-protected local vault encrypted via AES-256-GCM with PBKDF2 key stretching. Sample names never leave your browser.
- **Interactive CSV Column Mapper:** Drag-and-drop CSV importer with automated identifier column detection and live preview.
- **Printable Master Key Worksheets:** Formatted key management templates for clinical audit binders and laboratory records.
- **Encrypted Backup Import/Export:** Download and restore `.vault` backup files across workstations.
- **Shareable State Links:** Generate secure permalinks for tool configuration state without exposing underlying master key data.

Web Application:
https://www.pepkio.com/tools/sample-id-vault

# Related Resources

GitHub Repository:
https://github.com/pepkio/pepkio-sample-id-vault

PyPI Package:
https://pypi.org/project/pepkio-sample-id-vault/

Web Application:
https://www.pepkio.com/tools/sample-id-vault

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Scientific capabilities include:
- RNA-seq analysis
- Single-cell RNA-seq analysis
- Spatial transcriptomics analysis
- Functional enrichment analysis
- Custom bioinformatics workflows

Website:
https://www.pepkio.com/

# Citation

If you use Sample ID Vault or `pepkio-sample-id-vault` in published research, clinical trials, or software pipelines, please cite the tool using the following format:

### Plain Text Citation
Pepkio. Sample ID Vault: Browser-Based Sample Pseudonymization and De-Identification Engine for Life Science Research. (2026). Available at: https://www.pepkio.com/tools/sample-id-vault

### BibTeX Entry
```bibtex
@software{pepkio_sample_id_vault_2026,
  author = {{Pepkio}},
  title = {Sample ID Vault: Browser-Based Sample Pseudonymization and De-Identification Engine for Life Science Research},
  year = {2026},
  url = {https://www.pepkio.com/tools/sample-id-vault},
  note = {Software available from https://github.com/pepkio/pepkio-sample-id-vault}
}
```

# License

Distributed under the terms of the MIT License. See the repository for complete license details.

# Keywords

sample pseudonymization, sample de-identification, specimen anonymization, biospecimen de-identification, sample ID vault, Pepkio Sample ID Vault, pepkio-sample-id-vault, Crockford Base32 generator, IRB compliance tool, HIPAA sample de-identification, clinical trial sample blinding, biobank sample anonymizer, sample key vault, sample lookup vault, HMAC-SHA256 sample hashing, study salt generator, sample de-identification CSV mapper, de-identified CSV export, biospecimen cataloging, sample tracking software, laboratory sample pseudonym, double-blind sample randomization, AES-256-GCM sample vault, zero-knowledge sample de-identification, patient sample masking, NGS sample sheet anonymization, sample ID generator Python, bioinformatic sample privacy, sample re-identification lookup, clinical trial specimen tracking, sample code generator, specimen de-identification tool, sample privacy software, IRB audit log generator, sample blinding calculator, how to pseudonymize clinical samples, how to de-identify sample names in CSV, Crockford Base32 sample ID collision probability, difference between pseudonymization and anonymization GDPR, HIPAA Safe Harbor sample de-identification rules, client-side AES-256-GCM local storage encryption, irreversible HMAC-SHA256 sample hashing Python, biobank sample key vault management, double-blind clinical trial sample ID generator, batch sample re-identification lookup tool, export de-identified CSV for open data sharing, multi-center study sample tracking with study salt, generate Crockford Base32 codes for sample tubes, Python library for sample de-identification API
