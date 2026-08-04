# Security Automation Platform (Python)

A hands-on Python project that automates repetitive security-analyst tasks. It is the
**automation counterpart** to my [Mini SOC Lab](https://github.com/StellaRaissa/mini-soc-project):
that project focuses on *detecting* threats (Wazuh HIDS + Suricata NIDS); this one focuses
on *automating the analysis* of what those tools produce.

> **Status:** Phase 1 complete — three working tools (IOC Checker, Log Analyzer,
> VirusTotal Scanner). Further modules are on the roadmap below.

---

## Why this project

In a real SOC, analysts don't spend the day clicking through raw logs — they write small
scripts that triage and summarize data automatically. This project is my way of learning
Python by building exactly those kinds of tools, using real data from my own detection lab.

```
New event  →  Python  →  Parse  →  Classify / Enrich  →  Report
```

---

## Tools built so far

### 1. IOC Checker (`ioc_checker.py`)

Checks a list of IP addresses against a **local** blacklist of known Indicators of
Compromise (IOCs) and prints a summary report.

- Reads the known-threat list from `blacklist.txt`
- Reads the addresses to check from `a_verifier.txt`
- Compares each address and flags matches
- Prints a report with total addresses checked and threats detected

**Design choice:** data (the IP lists) is kept in external text files, fully separate from
the code. Adding new threats means editing `blacklist.txt` — never the Python source.

Sample output:

```
=== Rapport de verification IOC ===
[OK]     8.8.8.8 est inconnue.
[ALERTE] 45.148.10.35 est malveillante !
[ALERTE] 1.1.1.1 est malveillante !
[ALERTE] 193.32.162.7 est malveillante !
===================================
Adresses verifiees : 4
Menaces detectees  : 3
```

### 2. Suricata Log Analyzer (`log_analyzer.py`)

Reads the real `eve.json` alert file produced by Suricata in my Mini SOC, parses the JSON,
extracts the alerts, and writes a report.

- Reads `eve.json` line by line
- Parses each line as JSON (`json.loads`)
- Keeps only entries where `event_type` is `alert`, ignoring `stats` / `flow` noise
- Extracts the source IP and the alert signature
- Prints the report **and** saves it to `rapport.txt` for archiving

Sample output (real alerts from an Nmap scan against the lab):

```
=== Analyse des logs Suricata ===
[ALERTE] 127.0.0.1 -> SURICATA STREAM Packet with invalid ack
[ALERTE] 127.0.0.1 -> SURICATA STREAM SHUTDOWN RST invalid ack
=================================
Alertes trouvees : 2
```

### 3. VirusTotal Scanner (`vt_scanner.py`)

Enriches IP addresses by querying the **VirusTotal API** — a global service that aggregates
~70 antivirus/security engines. Where the IOC Checker uses a small local list, this tool
consults worldwide threat intelligence.

- Reads the addresses to check from `a_verifier.txt` (same input as the IOC Checker)
- Sends an authenticated request to the VirusTotal API for each IP (`requests` library)
- Reads how many engines flagged the IP as malicious (`last_analysis_stats`)
- Waits 15 seconds between requests to respect the free-tier rate limit (4 requests/min)
- Flags any IP reported by one or more engines

Sample output:

```
=== Scan VirusTotal ===
[OK]     8.8.8.8 -> propre
[ALERTE] 45.148.10.35 -> 12 moteurs la signalent
[OK]     1.1.1.1 -> propre
[ALERTE] 193.32.162.7 -> 5 moteurs la signalent
=== Scan termine ===
```

**Why query many engines?** No single antivirus is perfect. Combining ~70 engines fills
individual blind spots, and the *number* of engines that flag an IP acts as a confidence
score — 1 detection may be a false positive, 12 is near-certain.

---

## API key security

The VirusTotal scanner needs an API key, which is a secret (like a password). It must never
be committed to GitHub.

- The real key lives in a local `config.py` file, imported by the code (`from config import API_KEY`).
- `config.py` is listed in `.gitignore`, so Git never uploads it.
- A `config.example.py` shows the structure so anyone cloning the project knows to create
  their own `config.py`.

To run the scanner yourself:

```bash
cp config.example.py config.py
# then edit config.py and paste your own VirusTotal API key
```

---

## Project structure

```
security-automation/
├── ioc_checker.py        # Tool 1: local IOC blacklist matching
├── log_analyzer.py       # Tool 2: Suricata eve.json analyzer
├── vt_scanner.py         # Tool 3: VirusTotal API enrichment
├── blacklist.txt         # Known malicious IPs (data)
├── a_verifier.txt        # IPs to check (shared input)
├── config.example.py     # Template for the API key file
├── config.py             # Your real API key — NOT in Git (gitignored)
├── eve.json              # Suricata alert log — NOT in Git (gitignored)
└── rapport.txt           # Generated report — NOT in Git (gitignored)
```

---

## How to run

Requires Python 3 (tested on Python 3.13, Kali Linux). Only `requests` is needed beyond the
standard library:

```bash
pip install requests

python3 ioc_checker.py     # local blacklist check
python3 log_analyzer.py    # analyze Suricata logs
python3 vt_scanner.py      # enrich via VirusTotal (needs config.py)
```

---

## What I learned

- Variables, lists, and conditional logic (`if` / `else`)
- Loops (`for`) to process collections of data
- Reading from and writing to files (`open`, `read`, `write`, `splitlines`)
- Parsing JSON and accessing nested data by key (`json.loads`, `data["attributes"]["last_analysis_stats"]`)
- Calling a real web API with authentication (`requests`, API keys, HTTP headers)
- Respecting API rate limits (`time.sleep`)
- Handling secrets safely (`config.py` + `.gitignore`, never committing an API key)
- Separating data from logic — a foundational design principle

---

## How it connects to the Mini SOC

| Mini SOC Lab (detection) | This project (automation) |
|--------------------------|----------------------------|
| Suricata generates `eve.json` alerts | Log Analyzer parses and summarizes them |
| Wazuh centralizes host + network events | IOC Checker + VirusTotal Scanner handle triage & enrichment |
| Manual investigation in the dashboard | Automated report generation |

Together they show the full workflow an analyst cares about: **detect → collect →
enrich → automate the analysis.**

---

## Roadmap

- [ ] **Statistics** — count the most active source IPs in the Suricata logs
- [ ] **Timestamped reports** — add the run date/time to each generated report
- [ ] **Cross-tool triage** — filter locally with the IOC Checker, then enrich only the
      unknown IPs via VirusTotal
- [ ] **Error handling** — wrap API calls in `try/except` for robustness
- [ ] **Dashboard API** — expose results over a small FastAPI service

---

*Learning project — built step by step while studying Python, with the goal of developing
practical tooling for a cybersecurity Werkstudent role.*
