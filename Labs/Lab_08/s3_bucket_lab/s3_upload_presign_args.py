#!/usr/bin/env python3

import boto3
import urllib.request
import ssl  
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Download a file from the internet, upload to S3, and generate presigned URL'
    )
    parser.add_argument('url', help='URL of the file to download')
    parser.add_argument('bucket', help='S3 bucket name')
    parser.add_argument('--filename', help='Local filename (optional, auto-detected from URL)')
    parser.add_argument('--expiration', type=int, default=604800,
                       help='URL expiration in seconds (default: 604800 = 7 days)')
    
    args = parser.parse_args()
    
    if args.filename:
        local_filename = args.filename
    else:
        local_filename = args.url.split('/')[-1]
        if not local_filename or '.' not in local_filename:
            local_filename = 'downloaded_file.dat'
    
    print(f"Downloading file from {args.url}...")
    
    try:
        ssl_context = ssl._create_unverified_context()
        with urllib.request.urlopen(args.url, context=ssl_context) as response:
            with open(local_filename, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded to {local_filename}")
    except Exception as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)
    
    s3 = boto3.client('s3', region_name='us-east-1')
    
    print(f"\nUploading {local_filename} to s3://{args.bucket}/...")
    
    try:
        with open(local_filename, 'rb') as data:
            s3.put_object(
                Body=data,
                Bucket=args.bucket,
                Key=local_filename
            )
        print("Upload successful!")
    except Exception as e:
        print(f"Error uploading file: {e}")
        sys.exit(1)
    
    print(f"\nGenerating presigned URL (expires in {args.expiration} seconds)...")
    
    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': args.bucket, 'Key': local_filename},
            ExpiresIn=args.expiration
        )
        
        print("\nPresigned URL:")
        print(presigned_url)
        print(f"\nThis URL will expire in {args.expiration} seconds ({args.expiration/86400:.1f} days)")
        
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()