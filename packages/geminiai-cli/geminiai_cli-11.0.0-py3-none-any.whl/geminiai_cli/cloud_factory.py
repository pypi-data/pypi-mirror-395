import os
from .b2 import B2Manager
from .cloud_s3 import S3Provider
from .ui import console

def get_cloud_provider(args):
    """
    Factory to return the appropriate cloud provider based on args/config.
    """
    # Priority: S3 config keys present? Or B2 config keys?
    # Since B2 keys are --b2-id etc, we can check those.
    # We need to add --aws-access-key-id etc or --cloud-provider=s3/b2

    # For now, let's assume we can detect based on presence of specific args.
    # But args might be missing if stored in config file.
    # Let's check environment or args.

    # S3
    # Check if we have S3 credentials in args or env
    s3_key = os.environ.get("GEMINI_AWS_ACCESS_KEY_ID")
    s3_secret = os.environ.get("GEMINI_AWS_SECRET_ACCESS_KEY")
    s3_bucket = os.environ.get("GEMINI_S3_BUCKET")
    s3_region = os.environ.get("GEMINI_S3_REGION", "us-east-1")

    # B2
    b2_id = args.b2_id or os.environ.get("GEMINI_B2_KEY_ID")
    b2_key = args.b2_key or os.environ.get("GEMINI_B2_APP_KEY")
    b2_bucket = args.bucket or os.environ.get("GEMINI_B2_BUCKET")

    # If args has --provider (we haven't added it yet), or we infer.
    # Let's infer. If s3_key is set, prefer S3? Or if b2_id is set, prefer B2?
    # What if both?

    # Let's check "cloud_provider" from config if we added it.
    # We didn't add it yet to args.py.

    # Simple logic: If B2 credentials explicit in args -> B2
    if args.b2_id and args.b2_key:
        return B2Manager(args.b2_id, args.b2_key, args.bucket)

    # If S3 env vars exist -> S3
    if s3_key and s3_secret and s3_bucket:
        return S3Provider(s3_bucket, s3_key, s3_secret, s3_region)

    # Default to B2 if environment vars exist
    if b2_id and b2_key and b2_bucket:
         return B2Manager(b2_id, b2_key, b2_bucket)

    console.print("[yellow]No valid cloud credentials found. Please configure B2 or S3.[/]")
    return None
