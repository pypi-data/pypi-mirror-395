# 🚀 s3-zipper

**High-performance, memory-safe ZIP/UNZIP utility for Amazon S3**  
Supports **same-account and cross-account** (STS assume-role) operations.  
Streams zip files directly between S3 buckets **without storing on disk**.

---

## ✨ Features

- 🔥 **True streaming ZIP creation** — no local temp files needed  
- 🌉 **Cross-account S3 copy** using AWS STS `AssumeRole`  
- 📦 **Streaming ZIP extraction** — handles very large ZIPs without RAM blow-ups  
- 🧪 **Fully tested** (pytest + moto)  
- 🖥️ **CLI included**: use `s3-zipper` from shell  
- 🧰 Pure Python package (`boto3`, `zipstream`)  

---

## 📦 Installation

```sh
pip install s3-zipper
```

### ZIP FLOW (S3 → ZIP → S3)
This flow zips all objects under a given prefix in one bucket and streams the ZIP directly into another bucket.

**CLI Usage**

```sh
s3-zipper \
  --flow zip \
  --source-s3-bucket my-source-bucket \
  --source-s3-key data/prefix/ \
  --target-s3-bucket my-target-bucket \
  --target-s3-key output/my-archive.zip \
  --region us-east-1
```

**With cross account role**

```sh
s3-zipper \
  --flow zip \
  --source-s3-bucket src-bucket \
  --source-s3-key logs/ \
  --target-s3-bucket dest-bucket \
  --target-s3-key backups/logs.zip \
  --source-role-arn arn:aws:iam::111111111111:role/SourceReadRole \
  --target-role-arn arn:aws:iam::222222222222:role/WriteZipRole \
  --region us-east-1
```

### UNZIP FLOW (ZIP in S3 → Extracted files → S3)
Streams each file from a ZIP stored in S3 and uploads each file individually to another S3 location — no disk needed.

```sh
s3-zipper \
  --flow unzip \
  --source-s3-bucket my-bucket \
  --source-s3-key archives/my.zip \
  --target-s3-bucket my-output \
  --target-s3-key extracted/
```

### Python API Usage
```sh
from s3_zipper.s3_client import get_s3_client
from s3_zipper.zip_flow import zip_s3_s3
from s3_zipper.unzip_flow import unzip_s3_s3

# Same-account client
client = get_s3_client(region="us-east-1")

# ZIP: s3://src-bucket/data/*  →  s3://dest-bucket/archive.zip
zip_s3_s3(
    args=SimpleNamespace(
        source_s3_bucket="src-bucket",
        source_s3_key="data/",
        target_s3_bucket="dest-bucket",
        target_s3_key="archive.zip",
        same_account=True,
        source_role_arn=None,
        target_role_arn=None
    ),
    source_s3=client,
    target_s3=client
)
```