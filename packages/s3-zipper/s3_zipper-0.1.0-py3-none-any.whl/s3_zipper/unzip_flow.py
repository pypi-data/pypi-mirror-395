import boto3
import zipfile
import io
from .progress import ProgressTracker
from .logger import logger

def multipart_upload_stream(target_client, bucket, key, stream, part_size=5 * 1024 * 1024):
    """
    Upload a byte-stream generator to S3 using multipart upload.
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
                    UploadId=upload_id,
                    PartNumber=part_number,
                    Body=buffer,
                )
                parts.append({"ETag": resp["ETag"], "PartNumber": part_number})
                part_number += 1
                buffer = b""

        # Upload remaining buffer
        if buffer:
            resp = target_client.upload_part(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=buffer,
            )
            parts.append({"ETag": resp["ETag"], "PartNumber": part_number})

        target_client.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )

    except Exception:
        target_client.abort_multipart_upload(
            Bucket=bucket, Key=key, UploadId=upload_id
        )
        raise


def stream_zip_entries(s3_client, bucket, key, progress=None, chunk_size=1024 * 1024):
    """
    Download a ZIP from S3 and yield (filename, file_bytes_generator).
    Only ZIP headers are buffered; entries are streamed.
    """

    obj = s3_client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"]

    zip_buffer = io.BytesIO()

    # Stream downloaded zip → memory
    for chunk in body.iter_chunks(chunk_size=chunk_size):
        if chunk:
            zip_buffer.write(chunk)
            if progress:
                progress.update(len(chunk))

    zip_buffer.seek(0)

    # Now iterate ZIP entries
    with zipfile.ZipFile(zip_buffer, "r") as z:
        for name in z.namelist():
            with z.open(name) as f:

                def file_chunk_generator():
                    while True:
                        data = f.read(chunk_size)
                        if not data:
                            break
                        if progress:
                            progress.update(len(data))
                        yield data

                yield name, file_chunk_generator()


def unzip_s3_s3(args, source_client, target_client):
    """
    Unzip ZIP file stored in S3 and upload each file to another S3 location.
    """

    source_bucket = args.source_s3_bucket
    source_key = args.source_s3_key

    target_bucket = args.target_s3_bucket
    target_prefix = args.target_s3_key or ""

    logger.info(f"▶ Unzipping s3://{source_bucket}/{source_key}")

    # -----------------------------------------
    # 1️⃣ Get total ZIP size for progress tracker
    # -----------------------------------------
    head = source_client.head_object(Bucket=source_bucket, Key=source_key)
    total_bytes = head["ContentLength"]

    progress = ProgressTracker(total_bytes, label="UNZIP")

    logger.info(f"▶ Uploading extracted files to s3://{target_bucket}/{target_prefix}")

    # -----------------------------------------
    # 2️⃣ Stream entries + upload with progress
    # -----------------------------------------
    for filename, file_stream in stream_zip_entries(
        source_client,
        source_bucket,
        source_key,
        progress=progress,
    ):
        target_key = f"{target_prefix.rstrip('/')}/{filename}"

        logger.info(f"  → Extracting: {filename}")

        multipart_upload_stream(
            target_client=target_client,
            bucket=target_bucket,
            key=target_key,
            stream=file_stream,
        )

    # -----------------------------------------
    # 3️⃣ Finish reporting
    # -----------------------------------------
    progress.finish()
    logger.info("✔ Unzip + upload complete.")
