#!/usr/bin/env python3

import boto3
import urllib.request
import ssl
import sys
import os

def main():
    bucket_name = 'ds2002-f25-hbv6pz'  
    image_url = 'https://media.giphy.com/media/3o7btPCcdNniyf0ArS/giphy.gif'
    local_filename = 'downloaded_image.gif'
    expiration_seconds = 604800  
    
    print(f"Downloading file from {image_url}...")
    
    try:
        ssl_context = ssl._create_unverified_context()
        with urllib.request.urlopen(image_url, context=ssl_context) as response:
            with open(local_filename, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded to {local_filename}")
    except Exception as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)
    
    s3 = boto3.client('s3', region_name='us-east-1')
    
    print(f"\nUploading {local_filename} to s3://{bucket_name}/...")
    
    try:
        with open(local_filename, 'rb') as data:
            s3.put_object(
                Body=data,
                Bucket=bucket_name,
                Key=local_filename
            )
        print("Upload successful!")
    except Exception as e:
        print(f"Error uploading file: {e}")
        sys.exit(1)
    
    print(f"\nGenerating presigned URL (expires in {expiration_seconds} seconds)...")
    
    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': local_filename},
            ExpiresIn=expiration_seconds
        )
        
        print("\nPresigned URL:")
        print(presigned_url)
        print(f"\nThis URL will expire in {expiration_seconds} seconds ({expiration_seconds/86400} days)")
        
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()