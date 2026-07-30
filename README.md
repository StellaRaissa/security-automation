# Security Automation Platform (Python)

A hands-on Python project that automates repetitive security-analyst tasks. It is the
**automation counterpart** to my [Mini SOC Lab](https://github.com/StellaRaissa/mini-soc-project):
that project focuses on *detecting* threats (Wazuh HIDS + Suricata NIDS); this one focuses
on *automating the analysis* of what those tools produce.

> **Status:** Phase 1 complete — two working tools (IOC Checker, Log Analyzer).
> Further modules are on the roadmap below.

---

## Why this project

In a real SOC, analysts don't spend the day clicking through raw logs — they write small
scripts that triage and summarize data automatically. This project is my way of learning
Python by building exactly those kinds of tools, using real data from my own detection lab.

```
New event  →  Python  →  Parse  →  Classify  →  Report
```

---

## Tools built so far

### 1. IOC Checker (`ioc_checker.py`)

Checks a list of IP addresses against a blacklist of known Indicators of Compromise (IOCs)
and prints a summary report.

- Reads the known-threat list from `blacklist.txt`
- Reads the addresses to check from `a_verifier.txt`
- Compares each address and flags matches
- Prints a report with total addresses checked and threats detected

**Design choice:** data (the IP lists) is kept in external text files, fully separate from
the code. Adding new threats means editing `blacklist.txt` — never the Python source. This
is how real detection tools are structured.

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

**This is the link to the Mini SOC.** It reads the real `eve.json` alert file produced by
Suricata in my detection lab, parses the JSON, extracts the alerts, and writes a report.

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
Rapport sauvegarde dans rapport.txt
```

---

## Project structure

```
security-automation/
└── ioc-checker/
    ├── ioc_checker.py       # Tool 1: IOC blacklist matching
    ├── blacklist.txt        # Known malicious IPs (data)
    ├── a_verifier.txt       # IPs to check (data)
    ├── log_analyzer.py      # Tool 2: Suricata eve.json analyzer
    ├── eve.json             # Sample Suricata alert log (from the Mini SOC)
    └── rapport.txt          # Generated analysis report (output)
```

---

## How to run

Requires Python 3 (tested on Python 3.13, Kali Linux).

```bash
# Tool 1 — IOC Checker
python3 ioc_checker.py

# Tool 2 — Suricata Log Analyzer
python3 log_analyzer.py
```

No external dependencies — both tools use only the Python standard library (`json`).

---

## What I learned

Building these tools from scratch, I practiced the core Python concepts every security
script relies on:

- Variables, lists, and conditional logic (`if` / `else`)
- Loops (`for`) to process collections of data
- Reading from and writing to files (`open`, `read`, `write`, `splitlines`)
- Counting and summarizing results (`len`, counters, `str` conversion)
- Parsing JSON and accessing nested data by key (`json.loads`, `event["alert"]["signature"]`)
- Separating data from logic — a foundational design principle

---

## How it connects to the Mini SOC

| Mini SOC Lab (detection) | This project (automation) |
|--------------------------|----------------------------|
| Suricata generates `eve.json` alerts | Log Analyzer parses and summarizes them |
| Wazuh centralizes host + network events | IOC Checker models the enrichment/triage step |
| Manual investigation in the dashboard | Automated report generation |

Together they show the full workflow an analyst cares about: **detect → collect →
automate the analysis.**

---

## Roadmap

- [ ] **VirusTotal Scanner** — enrich IOCs by querying the VirusTotal API (`requests`)
- [ ] **Statistics** — count the most active source IPs in the Suricata logs
- [ ] **Timestamped reports** — add the run date/time to each generated report
- [ ] **Cross-tool triage** — feed Suricata source IPs into the IOC Checker automatically
- [ ] **Dashboard API** — expose results over a small FastAPI service

---

*Learning project — built step by step while studying Python, with the goal of developing
practical tooling for a cybersecurity Werkstudent role.*
