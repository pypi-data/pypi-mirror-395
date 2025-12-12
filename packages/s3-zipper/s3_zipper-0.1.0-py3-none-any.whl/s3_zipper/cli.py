from .zip_flow import zip_s3_s3
from .unzip_flow import unzip_s3_s3
from .s3_client import get_s3_client
from .logger import logger
import argparse


def build_parser():
    parser = argparse.ArgumentParser(description="S3 ZIP/UNZIP utility")

    parser.add_argument("--flow", required=True, choices=["zip", "unzip"])
    parser.add_argument("--source-s3-bucket", required=True)
    parser.add_argument("--source-s3-key")
    parser.add_argument("--target-s3-bucket", required=True)
    parser.add_argument("--target-s3-key")
    parser.add_argument("--same-account", action="store_true")

    parser.add_argument("--source-role-arn")
    parser.add_argument("--target-role-arn")

    parser.add_argument("--region", default="us-east-1")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    logger.info(f"▶ Running flow: {args.flow}")

    # Create clients
    logger.info("▶ Initializing S3 clients...")
    # If same account is explicitly forced → ignore role ARNs
    if args.same_account:
        source_client = get_s3_client(None, args.region)
        target_client = get_s3_client(None, args.region)
    else:
        source_client = get_s3_client(args.source_role_arn, args.region)
        target_client = get_s3_client(args.target_role_arn, args.region)


    # Route to flows
    if args.flow == "zip":
        zip_s3_s3(args, source_client, target_client)
    else:
        unzip_s3_s3(args, source_client, target_client)
