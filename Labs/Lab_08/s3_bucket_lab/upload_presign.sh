#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <local_file> <bucket_name> <expiration_seconds>"
    echo "Example: $0 myfile.jpg ds2002-f25-abc123 604800"
    exit 1
fi

LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=$3

if [ ! -f "$LOCAL_FILE" ]; then
    echo "Error: File '$LOCAL_FILE' does not exist"
    exit 1
fi

FILENAME=$(basename "$LOCAL_FILE")

echo "Uploading $LOCAL_FILE to s3://$BUCKET_NAME/$FILENAME..."

aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/$FILENAME"

if [ $? -eq 0 ]; then
    echo "Upload successful!"
    echo "Generating presigned URL (expires in $EXPIRATION seconds)..."
    
    PRESIGNED_URL=$(aws s3 presign --expires-in "$EXPIRATION" "s3://$BUCKET_NAME/$FILENAME")
    
    echo ""
    echo "Presigned URL:"
    echo "$PRESIGNED_URL"
    echo ""
    echo "This URL will expire in $EXPIRATION seconds"
else
    echo "Upload failed!"
    exit 1
fi