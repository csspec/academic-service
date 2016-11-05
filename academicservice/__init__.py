from flask import Flask, request, make_response, jsonify
from flask_cors import CORS

import academicservice.constants as constants
import academicservice.db_helper as db_helper
from academicservice.exceptions.CSSException import CSSException

app = Flask(__name__)
CORS(app)


@app.route(constants.API_PATH_PREFIX + constants.API_PATH_COURSES, methods=['GET'])
def get_courses():
    """
    The method to handle a GET request to the courses resource
    :return:
    """
    token = request.args.get('token')
    if token is None or verify_token(token) is False:
        raise CSSException(401, constants.RESPONSE_MESSAGE_UNAUTHORIZED)

    req = get_request_for_courses()
    res = dict()
    res['data'] = dict()
    res['data']['items'] = db_helper.get_courses(req)

    return make_response(jsonify(res), 200)


@app.route(constants.API_PATH_PREFIX + constants.API_PATH_CURRENT_SEM, methods=['GET'])
def get_current_semester():
    """
    The method to handle GET /academic/current-sem
    :return:
    """
    token = request.args.get('token')
    if token is None or verify_token(token) is False:
        raise CSSException(401, constants.RESPONSE_MESSAGE_UNAUTHORIZED)

    current_sem = db_helper.get_current_sem()

    response = dict()
    response['data'] = dict()
    response['data']['current-sem'] = current_sem

    return make_response(jsonify(response), 200)


def verify_token(token):
    """
    The function that verifies a given token by calling Auth service
    :return: The token returned by Auth if token is valid, False otherwise
    """
    return True


def get_request_for_courses():
    """
    Constructs a dictionary for a request object for GET /courses
    :return:
    """
    req = dict()

    active = request.args.get("active")
    if active is not None:
        if not (active is "true" or active is "false"):
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "key `active` is not boolean value")
        req['active'] = active
    else:
        req['active'] = "true"

    studentId = request.args.get("studentId")
    if studentId is not None:
        req['studentId'] = studentId

    teacherId = request.args.get("teacherId")
    if teacherId is not None:
        req['teacherId'] = teacherId

    semester = request.args.get("semesterId")
    if semester is not None:
        req['semesterId'] = semester

    courseId = request.args.get("id")
    if courseId is not None:
        req['courseId'] = courseId

    isDetailed = request.args.get("isDetailed")
    if isDetailed is not None:
        if not (isDetailed == "true" or isDetailed == "false"):
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "key 'isDetailed' is not boolean value")
        req['isDetailed'] = isDetailed

    return req


@app.route(constants.API_PATH_PREFIX + constants.API_PATH_COURSES, methods=['POST'])
def add_course():
    """
    Route to add a new course
    :return:
    """
    # TODO: Check authorization before adding
    req = request.get_json()
    data = req['data']
    if not isinstance(data, list):
        raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "data is not an array (list)")

    db_helper.insert_into_courses(data)

    res = dict()
    res['data'] = dict()
    res['data']['status'] = "success"
    return make_response(jsonify(res), 201)


@app.route(constants.API_PATH_PREFIX + constants.API_PATH_SCT_COLLECTION, methods=['POST'])
def add_sct():
    """
    The endpoint for inserting into the SCT collection
    :return:
    """
    # TODO: Check authorizations before adding
    req = request.get_json()
    data = req['data']
    if not isinstance(data, list):
        raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "data is not an array (list)")

    db_helper.insert_into_sct(data)

    res = dict()
    res['data'] = dict()
    res['data']['status'] = "success"

    return make_response(jsonify(res), 201)


@app.route(constants.API_PATH_PREFIX + constants.API_PATH_CURRENT_SEM, methods=['POST'])
def set_current_sem():
    """
    The endpoint to set the current semester
    :return:
    """
    # TODO: Check the authorizations
    req = request.get_json()
    data = req['data']
    if not isinstance(data, dict):
        raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "data must be a dictionary")

    if 'current-sem' not in data:
        raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "current-sem key is missing")
    sem = data['current-sem']
    if len(sem) != 5:
        raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "current-sem value is incorrect")

    db_helper.set_current_sem(sem)

    res = dict()
    res['data'] = dict()
    res['data']['status'] = "success"

    return make_response(jsonify(res), 201)


@app.errorhandler(CSSException)
def bad_request(error):
    return make_response(error.to_json(), error.status_code)


@app.errorhandler(404)
def not_found(error):
    exception = CSSException(404, constants.RESPONSE_MESSAGE_NOT_FOUND)
    return make_response(exception.to_json(), exception.status_code)


@app.errorhandler(400)
def bad_request(error):
    exception = CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST)
    return make_response(exception.to_json(), exception.status_code)

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')
