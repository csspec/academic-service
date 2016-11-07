import academicservice.constants as constants
from pymongo import MongoClient

from academicservice.exceptions.CSSException import CSSException

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
    :param courses: The array of objects(dictionaries) to be inserted into the collection
    :return:
    """
    for course in courses:
        if 'courseId' not in course:
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "courseId is invalid")
        if 'offeredBy' not in course:
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "offeredBy is invalid")
        if 'name' not in course:
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "name is invalid")
        # if 'credits' not in course:
        #     raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "credits is invalid")
        # if 'ltp' not in course:
        #     raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "ltp is invalid")

    courses_col.insert(courses)


def insert_into_sct(scts):
    """
    Inserts into the student-to-course-to-teacher mapping collection
    :param scts: The array of objects to be inserted
    :return:
    """
    for sct in scts:
        if 'courseId' not in sct:
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "courseId is not valid")
        if 'studentId' not in sct:
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "studentId is not valid")
        if 'teacherId' not in sct:
            raise CSSException(400, constants.RESPONSE_MESSAGE_BAD_REQUEST, "courseId is not valid")
        if 'semesterId' not in sct:
            sct['semesterId'] = get_current_sem()

    sct_col.insert(scts)


def get_courses(req):
    """
    The public method which returns the result of querying the database for a GET on courses
    :param req: The request
    :return:
    """
    sct_filter = dict()

    studentId = None
    if 'studentId' in req:
        studentId = req['studentId']
        sct_filter['studentId'] = studentId

    teacherId = None
    if 'teacherId' in req:
        teacherId = req['teacherId']
        sct_filter['teacherId'] = teacherId

    if 'semesterId' in req:
        semesterId = req['semesterId']
    else:
        semesterId = get_current_sem()

    sct_filter['semesterId'] = semesterId

    sct_result = get_courses_by_sct_map(sct_filter)

    courses = []
    if 'isDetailed' in req:
        if req['isDetailed'] == "true":
            courses = __get_courses_with_variant_info(sct_result, studentId)
    else:
        courses = __get_courses_without_variant(sct_result)

    courses_final = []
    if 'offeredBy' in req:
        for i, val in enumerate(courses):
            if val['offeredBy'] == req['offeredBy']:
                courses_final.append(val)
        return courses_final
    else:
        return courses


def get_courses_by_sct_map(query_filter):
    """
    Returns the courses by first filtering on student-course-teacher map
    :param query_filter: Dictionary with these keys (one or all) - `studentId`, `teacherId`, `semesterId`
    :return:
    """
    return sct_col.find(query_filter)


def __get_courses_with_variant_info(sct_result, studentId):
    """
    Gets an array of documents of courses with their relevant `studentId`, `teacherId` and `semesterId` triplet
    :param sct_result: The Cursor instance of results returned by calling on sct map
    :return:
    """
    result = []
    if studentId is None:
        return __get_courses_without_variant(sct_result)

    courseIds = []

    for doc in sct_result:
        courseId = doc['courseId']
        if doc['courseId'] not in courseIds:
            courseIds.append(courseId)
            course = courses_col.find({'courseId': courseId}, {'_id': False})

            temp_course = dict()
            temp_course = course[0]
            temp_course['studentId'] = studentId
            temp_course['teacherId'] = doc['teacherId']
            temp_course['semesterId'] = doc['semesterId']

            result.append(temp_course)

    return result


def __get_courses_without_variant(sct_result):
    """
    Gets an array of documents of courses without any student/teacher details
    :param sct_result: The Cursor instance of results returned by calling on sct map
    :return:
    """
    result = []
    sct_result = sct_result.distinct("courseId")

    for courseId in sct_result:
        course = courses_col.find({'courseId': courseId}, {'_id': False})
        #course[0]['semesterId'] = courseId['semesterId']
        result.append(course[0])

    return result


def get_students(req):
    """
    Method which returns the studentIds based on certain filters
    :param req: request dictionary
    :return: Array of studentIds which matched
    """
    query = dict()

    students = []

    if 'courseId' in req:
        query['courseId'] = req['courseId']

    query_result = sct_col.find(query, {"_id": False})

    for sct_row in query_result:
        students.append(sct_row['studentId'])

    return students
