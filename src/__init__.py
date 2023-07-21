from flask import Flask, request, make_response
from werkzeug.utils import secure_filename

import s3_client as s3


VALID_FILE_TYPES = set(['csv', 'm4a', 'mp4', 'jpeg', 'txt'])

def validate_file_type(file):
	return '.' in file and file.rsplit('.', 1)[1].lower() in VALID_FILE_TYPES


app = Flask(__name__)

@app.route('/bucket', methods=['POST'])
def create_bucket():
    args = request.args
    session_id = args["session_id"]
    
    # can session_id here (string, numbers, length, etc)

    response = s3.create_session_bucket(session_id)

    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': f'Create Bucket: session-{session_id} Successful',
        }
    return make_response ({'msg': f'Something went wrong when creating a S3 bucket. Response: {response}'}, 400)


@app.route('/bucket', methods=['DELETE'])
def delete_bucket():
    args = request.args
    session_id = args["session_id"]
    response = s3.delete_bucket(session_id)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': f'Delete bucket: session-{session_id} Successful',
        }
    return make_response ({'msg': f'Something went wrong when deleting a S3 bucket. Response: {response}'}, 400)


#TODO: update file format for Flask
@app.route('/object', methods=['POST'])
def create_object():
    args = request.args
    session_id = args["session_id"]

    if 'file' not in request.files:
        return make_response({'message' : 'No file part in the request'}, 400)
    
    file = request.files['file']
    if file.filename == '':
        return make_response({'message' : 'No file selected for uploading'}, 400)

    if file and validate_file_type(file.filename):
        file_name = secure_filename(file.filename)
        response = s3.upload_object_to_bucket(session_id, file)

        if ('ResponseMetadata' in response and response['ResponseMetadata']['HTTPStatusCode'] == 200):
            return {
                'msg': f'Create object: {file_name} Successful',
            }

        return make_response({'message' : f'Something went wrong uploading the file {response}'}, 400)


@app.route('/object', methods=['GET'])
def get_object():
    args = request.args
    session_id = args["session_id"]
    object_name = args["object_name"]
    path = args["path"]

    # Should validate path here

    response = s3.get_object(session_id, object_name, path)
    if "Success" in response:
        return {
            'msg': response,
        }
    return make_response({'message' : f'Something went wrong getting the file {response}'}, 400)


@app.route('/object', methods=['DELETE'])
def delete_object():
    args = request.args
    session_id = args["session_id"]
    object_name = args["object_name"]
    response = s3.delete_object(session_id, object_name)
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': f'Delete object: {object_name} Successful',
        }
    return make_response({'message' : f'Something went deleting the file {response}'}, 400)


if __name__ == '__main__':
    app.run(port=8888)
