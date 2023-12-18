import os
import csv
from database import Database, Table, read_file, write_file

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def initializing(data_directory):
    db = Database()
    csv_files = [f for f in os.listdir(data_directory) if f.endswith(".csv")]

    for file in csv_files:
        try:
            table_name = file.split('.')[0]
            full_path = os.path.join(data_directory, file)
            if os.path.getsize(full_path) > 0:
                table_data = read_file(full_path)
            else:
                table_data = []  # Initialize an empty table if file is empty
            new_table = Table(table_name, table_data)
            db.insert(new_table)
            print(f"Table '{table_name}' added to the database with {len(table_data)} records.")
        except Exception as e:
            print(f"Error initializing table '{table_name}': {e}")

    # Print out all table names added to the database
    print("All loaded tables:")
    for table in db._database:
        print(f"Loaded table: {table.table_name}")

    return db


def login(db):
    username_input = input("Enter your username: ")
    pass_input = input("Password: ")

    # Authenticate using login table
    login_table = db.search('login')
    if login_table:
        valid_login = next((user for user in login_table.table if user['username'] == username_input and user['password'] == pass_input), None)
        if valid_login:
            user_id = valid_login['ID']

            # Fetch user role from persons table
            persons_table = db.search('persons')
            if persons_table:
                user_record = next((person for person in persons_table.table if person['ID'] == user_id), None)
                if user_record:
                    return user_record['ID'], user_record['type']
                else:
                    print("User record not found.")
                    return None

    print("Access denied. Please check your credentials.")
    return None



def student_activities(db, user_id):
    projects_table = db.search('projects')
    invitations_table = db.search('member_pending_request')

    while True:
        print("\nStudent Menu:")
        print("1. View Project Invitations")
        print("2. Create New Project")
        print("3. Join a Project")
        print("0. Exit or Log out")

        choice = input("Enter your choice: ")
        invitations = [inv for inv in invitations_table.table if inv['to_be_member'] == user_id and inv['Response'] == 'pending']

        if choice == '1':
            # View project invitations 
            print("Project Invitations:")
            for inv in invitations:
                print(f"Project ID: {inv['ProjectID']}, Status: {inv['Response']}")

        elif choice == '2':
            # Create new project
            # Check if there are pending invitations
            if any(inv['Response'] == 'pending' for inv in invitations):
                print("You must deny all invitations before creating a new project.")
            else:
                new_project_id = input("Enter new Project ID: ")
                new_project_title = input("Enter new Project Title: ")
                projects_table.insert({'ProjectID': new_project_id, 'Title': new_project_title, 'Lead': user_id, 'Status': 'pending'})
                new_role = 'lead'
                update_role_in_db(db, user_id, new_role)
                print(f"New project '{new_project_title}' created. You are now the lead.")
                lead_activities(db, user_id) 
                return 

        elif choice == '3':
            # Join a project 
            project_id = input("Enter Project ID to join: ")
            selected_project = next((p for p in projects_table.table if p['ProjectID'] == project_id), None)
            if selected_project and ('Member1' not in selected_project or 'Member2' not in selected_project):
                if 'Member1' not in selected_project:
                    selected_project['Member1'] = user_id
                else:
                    selected_project['Member2'] = user_id
                new_role = 'member'
                update_role_in_db(db, user_id, new_role)
                print(f"Joined project: {selected_project['Title']} as a member.")
                member_activities(db, user_id)  
                return  

        elif choice == '0':
            break

