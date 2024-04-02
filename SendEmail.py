import boto3
import json

def CheckEmotions(emotion_data_list):
    try:
        # Iterate over each dictionary in the emotion data list
        for emotion_data in emotion_data_list:
            image_name = emotion_data['ImageName']['S']

            # Iterate over each emotion type and confidence data
            for emotion_type, confidence_data in emotion_data.items():
                if emotion_type in ['ANGRY', 'FRUSTRATED']:
                    # Extract confidence scores from the data
                    confidence_scores = confidence_data.get('NS', [])
                    # Iterate over confidence scores
                    for confidence in confidence_scores:
                        try:
                            # Convert confidence score to float
                            confidence_float = float(confidence)
                            # Check if confidence score is greater than or equal to 10%
                            if confidence_float >= 10.0:
                                # Send email alert if confidence score is high
                                SendEmail(f"Emotion analysis for image {image_name}: {emotion_type} emotion confidence > 10% - {confidence_float}")
                                # Break loop if emotion is found
                                break
                        except ValueError:
                            print(f"Invalid confidence score format for {emotion_type} emotion in image {image_name}")
    except Exception as e:
        print(f"Error checking emotions: {str(e)}")

def SendEmail(message):
    try:
        sns_client = boto3.client('sns')
        # Publish email message to SNS topic
        sns_client.publish(
            TopicArn='arn:aws:sns:us-east-1:975049959573:SendEmail',
            Message=message,
            Subject='Emotion Alert'
        )
    except Exception as e:
        print(f"Error sending email: {e}")

def lambda_handler(event, context):
    try:
        # Filter insert events from the event records
        insert_events = [record for record in event['Records'] if record['eventName'] == 'INSERT']
        # Extract emotion data from insert events
        emotion_data = [record['dynamodb']['NewImage'] for record in insert_events]

        # Check emotions for the extracted data
        CheckEmotions(emotion_data)

        return {
            'statusCode': 200,
            'body': json.dumps('Emotion check and email sending successful')
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error')
        }
