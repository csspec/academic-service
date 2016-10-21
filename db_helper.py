from pymongo import MongoClient
import constants
from exceptions.CSSException import CSSException

client = MongoClient()

# The database for the service
db = client[constants.DB_NAME]

# The collection for storing the semesterId
semester_id_col = db[constants.SEMESTER_ID_COLLECTION]

# The collection for courses
courses_col = db[constants.COURSES_COLLECTION]

# The collection for student-course-teacher mapping
sct_col = db[constants.SCT_MAP]


def get_current_sem():
    """
    :return: The current semester Id from the database
    """
    resp = semester_id_col.find_one()
    print(resp)
    if resp is not None:
        return resp['current_sem']
    raise CSSException(501, constants.RESPONSE_MESSAGE_NOT_IMPLEMENTED)


def set_current_sem(current_sem):
    """
    Sets the current semester in the database
    :param current_sem:
    :return:
    """
    sem = dict()
    sem['current_sem'] = current_sem
    return semester_id_col.insert(sem)


def insert_into_courses(courses):
    """
    Inserts into the courses collection
    :param courses: The array of objects to be inserted into the collection
    :return:
    """
    courses_col.insert(courses)


def insert_into_sct(sct):
    """
    Inserts into the student-to-course-to-teacher mapping collection
    :param sct: The array of objects to be inserted
    :return:
    """
    sct_col.insert(sct)


def get_courses(req):
    """
    The public method which returns the result of querying the database for a GET on courses
    :param req: The request
    :return:
    """
    sct_filter = dict()

    if 'studentId' in req:
        studentId = req['studentId']
        sct_filter['studentId'] = studentId

    if 'teacherId' in req:
        teacherId = req['teacherId']
        sct_filter['teacherId'] = studentId

    if 'semesterId' in req:
        semesterId = req['semesterId']
        sct_filter['semesterId'] = semesterId
    else:
        sct_filter['semesterId'] = get_current_sem()

    # TODO: Check if size of sct_filter is one, and then only get uniques from the collection

    sct_result = get_courses_by_sct_map(sct_filter)

    # The final result to be returned
    result = []

    for doc in sct_result:
        course = courses_col.find({'courseId': doc['courseId']}, {'_id': False})
        course[0]['studentId'] = doc['studentId']
        course[0]['teacherId'] = doc['teacherId']
        course[0]['semesterId'] = doc['semesterId']

        result.append(course[0])

    return result


def get_courses_by_sct_map(query_filter):
    """
    Returns the courses by first filtering on student-course-teacher map
    :param query_filter: Dictionary with these keys (one or all) - `studentId`, `teacherId`, `semesterId`
    :return:
    """
    return sct_col.find(query_filter)