def member_activities(db, user_id):
    projects_table = db.search('projects')

    while True:
        print("\nMember Menu:")
        print("1. View/Edit My Project")
        print("2. See Project Status")
        print("0. Exit or Log out")

        choice = input("Enter your choice: ")

        if choice == '1':
            # View/Edit My Project 
            my_projects = [p for p in projects_table.table if user_id in (p.get('Member1'), p.get('Member2'))]
            if not my_projects:
                print("You are not part of any project.")
                continue

            print("Your Projects:")
            for proj in my_projects:
                print(f"Project ID: {proj['ProjectID']}, Title: {proj['Title']}")

            edit_id = input("Enter the Project ID to edit or 'exit' to return: ")
            if edit_id.lower() == 'exit':
                continue

            selected_project = next((p for p in my_projects if p['ProjectID'] == edit_id), None)
            if selected_project:
                new_title = input("Enter new title for the project: ")
                selected_project['Title'] = new_title
                print("Project title updated.")
            else:
                print("Project not found.")

        elif choice == '2':
            # See Project Status 
            my_projects = [p for p in projects_table.table if user_id in (p.get('Member1'), p.get('Member2'))]
            if not my_projects:
                print("You are not part of any project.")
                continue

            for proj in my_projects:
                print(f"Project ID: {proj['ProjectID']}, Status: {proj['Status']}")

        elif choice == '0':
            break

def lead_activities(db, user_id):
    projects_table = db.search('projects')
    member_requests_table = db.search('member_pending_request')
    advisor_requests_table = db.search('advisor_pending_request')

    while True:
        print("\nLead Menu:")
        print("1. View/Edit My Project")
        print("2. Send Member Requests")
        print("3. Send Advisor Requests")
        print("4. View Project Status")
        print("5. Submit Proposal")
        print("6. Submit Report")
        print("0. Exit or Log out")
        choice = input("Enter your choice: ")
        my_project = next((p for p in projects_table.table if p['Lead'] == user_id), None)

        if choice == '1':
            # View/Edit my project logic
            print(f"Project ID: {my_project['ProjectID']}, Title: {my_project['Title']}, Status: {my_project['Status']}")
            edit_choice = input("Do you want to edit the title? (yes/no): ").lower()
            if edit_choice == 'yes':
                new_title = input("Enter new title: ")
                my_project['Title'] = new_title
                print("Project title updated.")

        elif choice == '2':
            # Logic to send member requests
            potential_member_id = input("Enter the ID of the student to invite: ")
            # Assume member_requests_table is fetched from the database
            member_requests_table.insert({'ProjectID': my_project['ProjectID'], 'to_be_member': potential_member_id, 'Response': 'pending'})
            print(f"Member request sent to user ID {potential_member_id}.")

        elif choice == '3':
            # Logic to send advisor requests
            potential_advisor_id = input("Enter the ID of the faculty to invite as an advisor: ")
            # Assume advisor_requests_table is fetched from the database
            advisor_requests_table.insert({'ProjectID': my_project['ProjectID'], 'to_be_advisor': potential_advisor_id, 'Response': 'pending'})
            print(f"Advisor request sent to faculty ID {potential_advisor_id}.")

        elif choice == '4':
            # Submit Proposal logic
            print("Submitting proposal for project ID: " + my_project['ProjectID'])
            # Simulate proposal submission
            print("Proposal submitted. Waiting for advisor approval.")

        elif choice == '5':
            # Submit Report logic
            print("Submitting report for project ID: " + my_project['ProjectID'])
            # Simulate report submission
            print("Report submitted. Waiting for advisor approval.")

        elif choice == '0':
            break

def faculty_activities(db, user_id):
    projects_table = db.search('projects')
    advisor_requests_table = db.search('advisor_pending_request')

    while True:
        print("\nFaculty Menu:")
        print("1. View Advisor Requests")
        print("2. Approve/Deny Advisor Requests")
        print("3. View All Projects")
        print("0. Exit or Log out")
        choice = input("Enter your choice: ")

        if choice == '1':
            # View advisor requests 
            print("Advisor Requests:")
            found_requests = False
            for request in advisor_requests_table.table:
                if request['to_be_advisor'] == user_id and request['Response'] == 'pending':
                    print(f"Project ID: {request['ProjectID']}, Request Status: {request['Response']}")
                    found_requests = True
            if not found_requests:
                print("No pending advisor requests.")

        elif choice == '2':
            # Approve/Deny advisor requests 
            project_id = input("Enter Project ID to respond to: ")
            selected_request = next((r for r in advisor_requests_table.table if r['ProjectID'] == project_id and r['to_be_advisor'] == user_id), None)
            if selected_request:
                response = input("Accept (yes) or Deny (no): ").lower()
                if response == 'yes':
                    selected_request['Response'] = 'Approved'
                    new_role = 'advisor'
                    update_role_in_db(db, user_id, new_role)
                    print(f"Advisor request for Project ID {project_id} approved. You are now an advisor.")
                    
                    advisor_activities(db, user_id)  
                    return  
                elif response == 'no':
                    selected_request['Response'] = 'Denied'
                    print(f"Advisor request for Project ID {project_id} denied.")
            else:
                print("Project request not found.")

        elif choice == '3':
            # View all projects 
            print("All Projects:")
            for project in projects_table.table:
                print(f"Project ID: {project['ProjectID']}, Title: {project['Title']}, Status: {project['Status']}")

        elif choice == '0':
            break

