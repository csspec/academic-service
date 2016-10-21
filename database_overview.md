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
| `credits` | `integer` | The number of credits of the course |
| `ltp` | `string` | Dash (-) separated numbers specifying the Lecture-Tutorials-Practical for the course |

#### StudentToCourse mapping
It is a semester-variant collection that stores the mapping of Students to Courses, that is, it keeps track of what all courses are opted by a student in what semester.

Fields:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| `semesterId` | `string` | The unique Id identifying a semester |
| `studentId` | `string` | The unique Id identifying a student |
| `courses` | Array of `strings` | An array of strings representing the courses opted by the particular student. Each `string` in the array is a `courseId` representing the course |

#### Semester-Variant Student-to-course-to-teacher mapping
It is a semester-variant collection that stores the mapping of particular student to the course to the teacher teaching to that particular student. This collection has been discussed in <a href="https://github.com/csspec/academic-service/issues/1">this</a> issue.
Please read this issue for an explanation on data redundancy concerns.

Fields:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| `semesterId` | `string` | The unique Id identifying a semester | 
| `studentId` | `string` | The unique Id identifying a student |
| `courseId` | `string` | The Id of the course |
| `teacherId` | `string` | The unique Id identifying a teacher |

#### Departments
It is a semester invariant collection that stores the information about a particular department.

Fields:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| `departmentId` | `string` | The unique department identifier |
| `name` | `string` | The name of the department |

`departmentId` is proposed to be a 3-letter department code so that all services in the ecosystem can use it independently without any network call.

| Department Id | Department Name |
| ------------- | --------------- |
| "AER" | Aeronautical |
| "CIV" | Civil |
| "CSE" | Computer Science |
| "EEE" | Electrical |
| "ECE" | Electronics & Communication |
| "MEC" | Mechanical |
| "MET" | Metallurgy | 
| "PRO" | Production |