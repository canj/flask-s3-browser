from flask import Flask, render_template, request, redirect, url_for, flash, \
    Response, session
from flask_bootstrap import Bootstrap
import boto3
from resources import get_bucket, get_buckets_list
from config import S3_BUCKET, S3_KEY, S3_SECRET
from filters import datetimeformat, file_type
import allowed_files as af

s3_resource = boto3.resource(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'secret'
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in af.ALLOWED_EXT


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bucket = request.form['bucket']
        session['bucket'] = bucket
        return redirect(url_for('files'))
    else:
        buckets = get_buckets_list()
        return render_template("index.html", buckets=buckets)


@app.route('/files')
def files():
    my_bucket = get_bucket()
    summaries = my_bucket.objects.all()

    return render_template('files.html', my_bucket=my_bucket, files=summaries)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has a file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('files'))
        file = request.files['file']
        # if user does not select file
        if file.filename == '':
            flash('No Selected File')
            return redirect(url_for('files'))
        # If the file is selected
        if file and allowed_file(file.filename):
            my_bucket = get_bucket()
            my_bucket.Object(file.filename).put(Body=file)

            flash('File uploaded successfully')
            return redirect(url_for('files'))
        # If uploading a file with extension not in allowed_files.py
        else:
            flash('File type Not Supported')
            return redirect(url_for('files'))

@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket = get_bucket()
    my_bucket.Object(key).delete()

    flash('File deleted successfully')
    return redirect(url_for('files'))


@app.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    my_bucket = get_bucket()
    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )


if __name__ == "__main__":
    app.run()
