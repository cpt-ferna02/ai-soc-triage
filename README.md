AI-Powered SOC Alert Triage System
An advanced cybersecurity project that combines a live phishing detection pipeline with an AI analyst powered by Claude (Anthropic) to automatically triage, classify, and generate incident reports for security alerts — in real time.
Built on Kali Linux 2026.1 as a portfolio project demonstrating next-generation SOC automation, AI integration, and threat detection engineering.

This project extends the Phishing Detection Lab — feeding its live Splunk alerts into an AI triage engine.


The Problem This Solves
SOC analysts are buried in alerts. The average enterprise SOC receives thousands of alerts per day, and studies show that over 40% go uninvestigated due to alert fatigue. Junior analysts spend most of their time on repetitive triage tasks instead of actual investigation.
This project simulates an AI-assisted triage layer that:

Automatically pulls alerts from a SIEM (Splunk)
Sends each alert to an AI model for analysis
Returns structured severity ratings, classifications, MITRE ATT&CK mappings, and recommended actions
Saves everything to an incident report — in seconds


What This Lab Demonstrates

Integrating a live SIEM (Splunk) with the Anthropic Claude API via Python
Automated alert triage using large language models (LLMs)
Structured AI output: severity, classification, MITRE technique, risk score, recommended action
Full SOC kill chain from phishing attack → SIEM detection → AI triage → incident report
Prompt engineering for consistent, structured security analysis output
Real-world SOC workflow automation concepts


MITRE ATT&CK Techniques Triaged
Alert TypeTechnique IDTechnique NameSubmitted DataT1566 / T1056.003Phishing / Web Portal CaptureClicked LinkT1566.002Spearphishing LinkEmail OpenedT1566PhishingCampaign CreatedT1566Phishing Infrastructure

Tools & Technologies
ToolPurposeCostPython 3Core scripting languageFreeAnthropic Claude APIAI alert analysis enginePay per use (~$0.001/alert)Splunk EnterpriseSIEM — alert sourceFree (500MB/day)GoPhishPhishing simulation — generates alertsFree / Open SourceMailhogLocal SMTP serverFree / Open SourceKali Linux 2026.1Lab operating systemFree

Architecture
┌─────────────────────────────────────────────────────┐
│                    ATTACK LAYER                      │
│  GoPhish Campaign → Mailhog → Phishing Kill Chain   │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                  DETECTION LAYER                     │
│         Splunk SIEM (index=main source=gophish)     │
│    Email Sent | Opened | Clicked | Submitted Data   │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                    TRIAGE LAYER                      │
│              Python Triage Engine                    │
│   Pulls alerts from Splunk REST API every run       │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                      AI LAYER                        │
│           Anthropic Claude API                       │
│  Input: Raw alert data                              │
│  Output: Severity | Classification | MITRE |        │
│          Summary | Recommended Action | Risk Score  │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                   REPORTING LAYER                    │
│     triage_report.txt — full incident report        │
│     Timestamped, structured, ready for review       │
└─────────────────────────────────────────────────────┘

Sample AI Triage Output
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

Prerequisites

Kali Linux 2026.1
Python 3.13+
Splunk Enterprise 9.3.2+ running locally
Anthropic API key (get one at console.anthropic.com)
Phishing Detection Lab running and generating events


If you haven't set up the phishing lab yet, start here first:
github.com/cpt-ferna02/splunk-phishing-lab


Setup — Step by Step
Step 1 — Clone the repo
bashgit clone https://github.com/cpt-ferna02/ai-soc-triage.git
cd ai-soc-triage
Step 2 — Install dependencies
bashpip3 install anthropic requests --break-system-packages
Step 3 — Configure your credentials
Create your config file:
bashnano config.py
Fill in your values:
python# Splunk settings
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

config.py is in .gitignore — your credentials will never be committed to GitHub.

Step 4 — Make sure your phishing lab is running
Start all services in this order:
bash# Terminal 1 — Mailhog
cd ~ && ./MailHog_linux_amd64

# Terminal 2 — GoPhish
cd ~/gophish && sudo ./gophish

# Terminal 3 — Splunk
sudo /opt/splunk/bin/splunk start

# Terminal 4 — GoPhish to Splunk forwarder
python3 ~/lab/gophish_to_splunk.py
Step 5 — Run the AI triage system
bashpython3 triage.py
The system will:

Pull the 10 most recent alerts from Splunk
Send each one to Claude AI for analysis
Print structured triage reports to the terminal
Save all reports to triage_report.txt


