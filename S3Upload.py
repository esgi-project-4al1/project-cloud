import boto3
from boto3 import exceptions


class S3Upload:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='eu-north-1'
        )
        self.url = ""

    def upload_file(self, file, file_name):
        try:
            self.s3.upload_fileobj(file, self.bucket_name, file_name)
            url = self.s3.generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_name},
                ExpiresIn=3600*12,
            )
            self.url = url
            return True
        except exceptions as e:
            print("Error uploading {}: {}".format(file_name, e))
            return False

    def get_file_url(self):
        return self.url

    def suppress_all_download(self):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if response['KeyCount'] == 0:
            return True
        files_in_folder = response["Contents"]
        files_to_delete = []
        # We will create Key array to pass to delete_objects function
        for f in files_in_folder:
            files_to_delete.append({"Key": f["Key"]})
        if len(files_to_delete) == 0:
            return True

        response = self.s3.delete_objects(
            Bucket=self.bucket_name, Delete={"Objects": files_to_delete}
        )