def advisor_activities(db, user_id):
    projects_table = db.search('projects')

    print("\nAdvisor Menu:")
    print("1. View Supervisor Requests")
    print("2. Respond to Supervisor Requests")
    print("3. View All Projects")
    print("4. Evaluate and Approve Projects")
    print("0. Exit or Log out")

    while True:
        choice = input("Enter your choice: ")

        if choice == '1':  
                print("Projects pending approval:")
                for project in projects_table.table:
                    if project['Status'] in ['Proposal submitted', 'Report submitted']:
                        print(f"Project ID: {project['ProjectID']}, Current Status: {project['Status']}")
                        decision = input(f"Approve Project ID {project['ProjectID']}? (yes/no): ").lower()
                        if decision == 'yes':
                            if project['Status'] == 'Proposal submitted':
                                project['Status'] = 'Proposal approved'
                            elif project['Status'] == 'Report submitted':
                                project['Status'] = 'Report approved'
                            print(f"Project ID {project['ProjectID']} status updated to {project['Status']}.")
                        else:
                            print(f"Approval denied for Project ID {project['ProjectID']}.")

        elif choice == '2':
                # Send evaluation requests logic
                print("Projects eligible for Evaluation Request:")
                eligible_projects = [project for project in projects_table.table if project.get('Advisor') == user_id and project['Status'] == 'Report approved']
                for project in eligible_projects:
                    print(f"Project ID: {project['ProjectID']}, Title: {project['Title']}")

                project_id = input("Enter the Project ID to send evaluation request: ")
                selected_project = next((p for p in eligible_projects if p['ProjectID'] == project_id), None)
                if selected_project:
                    selected_project['Status'] = 'Evaluation pending'
                    print(f"Evaluation request sent for Project ID {project_id}. Status updated to 'Evaluation pending'.")
                else:
                    print("No action has taken")

        elif choice == '3':
            # View all projects 
            print("All Projects:")
            for project in projects_table.table:
                print(f"Project ID: {project['ProjectID']}, Title: {project['Title']}, Status: {project['Status']}")

        elif choice == '0':
            break

def committee_activities(db, user_id):
    projects_table = db.search('projects')

    while True:
        print("\nCommittee Menu:")
        print("1. Approve Project Evaluation Requests")
        print("0. Exit or Log out")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Approve project evaluation requests
            pending_evaluations = [project for project in projects_table.table if project['Status'] == 'Evaluation pending']
            if not pending_evaluations:
                print("No pending evaluation requests.")
                continue

            print("Projects awaiting evaluation:")
            for project in pending_evaluations:
                print(f"Project ID: {project['ProjectID']}, Title: {project['Title']}")

            project_id = input("Enter the Project ID to approve: ")
            selected_project = next((p for p in pending_evaluations if p['ProjectID'] == project_id), None)
            if selected_project:
                approval_decision = input("Approve this project? (yes/no): ").lower()
                if approval_decision == 'yes':
                    selected_project['Status'] = 'Project approved'
                    print(f"Project ID {project_id} has been approved.")
                else:
                    print(f"Project ID {project_id} not approved.")
            else:
                print("Project not found or not eligible for evaluation.")

        elif choice == '0':
            break