How the AI Prompt Works
The triage engine sends each alert to Claude with a structured prompt that enforces consistent output format:
pythonprompt = f"""
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
This prompt engineering technique — enforcing structured output format — is the same approach used in production AI security tools.

AI Triage Results Summary
From a live run against 10 phishing alerts:
Alert TypeAI SeverityClassificationRisk ScoreSubmitted DataCriticalTrue Positive9/10Submitted DataCriticalTrue Positive9/10Clicked LinkHighNeeds Investigation7/10Clicked LinkHighNeeds Investigation7/10Email OpenedHighNeeds Investigation7/10Email OpenedHighNeeds Investigation7/10Email SentMediumNeeds Investigation5/10Email SentLowNeeds Investigation3/10Campaign CreatedMediumNeeds Investigation5/10Campaign CreatedLowNeeds Investigation3/10

Repository Structure
ai-soc-triage/
├── README.md
├── triage.py              ← main AI triage engine
├── config.py              ← credentials (gitignored)
├── .gitignore
├── triage_report.txt      ← sample output report
├── sample-output/
│   └── sample_triage_report.txt   ← sanitized example report
└── screenshots/
    ├── 01-triage-running.png
    ├── 02-critical-alert.png
    ├── 03-full-report.png
    └── 04-splunk-events.png

Lessons Learned

Prompt engineering matters: The AI output quality depends entirely on how the prompt is structured. Enforcing a strict output format in the prompt is critical for parsing and automation.
LLMs as force multipliers: The AI doesn't replace the analyst — it handles the repetitive first-pass triage so analysts can focus on true positives and complex investigation.
Alert context is everything: Alerts with missing details (like Campaign Created) produce lower quality AI analysis. Rich log data = better AI output.
Cost efficiency: 10 alert triage costs less than $0.01 using Claude Sonnet. At scale this is dramatically cheaper than adding headcount.
Model versioning: Always pin to a specific model version in production code. Deprecated models break pipelines.
Real world additions: A production version would add: email notifications for Critical alerts, automatic ticket creation in a SOAR platform, feedback loop to improve AI classifications over time, and multi-source alert ingestion beyond just phishing.


Cost Estimate
VolumeEstimated Cost10 alerts (this lab)~$0.01100 alerts/day~$0.10/day1,000 alerts/day~$1.00/dayEnterprise scale (10k/day)~$10.00/day
Compared to a junior SOC analyst salary for the same triage work, the ROI is significant — which is why AI-assisted triage is one of the fastest growing areas in enterprise security.

Future Improvements

 Add Slack/email notifications for Critical severity alerts
 Build a Splunk dashboard showing AI triage results
 Add false positive feedback loop to improve accuracy
 Integrate with additional log sources (Sysmon, Windows Events)
 Add automatic SOAR ticket creation for True Positives
 Schedule automatic runs every 15 minutes via cron job
 Add multi-model support (compare Claude vs other models)


Related Projects
This project is part of a cybersecurity portfolio ecosystem:

Phishing Detection Lab — GoPhish + Mailhog + Splunk phishing simulation and detection
Active Directory Home Lab — Windows Server 2022 AD attack and defense simulation


Disclaimer
This project is built entirely in a controlled lab environment. All phishing simulations target fake email addresses on a local mail server. No real emails are sent. The AI triage system is for educational and portfolio purposes only.

Author
Built as an advanced cybersecurity portfolio project demonstrating AI integration, SOC automation, SIEM engineering, and prompt engineering for security use cases.ShareContent┌──(kali㉿kali)-[~/gophish]
└─$ python3 ~/lab/gophish_to_splunk.py
Polling GoPhish...
/usr/lib/python3/dist-packages/urllib3/connectionpool.py:1097: InsecureRequestWarning: Unverified HTTPS request is being made to host 'localhost'. Adding certificate verification is strongly advised. See: https:/pasted┌──(kali㉿kali)-[~/ai-soc-triage]
└─$ python3 triage.py

🔍 AI SOC Triage System Starting...
Pulling alerts from Splunk...

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 787, in urlopen
    response = self._make_request(
        copasted┌──(kali㉿kali)-[~/ai-soc-triage]
└─$ python3 triage.py

🔍 AI SOC Triage System Starting...
Pulling alerts from Splunk...

Found 10 alerts. Sending to AI for triage...

Triaging alert 1 of 10: Clicked Link...

============================================================
TRIAGE REPORT — 20pasted
