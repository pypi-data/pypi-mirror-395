from argparse import ArgumentParser
from security_scanner_analyzers.nuclei.nuclei import main 

if __name__ == "__main__":
    parser = ArgumentParser(description="Process a Nuclei JSON report.")

    parser.add_argument(
        "--file", "-f", required=True, help="Path to the Nuclei JSON report file."
    )

    # This part is correct (required=False for local testing)
    parser.add_argument(
        "--slack", "-s", required=False, help="Slack Webhook URL to send the report."
    )

    args = parser.parse_args()

    main(args.file, args.slack)