# Project
## Role
### Student
- [ ] **When logged in as a student, what can a person see and do?**
    - [ ] (Students who aren't assigned to any project)
        - [ ] Show invites to become a member of already created projects
        - [ ] Create a project and become the Lead student (Must deny all invites first)

    - [ ] (Students who are already a member)
        - [ ] Permission to access and modify the project information
        - [ ] See project status 

    - [ ] (Students who are a Lead)
        - [ ] Request Advisor 
            - [ ] Add a new request to the `Advisor_pending_request` table (only one at a time)
        - [ ] See project status
        - [ ] Invite other student to the project (If the number of members in the group already exceeded 2, Lead can't sent out anymore invite)
        - [ ] See responses of the request sent out
        - [ ] Access and modify the project information
        - [ ] Submit
            - [ ] Proposal (If the project is just getting started)
            - [ ] Report (If the project is already done)  
### Faculty
- [ ] **When logged in as a faculty, what can a person see and do?**
    - [ ] (Normal Faculty)
        - [ ] See request to be a supervisor
        - [ ] Send out response
            - [ ] Accept (Become and serve as an advisor)
            - [ ] Deny (Stay the same)
        - [ ] See details of all the project
        - [ ] Evaluate project
    - [ ] (Advising Faculty)
        - [ ] See request to be a supervisor
        - [ ] Send out response
            - [ ] Accept
            - [ ] Deny 
        - [ ] See detail of all the project
        - [ ] Evaluate project
        - [ ] Approve the project
### Admin 
- [ ] **When logged in as an admin, what can a person see and do?**    
    - [ ] (Admin)
        - [ ] Can see and modify all data in database  

