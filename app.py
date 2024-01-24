import os

from apscheduler.triggers.cron import CronTrigger
from flask import Flask, render_template, request, flash, redirect
from flask.cli import load_dotenv
from flask_apscheduler import APScheduler
from Action import action_insert, display_action, suppress_action

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


class Config:
    SCHEDULER_API_ENABLED = True


load_dotenv()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BUCKET_NAME'] = os.getenv('BUCKET_NAME')
app.config['REGION'] = os.environ.get('REGION')
app.config['ACCESS_KEY'] = os.environ.get('ACCESS_KEY')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['TOPIC_ARN'] = os.environ.get('TOPIC_ARN')
app.config['USER_BDD'] = os.environ.get('USER_BDD')
app.config['PASSWORD'] = os.environ.get('PASSWORD')
app.config['DATABASE'] = os.environ.get('DATABASE')
app.config['URL'] = os.environ.get('URL')


def job1():
    print('Job 1 executed')
    suppress_action()


app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(func=job1, id='my_job_id', trigger=CronTrigger.from_crontab('0 8 * * *', 'UTC'))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            print("hello")
            return redirect(request.url)
        if 'title' not in request.form:
            print("hello1")
            return redirect(request.url)
        if 'email' not in request.form:
            print("hello2")
            return redirect(request.url)
        if 'comment' not in request.form:
            print("hello4")
            return redirect(request.url)
        file = request.files['file']
        title = request.form['title']
        email = request.form['email']
        comment = request.form['comment']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            result = action_insert(title, file, email, comment)
            if result is True:
                return render_template('good.html')
            else:
                return render_template('upload.html')

    return render_template('upload.html')


@app.route('/display/<string:identifier>/', methods=['GET'])
def display_html(identifier):
    if request.method == 'GET':
        object_id = identifier
        result = display_action(object_id)
        return render_template('display.html', file=result)


@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        suppress_action()
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
