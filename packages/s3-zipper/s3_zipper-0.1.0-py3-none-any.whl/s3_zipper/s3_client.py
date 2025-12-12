import boto3


def assume_role(role_arn, region):
    """
    Assume an IAM role and return temporary credentials.
    """
    sts = boto3.client("sts", region_name=region)

    resp = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName="s3_zipper_session"
    )

    creds = resp["Credentials"]

    return boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
    )


def get_s3_client(role_arn: str, region: str):
    """
    Returns either:
      - default S3 client   (same account)
      - STS-assumed S3 client (cross account)
    """
    # No role provided → use default credentials
    if not role_arn:
        return boto3.client("s3", region_name=region)

    # Role provided → cross-account
    return assume_role(role_arn, region)
