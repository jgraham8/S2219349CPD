import boto3
import time
import json

def UploadImagesToBucket():
    s3_client = boto3.client("s3")
    sqs_client = boto3.client('sqs')

    try:
        image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'image4.jpg', 'image5.jpg']
        
        for image in image_files:
            s3_client.upload_file(f"./images/{image}", "mybucket-s2219349", image)
            print(f"{image} uploaded.")

            time.sleep(10)

        print("Uploading Successful")
    except Exception as e:
        print(f"Error Uploading Images {e}")
    
if __name__ == "__main__":
    UploadImagesToBucket()