# Flask S3 Browser

Creating a virtual environment is recommended.

Creating virtual environment using Python 3 installed with Homebrew:
```shell
virtualenv -p python3 venv --always-copy
source venv/bin/activate
```

Install Dependencies

```shell
pip install -r requirements.txt
```

## Configuration

Create a new file `.env` using the contents of `.env-sample`.

If you are not using the AWS CLI, modify sample-config with your AWS credentials and rename to "config.py"

## Fork Updates

Fixed uploader. Previously, the uploader would break if you didn't select a file when uploading.
Added allowed_files.py to set which file extensions can be uploaded. 
