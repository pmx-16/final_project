# Final Project Summary

- `database.py`: Contains the `Database and Table` class which provides methods to update and insert rows in different tables and act as a database to store data and have a function read_file and write_file which read the data in the csv file and write a new data or edit the data in the csv file.
- `project_manage.py`: Contains the operation of initializing, save, exit, login with methods for project management,
- `projects.csv`: empty csv file for storing data of created project
- `member_pending_request.csv` and `advisor_pending_request.csv`: empty csv file for storing data of each pending requests.

## How to compile and run

1. Git clone this repo
2. Run the file project_manage.py
3. Login into each role


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


