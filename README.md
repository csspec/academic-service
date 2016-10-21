# academic-service
The service keeping track of all academic details of students and teachers.

## API reference
All API endpoints shall begin with `/academic` to call the Academic service.

### Schema 
All API access is over HTTPS. All data is sent and received as JSON.

##### Parameters
For GET requests, any parameters not specified as a segment in the path can be passed as an HTTP query string parameter:
~~~
curl -i https://api.pec.ac.in/academic/courses?semester=16172&departments=cse
~~~

For POST, PATCH, PUT, and DELETE requests, parameters not included in the URL should be encoded as JSON with a Content-Type of 'application/json'.

##### Summary and Detailed representations
When you fetch a list of resources, the response includes a subset of the attributes for that resource. This is the "summary" representation of the resource. (Some attributes are computationally expensive for the API to provide. For performance reasons, the summary representation excludes those attributes. To obtain those attributes, fetch the "detailed" representation.)

When you fetch an individual resource, the response typically includes all attributes for that resource. This is the "detailed" representation of the resource.
### Endpoints

#### Get the current semester
~~~
GET /academic/current-sem
~~~
Returns the `string` code for the current semester.

#### Get list of courses
~~~
GET /academic/courses
~~~
By default, returns all the courses being offered in the current semester in the college, in no particular order. Use the parameters as described below for a more predictable behaviour.

##### Parameters

| Name | Type | Description | 
| ---- | ---- | ----------- |
| `active` | `boolean` | If true, returns courses that are only being offered in the current semester, otherwise returns all matching courses. Defaults to true. |
| `studentId` | `string` | Returns the courses opted in by the `userId` |
| `teacherId` | `string` | Returns the courses taught by the `teacherId` |
| `departments` | `string` | Restricts the results to only courses offered by the specified departments |
| `semesterId` | `string` | Restricts the courses from a particular semester identified by `semester` id. Defaults to the current semester. | 

##### Getting course(s) by Id
Getting course(s) by Id is just a special case of the above method. Following parameters may be used independently or in conjunction with the above paramters.

| Name | Type | Description |
| ---- | ---- | ----------- |
| `id` | `string` | The `id`(s) of the courses to fetch. (Can be comma-separated list in the URL query parameter) |
| `isDetailed` | `boolean` | If true, returns the semester-variant information about the courses. Exact `teacherId` is only returned if the `userId` field is present, else all teachers are returned. | 