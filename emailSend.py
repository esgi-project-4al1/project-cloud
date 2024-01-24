import boto3


class EmailSender:
    def __init__(self, topic_arn, region_name, aws_access_key_id, aws_secret_access_key):
        self.sns = boto3.client('sns', region_name=region_name,
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key)
        self.topic_arn = topic_arn

    def send_email(self, address_email, subject, message):
        response = self.sns.publish(
            TopicArn=self.topic_arn,
            Message=message,
            Subject=subject,
            MessageStructure='string',
            MessageAttributes={
                'email': {
                    'DataType': 'String',
                    'StringValue': address_email
                }
            }
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
