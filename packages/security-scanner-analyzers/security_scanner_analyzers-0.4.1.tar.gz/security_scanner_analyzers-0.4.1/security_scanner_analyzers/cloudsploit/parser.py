from collections import Counter
from security_scanner_analyzers.utils import load_json, load_yaml, generate_report, send_to_slack

def cloudsploit_count_field(data, field_name, skip_values=["ok"]):
    """
    Counts occurrences of a field (e.g., status) in the provided data list.
    """
    count_dict = {}
    for item in data:
        value = item.get(field_name, "unknown").lower()
        if skip_values and value in skip_values:
            continue
        count_dict[value] = count_dict.get(value, 0) + 1
    return count_dict

def summarize_failures(data):
    """
    Analyzes the JSON to find what actually failed.
    Note: 'data' passed here MUST be already filtered/cleaned of whitelist items.
    """
    # Filter for only failed items
    failed_items = [
        item for item in data 
        if item.get("status", "").lower() == "fail"
    ]
    
    if not failed_items:
        return "\n:white_check_mark: No failures detected (after applying whitelist rules)."

    # Group by Category
    categories = [item.get("category", "Unknown") for item in failed_items]
    cat_counts = Counter(categories)
    
    # Get Unique Failing Plugins
    failing_plugins = {item.get("plugin", "Unknown") for item in failed_items}

    # Build the text report
    details = []
    details.append("\n*--- :mag: Failure Analysis ---*")
    
    # Add Category Breakdown
    details.append("*Failures by Category:*")
    for cat, count in cat_counts.most_common():
        details.append(f"• {cat}: {count}")

    # Add specific failing rules
    details.append(f"\n*Unique Failing Rules ({len(failing_plugins)}):*")
    sorted_plugins = sorted(list(failing_plugins))
    
    plugin_list = "\n".join([f"• {p}" for p in sorted_plugins])
    details.append(plugin_list)

    return "\n".join(details)

def main(file_path, slack_url, config_file_path):
    # 1. Load the Configuration File
    config = load_yaml(config_file_path)
    
    # Nested structure: whitelist -> cloudsploit -> plugin
    whitelist = config.get("whitelist", {}).get("cloudsploit", {}).get("plugin", [])
    if whitelist is None: 
        whitelist = [] # Safety check

    # 2. Load the CloudSploit Report Data
    raw_data = load_json(file_path)
    
    # 3. GLOBAL FILTER: Create a clean dataset immediately
    # We explicitly exclude any item where the 'plugin' is in the whitelist.
    clean_data = [
        item for item in raw_data 
        if item.get("plugin", "") not in whitelist
    ]

    # 4. Generate the basic status report (Warn/Fail counts) using ONLY clean_data
    status_count = cloudsploit_count_field(clean_data, "status")
    base_report = generate_report(":cloud: CloudSploit Status Report", status_count)
    
    # 5. Generate the detailed breakdown using ONLY clean_data
    # Because clean_data has NO whitelisted items, the category counts MUST reflect that.
    detailed_analysis = summarize_failures(clean_data)
    
    # 6. Combine them
    full_report = f"{base_report}\n{detailed_analysis}"

    # 7. Send or Print
    if slack_url:
        send_to_slack(slack_url, full_report)
        print("Success: Report sent to Slack.")
    else:
        # Local Preview
        print("\n" + "="*40)
        print("    LOCAL PREVIEW (NOT SENT TO SLACK)")
        print("="*40)
        print(full_report)
        print("="*40 + "\n")