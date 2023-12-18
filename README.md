# Final Project Summary

- `database.py`: Contains the `Database and Table` class which provides methods to update and insert rows in different tables and act as a database to store data and have a function read_file and write_file which read the data in the csv file and write a new data or edit the data in the csv file.
- `project_manage.py`: Contains the operation of initializing, save, exit, login with methods for project management,
- `projects.csv`: empty csv file for storing data of created project
- `member_pending_request.csv` and `advisor_pending_request.csv`: empty csv file for storing data of each pending requests.

## How to compile and run

1. Git clone this repo
2. Run the file project_manage.py
3. Login into each role

## Roles and Actions.

| Role  | Action                  | Method        | Class   | Completion Percentage |
|-------|-------------------------|---------------|---------|-----------------------|
| Admin | View all data | `print`      | `Table` | 40%                  |
| Admin | Modify user data | `update_role_in_db` | `Table` | 100%         |
| Lead  | Request a member        | `insert`| `Table` | 100%                 |
| Lead | Request an advisor | `insert` | `Table` | 100%
| Lead | Submit proposal | `insert` | `Table` | 30%
| Lead | Submit proposal | `insert` | `Table` | 30%
| Lead | View/Edit project | `insert` | `Table`| 100% 
| Faculty | View advisor request | `search`| `Database` | 100%
| Faculty | Approve/Deny Advisor request | `insert`| `Table`| 100%
| Faculty | View all projects | `search` | `Database`| 100%
| Student | View Project invitation | `search` | `Database` |  100%
| Student | Create a project | `update_role_in_db`| `Table` |100%
| Student | Join a project | `insert`|`Table`| 100
| Member| View/Edit project| `insert`| `Table`| 100%
| Member | See project status | `search`, `print`| `Database`| 100%
| Advisor | Approve project| `insert`| `Table`| 70%
| Advisor | Send evaluation request | `insert`| `Table` | 70%
| Advisor | View all projects | `search`, `print`| `Database` | 100%
|Committee| Approve project evaluation | `insert` | `Table`| Assuming around 30%, this whole features of evaluation is still missing|

## Missing Features and Bugs
Here are the known issues and incomplete features for each role:
- **Evaluation step features**
  - Only have a committee role and the rest is incomplete
- **Faculty Role**
  - Missing feature: accept a request from an advisor to become a committee to evaluate the project
- **Advisor Role** 
  - Missing feature: send a request to a faculty to become a comittee for evaluation process
- **Admin Role** 
  - Missing feature: edit a data of member_request_table and advisor_request_table, change the status of project.
- **Bugs**
  - Current bugs are in the choice of admin menu where when you choose to view all data an error occurs telling that NoneType object has no table attribute.


