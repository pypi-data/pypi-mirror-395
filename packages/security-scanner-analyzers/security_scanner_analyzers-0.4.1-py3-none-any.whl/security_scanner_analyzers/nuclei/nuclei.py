from collections import Counter
from security_scanner_analyzers.utils import load_json, generate_report, send_to_slack

def count_nuclei_severity(data):
    """
    Counts findings by severity (Critical, High, Medium, Low, Info).
    """
    severity_counts = {}
    for item in data:
        # Nuclei stores severity inside the 'info' dictionary
        severity = item.get("info", {}).get("severity", "unknown").lower()
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    return severity_counts

def summarize_nuclei_findings(data):
    """
    Analyzes Nuclei JSON to find unique failing templates.
    """
    if not data:
        return "\n:white_check_mark: No Nuclei findings detected."

    # 1. Group by Severity
    severities = [item.get("info", {}).get("severity", "unknown").capitalize() for item in data]
    severity_counts = Counter(severities)
    
    # 2. Get Unique Failing Templates (deduplicated)
    failing_templates = {item.get("template-id", "Unknown") for item in data}

    # Build the text report
    details = []
    details.append("\n*--- :radioactive_sign: Nuclei Analysis ---*")
    
    # Add Severity Breakdown (Sorted by importance)
    details.append("*Findings by Severity:*")
    order = ["Critical", "High", "Medium", "Low", "Info", "Unknown"]
    
    for sev in order:
        if severity_counts[sev] > 0:
            details.append(f"• {sev}: {severity_counts[sev]}")

    # Add specific failing templates (UNLIMITED LIST)
    details.append(f"\n*Unique Templates Triggered ({len(failing_templates)}):*")
    sorted_templates = sorted(list(failing_templates))
    
    # Loop through ALL templates
    template_list = "\n".join([f"• {t}" for t in sorted_templates])
    details.append(template_list)

    return "\n".join(details)

def main(file_path, slack_url=None):
    data = load_json(file_path)
    
    # 1. Get the basic stats
    severity_counts = count_nuclei_severity(data)
    base_report = generate_report(":warning: Nuclei Scan Report", severity_counts)
    
    # 2. Generate the detailed breakdown
    detailed_analysis = summarize_nuclei_findings(data)
    
    # 3. Combine them
    full_report = f"{base_report}\n{detailed_analysis}"

    # 4. Decide: Send to Slack OR Print to Console
    if slack_url:
        send_to_slack(slack_url, full_report)
        print("Success: Nuclei report sent to Slack.")
    else:
        # Local Preview
        print("\n" + "="*40)
        print("   LOCAL PREVIEW (NOT SENT TO SLACK)")
        print("="*40)
        print(full_report)
        print("="*40 + "\n")