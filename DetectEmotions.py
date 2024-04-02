import boto3
import json

def DetectEmotions(image_key):
    try:
        rekognition_client = boto3.client("rekognition")
        
        response = rekognition_client.detect_faces(
            Image={
                "S3Object": {
                    "Bucket": "s3bucket-s2219349",
                    "Name": image_key
                }
            },
            Attributes=['ALL']
        )
        
        return response["FaceDetails"]
    except Exception as e:
        print(f"Error detecting emotions for image {image_key}: {str(e)}")
        return []

def FormatEmotions(image_key, image_data):
    data = {}

    # Iterate over each face detail
    for face_detail in image_data:
        # Iterate over emotions detected for each face
        for emotion in face_detail["Emotions"]:
            emotion_type = emotion["Type"]
            confidence = emotion["Confidence"]
            
            # Aggregate emotions by type
            if emotion_type in data:
                data[emotion_type].append(confidence)
            else:
                data[emotion_type] = [confidence]

    formatted_data = {
        "ImageName": {"S": image_key}
    }
    for emotion_type, confidences in data.items():
            formatted_data[emotion_type] = {"NS": [str(confidence) for confidence in confidences]}

    return formatted_data

def RemoveDuplicates(emotion_data):
    # Iterate over each item in the emotion data
    for emotion, scores in emotion_data.items():
        # Check if 'NS' key exists
        if 'NS' in scores:
            # Convert the list to a set to remove duplicates
            unique_scores = list(set(scores.get('NS', [])))
            # Update the emotion data with the unique scores
            emotion_data[emotion]['NS'] = unique_scores
    return emotion_data

def StoreData(image_key, formatted_data):
    try:
        dynamodb_client = boto3.client("dynamodb")

        # Insert aggregated data into DynamoDB
        dynamodb_client.put_item(
            TableName = "dyndb-s2219349",
            Item = formatted_data
        )
        print(f"Data inserted into DynamoDB for image {image_key}")
    except Exception as e:
        print(f"Error inserting data into DynamoDB for image {image_key}: {str(e)}")

def lambda_handler(event, context):
    try:
        body = json.loads(event["Records"][0]["body"])
        image_key = body['Records'][0]['s3']['object']['key']
        
        face_details = DetectEmotions(image_key)

        formatted_data = FormatEmotions(image_key, face_details)
        
        formatted_data = RemoveDuplicates(formatted_data)

        StoreData(image_key, formatted_data)
        
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