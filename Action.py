import re
from pydoc import html

from flask import current_app
from werkzeug.utils import secure_filename

from CoolConfig import CoolConfig
from S3Upload import S3Upload
from emailSend import EmailSender


def is_valid_email(email):
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.match(regex, email) is not None


def sanitize_input(input_str):
    sanitized_str = html.escape(input_str)
    return sanitized_str


def action_insert(title, file, email, comment):
    email_validate = is_valid_email(email)
    if email_validate:
        title = sanitize_input(title)
        email = sanitize_input(email)
        comment = sanitize_input(comment)
        filename = secure_filename(sanitize_input(file.filename))
        s3 = S3Upload(
            aws_access_key_id=current_app.config.get('ACCESS_KEY'),
            aws_secret_access_key=current_app.config.get('SECRET_KEY'),
            bucket_name=current_app.config.get('BUCKET_NAME')
        )
        result = s3.upload_file(file, filename)
        if result is False:
            return False
        url = s3.get_file_url()
        data = {'title': title, 'filename': filename, 'comment': comment, 'email': email, 'url_signed': url}
        config = CoolConfig(
            current_app.config.get('USER_BDD'),
            current_app.config.get('PASSWORD'),
            current_app.config.get('DATABASE')
        )
        id_mongo = config.insert_data(data)
        subject = "Quelqu'un t'a envoyé un message qui s'éfface a 8am pile attention"
        message = (f"Envie de voir ce que c'est ;) clique sur ce lien  {current_app.config.get('URL')}display/"
                   f"{id_mongo}/")
        sns = EmailSender(
            aws_access_key_id=current_app.config.get('ACCESS_KEY'),
            aws_secret_access_key=current_app.config.get('SECRET_KEY'),
            topic_arn=current_app.config.get('TOPIC_ARN'),
            region_name=current_app.config.get('REGION')
        )
        sns.send_email(email, subject, message)
        return True
    else:
        return False


def display_action(object_id):
    config = CoolConfig(
        current_app.config.get('USER_BDD'),
        current_app.config.get('PASSWORD'),
        current_app.config.get('DATABASE')
    )
    return config.get_element(object_id)


def suppress_action():
    s3 = S3Upload(
        aws_access_key_id=current_app.config.get('ACCESS_KEY'),
        aws_secret_access_key=current_app.config.get('SECRET_KEY'),
        bucket_name=current_app.config.get('BUCKET_NAME')
    )
    s3.suppress_all_download()
    config = CoolConfig(
        current_app.config.get('USER_BDD'),
        current_app.config.get('PASSWORD'),
        current_app.config.get('DATABASE')
    )
    config.delete_element()

