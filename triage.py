import anthropic
import requests
import json
import time
from datetime import datetime
from config import *

# Suppress SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

def get_splunk_alerts():
    """Pull phishing events from Splunk"""
    search_query = """
    search index=main source=gophish
    | table _time, message, email, details
    | sort -_time
    | head 10
    """
    
    url = "https://localhost:8089/services/search/jobs"
    
    response = requests.post(
        url,
        auth=(SPLUNK_USER, SPLUNK_PASS),
        data={
            "search": search_query,
            "output_mode": "json",
            "exec_mode": "oneshot"
        },
        verify=False
    )
    
    results = response.json()
    events = results.get("results", [])
    return events

def triage_alert(event):
    """Send alert to Claude AI for triage"""
    
    prompt = f"""
You are a SOC analyst triaging a security alert. Analyze this phishing detection alert and provide a structured assessment.

ALERT DATA:
- Time: {event.get('_time', 'Unknown')}
- Event Type: {event.get('message', 'Unknown')}
- Target Email: {event.get('email', 'Unknown')}
- Details: {event.get('details', 'None')}

Provide your analysis in this EXACT format:

SEVERITY: [Critical/High/Medium/Low]
CLASSIFICATION: [True Positive/False Positive/Needs Investigation]
MITRE_TECHNIQUE: [technique ID and name]
SUMMARY: [one sentence summary of what happened]
RECOMMENDED_ACTION: [specific action a SOC analyst should take]
RISK_SCORE: [1-10]
"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def save_report(event, analysis):
    """Save triage result to a report file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
{'='*60}
TRIAGE REPORT — {timestamp}
{'='*60}
ORIGINAL ALERT:
  Time:       {event.get('_time', 'Unknown')}
  Event Type: {event.get('message', 'Unknown')}
  Target:     {event.get('email', 'Unknown')}

AI ANALYSIS:
{analysis}
{'='*60}
"""
    
    with open("triage_report.txt", "a") as f:
        f.write(report)
    
    print(report)

def run_triage():
    """Main triage loop"""
    print("\n🔍 AI SOC Triage System Starting...")
    print("Pulling alerts from Splunk...\n")
    
    events = get_splunk_alerts()
    
    if not events:
        print("No events found in Splunk.")
        return
    
    print(f"Found {len(events)} alerts. Sending to AI for triage...\n")
    
    for i, event in enumerate(events):
        print(f"Triaging alert {i+1} of {len(events)}: {event.get('message')}...")
        
        analysis = triage_alert(event)
        save_report(event, analysis)
        
        # Small delay to respect API rate limits
        time.sleep(1)
    
    print(f"\n✅ Triage complete! Report saved to triage_report.txt")

if __name__ == "__main__":
    run_triage()
