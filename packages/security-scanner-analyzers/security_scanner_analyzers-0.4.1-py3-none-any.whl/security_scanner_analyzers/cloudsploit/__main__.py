from argparse import ArgumentParser
from security_scanner_analyzers.cloudsploit.parser import main

if __name__ == "__main__":
    parser = ArgumentParser(description="Process a CloudSploit JSON report using an external configuration file for whitelisting.")

    parser.add_argument(
        "--file",
        "-f",
        required=True,
        help="Path to the CloudSploit JSON report file."
    )

    parser.add_argument(
        "--slack",
        "-s",
        required=True,
        help="Slack Webhook URL to send the report."
    )
    
    parser.add_argument(
        "--config-file", 
        "-c", 
        required=False, 
        help="Path to the YAML configuration file to skip the whitelist."
    )

    args = parser.parse_args()
    
    main(args.file, args.slack, args.config_file)