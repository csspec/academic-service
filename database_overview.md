# Overview of the Database Schema
This document covers the basic schema for the Academic service database. "Schema" here refers to the rough fields of each Collection in MongoDB.
 
There are two kinds of Collections at high level: **Semester Variant** and **Semester Invariant**. 

*Semester Variant* is a collection that stores its data mainly for the semester. At the end of the semester, this kind of collection is usually archived. Example, the student to courses mapping - since students shall be opting for different courses every semester.

*Semester Invariant* is a collection that has data for multiple semesters. Example, the courses that are offered by each department usually remain the same across different semesters.
 
## Available Collections
#### Courses
It is a semester-invariant collection that stores with itself all the details of various courses offered by different departments.

Fields:

| Field Name | Type | Description |
| ---------- | ---- | ----------- | 
| `courseId` | `string` | Denotes the unique Id of the course |
| `offeredBy`| `string` | Denotes the 3-lettered department code of the department that offers this course |
| `name` | `string` | The full name of the course |
| `description` | `string` | A brief description of the course |

#### StudentToCourse mapping
It is a semester-variant collection that stores the mapping of Students to Courses, that is, it keeps track of what all courses are opted by a student in what semester.

Fields:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| `semesterId` | `string` | The unique Id identifying a semester |
| `studentId` | `string` | The unique Id identifying a student |
| `courses` | Array of `strings` | An array of strings representing the courses opted by the particular student. Each `string` in the array is a `courseId` representing the course |

#### CourseToTeacher mapping
It is a semester-variant collection that stores the mapping of Courses to Teacher(s), that is, it keeps a track of which teacher is teaching what subject to (optionally) what students.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| `semesterId` | `string` | The unique Id identifying a semester |
| `courseId` | `string` | The unique Id identifying a course |
| `isTaughtByMultiple` | `boolean` | Flag, which set to true, means that this course is taught by multiple teachers. False otherwise |
| `teachers` | Array of objects | An array of objects describing which teacher is teaching to what classes (see below) |

An additional explanation is required for the field `teachers`.

`teachers` field for a course with multiple teachers would look like:

~~~
[
    {
        teacherId: "asxcvf325", // the unique teacherId
        range: ["13103001-13103050", "13105024-13105063","12103002"] // the range of students the teacher is teaching
    },
    {
        teacherId: "iujkk23tg",
        range: ["13105001-13105023"]
    }
]
~~~
 
`teachers` field for a course with one teacher would not contain the field `range` and would look like the following for uniformity:

~~~
[
    {
        teacherId: "asccg24c", // the unique id of the teacher
    }
]
~~~

The flag `isTaughtByMultiple` should make the parsing more predictable. The `range` field can be more thought after and changed in near-future over better alternatives.

