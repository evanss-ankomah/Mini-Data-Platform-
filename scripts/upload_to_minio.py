"""
upload_to_minio.py — Upload a CSV file to MinIO landing zone.

Usage:
    python scripts/upload_to_minio.py --file data/sample_sales.csv
    python scripts/upload_to_minio.py --file data/sample_sales.csv --bucket landing --prefix sales/
"""
import argparse
import os
from minio import Minio


def main():
    parser = argparse.ArgumentParser(description="Upload CSV to MinIO")
    parser.add_argument("--file", type=str, required=True, help="Path to CSV file")
    parser.add_argument("--bucket", type=str, default="landing", help="MinIO bucket name")
    parser.add_argument("--prefix", type=str, default="sales/", help="Object key prefix")
    parser.add_argument("--endpoint", type=str, default="localhost:9000", help="MinIO endpoint")
    parser.add_argument("--access-key", type=str, default="minioadmin", help="MinIO access key")
    parser.add_argument("--secret-key", type=str, default="changeme123", help="MinIO secret key")
    args = parser.parse_args()

    client = Minio(
        endpoint=args.endpoint,
        access_key=args.access_key,
        secret_key=args.secret_key,
        secure=False,
    )

    # Ensure bucket exists
    if not client.bucket_exists(args.bucket):
        client.make_bucket(args.bucket)

    filename = os.path.basename(args.file)
    object_name = f"{args.prefix}{filename}"

    client.fput_object(args.bucket, object_name, args.file)
    print(f"Uploaded {args.file} -> s3://{args.bucket}/{object_name}")


if __name__ == "__main__":
    main()
