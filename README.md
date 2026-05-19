# AI-Powered SOC Alert Triage System

[![Python](https://img.shields.io/badge/Python-3.13+-blue)](https://python.org)
[![Claude](https://img.shields.io/badge/Anthropic-Claude%20API-orange)](https://anthropic.com)
[![Splunk](https://img.shields.io/badge/Splunk-Enterprise-green)](https://splunk.com)
[![MITRE](https://img.shields.io/badge/MITRE-ATT%26CK-red)](https://attack.mitre.org)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-purple)](https://kali.org)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

An AI-assisted SOC triage pipeline that automatically pulls live alerts from Splunk, sends each one to Claude for analysis, and returns structured severity ratings, MITRE ATT&CK mappings, and recommended actions — in seconds.

> **This project extends the [Phishing Detection Lab](https://github.com/cpt-ferna02/splunk-phishing-lab)** — feeding its live Splunk alerts into an AI triage engine.

---

## Screenshots

### 1. AI Triage System Running
[![Triage Running](screenshots/01-triage-running.png)](screenshots/01-triage-running.png)

### 2. Critical Alert — Submitted Data (Risk Score 9)
[![Critical Alert](screenshots/02-critical-alert.png)](screenshots/02-critical-alert.png)

### 3. Full Incident Report
[![Full Report](screenshots/03-full-report.png)](screenshots/03-full-report.png)

---

## The Problem

SOC analysts are buried in alerts. The average enterprise SOC receives thousands per day, and studies show over 40% go uninvestigated due to alert fatigue. Junior analysts spend most of their time on repetitive first-pass triage instead of actual investigation.

This project simulates an AI-assisted triage layer that eliminates that bottleneck — automatically classifying every alert, scoring risk, mapping to MITRE ATT&CK, and recommending a response action before a human ever looks at it.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    ATTACK LAYER                      │
│  GoPhish Campaign → Mailhog → Phishing Kill Chain   │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                  DETECTION LAYER                     │
│       Splunk SIEM (index=main source=gophish)       │
│  Email Sent | Opened | Clicked | Submitted Data     │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                    TRIAGE LAYER                      │
│            Python Triage Engine (triage.py)         │
│    Pulls alerts from Splunk REST API every run      │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                      AI LAYER                        │
│              Anthropic Claude API                    │
│  Input:  Raw alert data                             │
│  Output: Severity | Classification | MITRE |        │
│          Summary | Recommended Action | Risk Score  │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                   REPORTING LAYER                    │
│    triage_report.txt — full timestamped report      │
└─────────────────────────────────────────────────────┘
```

---

## How the AI Prompt Works

Each alert is sent to Claude with a structured prompt that enforces a consistent, parseable output format:

```python
prompt = f"""
You are a SOC analyst triaging a security alert.
Analyze this phishing detection alert and provide a structured assessment.

ALERT DATA:
- Time: {event.get('_time')}
- Event Type: {event.get('message')}
- Target Email: {event.get('email')}
- Details: {event.get('details')}

Provide your analysis in this EXACT format:

SEVERITY: [Critical/High/Medium/Low]
CLASSIFICATION: [True Positive/False Positive/Needs Investigation]
MITRE_TECHNIQUE: [technique ID and name]
SUMMARY: [one sentence summary]
RECOMMENDED_ACTION: [specific SOC action]
RISK_SCORE: [1-10]
"""
```

Enforcing a strict output schema in the prompt is the same technique used in production AI security pipelines — it makes the output machine-readable and automatable, not just human-readable.

---

## Sample AI Triage Output

```
============================================================
TRIAGE REPORT — 2026-05-06 16:23:13
============================================================
ORIGINAL ALERT:
  Time:       2026-05-06T06:16:08
  Event Type: Submitted Data
  Target:     john.smith@acme-corp.com

AI ANALYSIS:
SEVERITY: Critical
CLASSIFICATION: True Positive
MITRE_TECHNIQUE: T1566 / T1056.003 - Phishing / Web Portal Capture
SUMMARY: User john.smith@acme-corp.com submitted corporate credentials
to a suspected phishing portal, indicating successful credential harvesting.
RECOMMENDED_ACTION: Immediately force password reset for
john.smith@acme-corp.com, disable affected accounts pending investigation,
audit recent authentication logs for unauthorized access, check for lateral
movement or data exfiltration, and block phishing infrastructure.
RISK_SCORE: 9
============================================================
```

---

## AI Triage Results — Live Run

Results from a live run against 10 phishing alerts:

| Alert Type | AI Severity | Classification | Risk Score |
|------------|-------------|----------------|------------|
| Submitted Data | Critical | True Positive | 9/10 |
| Submitted Data | Critical | True Positive | 9/10 |
| Clicked Link | High | Needs Investigation | 7/10 |
| Clicked Link | High | Needs Investigation | 7/10 |
| Email Opened | High | Needs Investigation | 7/10 |
| Email Opened | High | Needs Investigation | 7/10 |
| Email Sent | Medium | Needs Investigation | 5/10 |
| Email Sent | Low | Needs Investigation | 3/10 |
| Campaign Created | Medium | Needs Investigation | 5/10 |
| Campaign Created | Low | Needs Investigation | 3/10 |

---

## MITRE ATT&CK Coverage

| Alert Type | Technique ID | Technique Name |
|------------|-------------|----------------|
| Submitted Data | T1566 / T1056.003 | Phishing / Web Portal Capture |
| Clicked Link | T1566.002 | Spearphishing Link |
| Email Opened | T1566 | Phishing |
| Campaign Created | T1566 | Phishing Infrastructure |

---

## What This Demonstrates

- Integrating a live SIEM (Splunk) with the Anthropic Claude API via Python
- Automated alert triage using large language models
- Structured AI output via prompt engineering — severity, classification, MITRE technique, risk score, recommended action
- Full SOC kill chain: phishing attack → SIEM detection → AI triage → incident report
- Real-world SOC workflow automation concepts and cost modeling

---

## Tools & Technologies

| Tool | Purpose | Cost |
|------|---------|------|
| Python 3 | Core scripting language | Free |
| Anthropic Claude API | AI alert analysis engine | Pay per use (~$0.001/alert) |
| Splunk Enterprise | SIEM — alert source | Free (500MB/day) |
| GoPhish | Phishing simulation | Free / Open Source |
| Mailhog | Local SMTP server | Free / Open Source |
| Kali Linux 2026.1 | Lab OS | Free |

---

## Cost Estimate

| Volume | Estimated Cost |
|--------|---------------|
| 10 alerts (this lab) | ~$0.01 |
| 100 alerts/day | ~$0.10/day |
| 1,000 alerts/day | ~$1.00/day |
| Enterprise scale (10k/day) | ~$10.00/day |

Compared to junior analyst headcount for the same triage volume, the ROI is significant — which is why AI-assisted triage is one of the fastest-growing areas in enterprise security.

---

## Quick Start

### Prerequisites
- Kali Linux 2026.1
- Python 3.13+
- Splunk Enterprise 9.3.2+ running locally
- Anthropic API key ([console.anthropic.com](https://console.anthropic.com))
- [Phishing Detection Lab](https://github.com/cpt-ferna02/splunk-phishing-lab) running and generating events

### Step 1 — Clone the repo
```bash
git clone https://github.com/cpt-ferna02/ai-soc-triage.git
cd ai-soc-triage
```

### Step 2 — Install dependencies
```bash
pip3 install anthropic requests --break-system-packages
```

### Step 3 — Configure credentials
```bash
nano config.py
```
```python
# Splunk settings
SPLUNK_HOST     = "https://localhost:8089"
SPLUNK_USER     = "YOUR_SPLUNK_USERNAME"
SPLUNK_PASS     = "YOUR_SPLUNK_PASSWORD"
SPLUNK_HEC      = "http://localhost:8088/services/collector/event"
SPLUNK_HEC_TOK  = "YOUR_HEC_TOKEN"

# Anthropic API
ANTHROPIC_KEY   = "YOUR_ANTHROPIC_API_KEY"

# GoPhish settings
GOPHISH_API     = "https://localhost:3333/api"
GOPHISH_KEY     = "YOUR_GOPHISH_API_KEY"
```
> `config.py` is in `.gitignore` — your credentials will never be committed to GitHub.

### Step 4 — Start the phishing lab services
```bash
# Terminal 1 — Mailhog
cd ~ && ./MailHog_linux_amd64

# Terminal 2 — GoPhish
cd ~/gophish && sudo ./gophish

# Terminal 3 — Splunk
sudo /opt/splunk/bin/splunk start

# Terminal 4 — GoPhish to Splunk forwarder
python3 ~/lab/gophish_to_splunk.py
```

### Step 5 — Run the triage engine
```bash
python3 triage.py
```

The system will pull the 10 most recent Splunk alerts, send each to Claude, print structured triage reports, and save everything to `triage_report.txt`.

---

## Project Structure

```
ai-soc-triage/
├── triage.py              # Main AI triage engine
├── config.py              # Credentials (gitignored)
├── .gitignore
├── triage_report.txt      # Sample output report
└── screenshots/
    ├── 01-triage-running.png
    ├── 02-critical-alert.png
    ├── 03-full-report.png
    └── 04-splunk-events.png
```

---

## Lessons Learned

- **Prompt engineering is the hard part.** AI output quality depends entirely on how the prompt is structured. Enforcing a strict output schema is critical for consistent, parseable results.
- **LLMs as force multipliers.** The AI doesn't replace the analyst — it handles repetitive first-pass triage so analysts can focus on true positives and complex investigations.
- **Alert context drives output quality.** Alerts with rich log data produce far better AI analysis than sparse ones. Garbage in, garbage out applies to LLMs too.
- **Always pin model versions.** Deprecated models silently break pipelines. Learned this the hard way.
- **Real-world next steps:** A production version would add email/Slack notifications for Critical alerts, automatic SOAR ticket creation, a feedback loop to improve classifications over time, and multi-source alert ingestion.

---

## Future Improvements

- [ ] Slack/email notifications for Critical severity alerts
- [ ] Splunk dashboard showing AI triage results over time
- [ ] False positive feedback loop to improve accuracy
- [ ] Additional log sources (Sysmon, Windows Events)
- [ ] Automatic SOAR ticket creation for True Positives
- [ ] Scheduled runs every 15 minutes via cron job
- [ ] Multi-model benchmarking (Claude vs other models)

---

## Related Projects

- **[Phishing Detection Lab](https://github.com/cpt-ferna02/splunk-phishing-lab)** — GoPhish + Mailhog + Splunk phishing simulation (this project's alert source)
- **[AI Threat Hunt Analyst](https://github.com/cpt-ferna02/ai-threat-hunt-analyst)** — EVTX log correlation and kill chain reconstruction
- **[AI SOC Detection Lab](https://github.com/cpt-ferna02/ai-soc-detection-lab)** — Wazuh SIEM + Claude AI alert enrichment pipeline

---

## Disclaimer

This project runs entirely in a controlled lab environment. All phishing simulations target fake email addresses on a local mail server. No real emails are sent. For educational and portfolio purposes only.
