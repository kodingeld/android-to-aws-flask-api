# android-to-aws-flask-api

This Flask RESTful API uses the Python AWS SDK to communicate to AWS S3.

## Configuration
In order to communicate to AWS Resource, set up the `config.py` with AWS credentials.
It should look something like this:
```
AWS_ACCESS_KEY_ID = 'accessid'
AWS_SECRET_ACCESS_KEY = 'secretaccesskey'
REGION_NAME = 'regionname'
```

IMPORTANT: make sure that these credentials DO NOT get uploaded to public repos.
* An alternative option would be alter this project to use virtual environments instead

## Setting up virtual environment
To run this Flask server, activate the virtual environment

To create a python virtual environment, run:
`python3 -m venv venv`

To activate the virtual environment, run:
`source venv/bin/activate `

To install the required dependencies, run:
`pip3 install -r requirements.txt`

## Running the Flask App locally
Run the Flask Server by inputting `python __init__.py`

## Uploading the Flask App to AWS Elastic Beanstalk
1. Install the Elastic Beanstalk CLI
2. Initalize by running `eb init -p <python ver> <app name> --region <region>`
3. Generate a keypair to SSH to EC2 `eb init`
4. Create and deploy `eb create <app name>`

### Misc
* Note that `file` and `object` are used interchangeably
* Session_id refers to the identifier for how the files are grouped