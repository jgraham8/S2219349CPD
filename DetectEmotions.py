import boto3
import json

def DetectEmotions(image_key):
    try:
        rekognition_client = boto3.client("rekognition")
        
        # Detect emotions using Rekognition
        response = rekognition_client.detect_faces(
            Image={
                "S3Object": {
                    "Bucket": "mybucket-s2219349",
                    "Name": image_key
                }
            },
            Attributes=['ALL']
        )
        
        return response["FaceDetails"]
    except Exception as e:
        print(f"Error detecting emotions for image {image_key}: {str(e)}")
        return []

def AggregateEmotions(face_details):
    aggregated_emotions = {}
    total_faces = len(face_details)
    
    for face_detail in face_details:
        for emotion in face_detail["Emotions"]:
            emotion_type = emotion["Type"]
            confidence = emotion["Confidence"]
            
            if emotion_type in aggregated_emotions:
                aggregated_emotions[emotion_type] += confidence
            else:
                aggregated_emotions[emotion_type] = confidence
    
    for emotion_type in aggregated_emotions:
        aggregated_emotions[emotion_type] /= total_faces
    
    return aggregated_emotions

def StoreData(image_key, aggregated_emotions):
    try:
        dynamodb_client = boto3.client("dynamodb")
        
        # Insert aggregated data into DynamoDB
        primary_key = image_key.split('/')[-1]  # Extracts image name from key
        dynamodb_client.put_item(
            TableName= "dynamodb-table-s2219349",
            Item={
                "ImageName": {"S": primary_key},
                **{emotion: {"N": str(aggregated_emotions[emotion])} for emotion in aggregated_emotions}
            }
        )
        print(f"Data inserted into DynamoDB for image {primary_key}")
    except Exception as e:
        print(f"Error inserting data into DynamoDB for image {image_key}: {str(e)}")

def lambda_handler(event, context):
    try:
        body = json.loads(event["Records"][0]["body"])
        image_key = body['Records'][0]['s3']['object']['key']
        
        face_details = DetectEmotions(image_key)
        aggregated_emotions = AggregateEmotions(face_details)
        
        StoreData(image_key, aggregated_emotions)
        
        return {
            'statusCode': 200,
            'body': json.dumps('Emotion analysis and data insertion successful')
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }