import boto3
import time

def UploadImagesToBucket():
    # Initialize S3 and SQS clients
    s3_client = boto3.client("s3")

    try:
        # List of image files to upload
        image_files = ['IMAGE1.png', 'IMAGE2.png', 'IMAGE3.png', 'IMAGE4.png', 'IMAGE5.png']
        
        # Iterate through each image file
        for index, image in enumerate(image_files):
            # Upload image file to S3 bucket
            s3_client.upload_file(f"./images/{image}", "s3bucket-s2219349", image)
            print(f"{image} uploaded.")
            
            # Wait for 10 seconds before uploading the next image
            time.sleep(10)  

        print("Uploading Successful")
    except Exception as e:
        print(f"Error Uploading Images {e}")
    
if __name__ == "__main__":
    UploadImagesToBucket()
