import zipstream
import boto3
from .progress import ProgressTracker
from .logger import logger

def stream_s3_object(client, bucket, key, progress, chunk_size=1024 * 1024):
    """
    Stream an S3 object in chunks and update progress.
    """
    obj = client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"]

    for chunk in body.iter_chunks(chunk_size=chunk_size):
        if chunk:
            progress.update(len(chunk))
            yield chunk


def generate_zip_stream(source_client, bucket, prefix, progress):
    """
    Yield ZIP file chunks for all S3 objects under a prefix.
    Fully streaming using zipstream.
    """
    z = zipstream.ZipFile(mode="w", compression=zipstream.ZIP_DEFLATED)
    paginator = source_client.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            filename = key.split("/")[-1]

            # Each S3 file is streamed + progress tracked
            z.write_iter(
                arcname=filename,
                iterable=stream_s3_object(source_client, bucket, key, progress),
            )

    # Stream ZIP chunks out
    for chunk in z:
        yield chunk


def upload_stream_to_s3(target_client, bucket, key, stream, part_size=5 * 1024 * 1024):
    """
    Upload a generator stream to S3 using multipart upload.
    """
    mpu = target_client.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = mpu["UploadId"]

    parts = []
    part_number = 1
    buffer = b""

    try:
        for chunk in stream:
            buffer += chunk

            if len(buffer) >= part_size:
                resp = target_client.upload_part(
                    Bucket=bucket,
                    Key=key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=buffer,
                )
                parts.append({"ETag": resp["ETag"], "PartNumber": part_number})

                part_number += 1
                buffer = b""

        # Upload final buffer
        if buffer:
            resp = target_client.upload_part(
                Bucket=bucket,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=buffer,
            )
            parts.append({"ETag": resp["ETag"], "PartNumber": part_number})

        # Complete upload
        target_client.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            MultipartUpload={"Parts": parts},
            UploadId=upload_id,
        )

    except Exception:
        target_client.abort_multipart_upload(
            Bucket=bucket, Key=key, UploadId=upload_id
        )
        raise


def zip_s3_s3(args, source_client, target_client):
    """
    Orchestrates streaming ZIP → S3 upload.
    """
    source_bucket = args.source_s3_bucket
    source_prefix = args.source_s3_key

    target_bucket = args.target_s3_bucket
    target_key = args.target_s3_key or "archive.zip"

    logger.info(f"▶ Zipping objects from s3://{source_bucket}/{source_prefix}")

    # -------------------------------
    # 1️⃣ Calculate total bytes
    # -------------------------------
    paginator = source_client.get_paginator("list_objects_v2")
    total_bytes = 0

    for page in paginator.paginate(Bucket=source_bucket, Prefix=source_prefix):
        for obj in page.get("Contents", []):
            total_bytes += obj["Size"]

    # Init progress
    progress = ProgressTracker(total_bytes, label="ZIP")

    logger.info(f"▶ Uploading ZIP to s3://{target_bucket}/{target_key}")

    # -------------------------------
    # 2️⃣ Stream zip with progress
    # -------------------------------
    zip_stream = generate_zip_stream(
        source_client, source_bucket, source_prefix, progress
    )

    upload_stream_to_s3(
        target_client=target_client,
        bucket=target_bucket,
        key=target_key,
        stream=zip_stream,
    )

    # -------------------------------
    # 3️⃣ Finish progress
    # -------------------------------
    progress.finish()
    logger.info("✔ ZIP upload complete.")