def admin_activities(db):
    login_table = db.search('login')
    projects_table = db.search('projects')
    while True:
        print("\nAdmin Menu:")
        print("1. View All Data")
        print("2. Modify User Data")
        print("3. Manage Projects")
        print("0. Exit or Log out")
        choice = input("Enter your choice: ")

        if choice == '1':
            # View all data 
            for table_name in db._database:
                table = db.search(table_name)
                print(f"\nTable: {table_name}")
                for record in table.table:
                    print(record)

        elif choice == '2':
            # Modify user data 
            user_id = input("Enter the user ID to modify: ")
            user = next((u for u in login_table.table if u['ID'] == user_id), None)
            if user:
                new_role = input("Enter new role for this user: ")
                user['role'] = new_role
                print(f"User {user_id} role updated to {new_role}.")
                update_role_in_db(db, user_id, new_role)
            else:
                print("User not found.")

        elif choice == '3':
            # Manage projects 
            projects_table = db.search('projects')
            if not projects_table:
            # If projects_table doesn't exist, create it with the appropriate structure
                projects_table = Table('projects', [])
            db.insert(projects_table)
            action = input("Choose action (add/edit/delete): ").lower()
            if action == 'add':
                new_project_id = input("Enter new project ID: ")
                new_project_title = input("Enter new project title: ")
                projects_table.insert({'ProjectID': new_project_id, 'Title': new_project_title, 'Status': 'pending'})
                print(f"Project {new_project_id} added.")
            elif action == 'edit':
                project_id = input("Enter the project ID to edit: ")
                project = next((p for p in projects_table.table if p['ProjectID'] == project_id), None)
                if project:
                    new_title = input("Enter new title for the project: ")
                    project['Title'] = new_title
                    print(f"Project {project_id} title updated.")
                else:
                    print("Project not found.")
            elif action == 'delete':
                project_id = input("Enter the project ID to delete: ")
                project = next((p for p in projects_table.table if p['ProjectID'] == project_id), None)
                if project:
                    projects_table.table.remove(project)
                    print(f"Project {project_id} deleted.")
                else:
                    print("Project not found.")

        elif choice == '0':
            break

def update_role_in_db(db, user_id, new_role):
    # Fetch persons table
    persons_table = db.search('persons')
    if persons_table:
        # Find the user and update the role
        for person in persons_table.table:
            if person['ID'] == user_id:
                person['type'] = new_role
                break
        # Save changes to the CSV file
        save_table_to_csv(persons_table, 'persons.csv')

def save_table_to_csv(table, filename):
    data_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    file_path = os.path.join(data_directory, filename)
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=table.table[0].keys())
        writer.writeheader()
        writer.writerows(table.table)

def exit(db, data_directory):
    for table in db._database:
        file_path = os.path.join(data_directory, f"{table.table_name}.csv")
        try:
            if table.table:
                fieldnames = table.table[0].keys()
                print(f"Writing table '{table.table_name}' with fieldnames: {fieldnames}")
                write_file(file_path, table.table)
            else:
                print(f"Table '{table.table_name}' is empty, no data to write.")
        except Exception as e:
            print(f"Error writing table '{table.table_name}': {e}")

def role_based_activities(db, user_id, role):
    if role == 'student':
        student_activities(db, user_id)
    elif role == 'member':
        member_activities(db, user_id)
    elif role == 'faculty':
        faculty_activities(db, user_id)
    elif role == 'committee':
        committee_activities(db, user_id)
    elif role == 'admin':
        admin_activities(db)
    elif role == 'lead':
        lead_activities(db, user_id)
    elif role == 'advisor':
        advisor_activities(db, user_id)
    else:
        print("Role not recognized.")

def main():
    data_directory = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    db = initializing(data_directory)

    while True:
        print("\nLogin to the system:")
        user_id, role = login(db)

        if user_id and role:
            role_based_activities(db, user_id, role)
        else:
            print("Login failed. Please try again.")

        exit_choice = input("Do you want to exit the program? (yes/no): ").lower()
        if exit_choice == 'yes':
            break  # Exit the while loop and end the program

    exit(db, data_directory)

if __name__ == "__main__":
    main()

