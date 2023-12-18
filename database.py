import csv
import os
import copy

# Define the location of the script to find CSV files relative to it
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def read_file(csv_name):
    """Read a CSV file and return its content as a list of dictionaries."""
    file = []
    with open(os.path.join(__location__, csv_name)) as f:
        rows = csv.DictReader(f)
        for r in rows:
            file.append(dict(r))
        return file

def write_file(file_path, data):
    """Writes data to a CSV file."""
    if not data:
        print(f"No data to write for {file_path}.")
        return

    # Determine all unique keys present in the data
    all_keys = set(key for entry in data for key in entry.keys())

    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(data)



class Database:
    """A simple in-memory database to hold tables."""

    def __init__(self):
        self._database = []

    def insert(self, table):
        """Insert a table into the database."""
        self._database.append(table)

    def search(self, table_name):
        """Search for a table by its name."""
        for tables in self._database:
            if tables.table_name == table_name:
                return tables
        return None

class Table:
    """Represents a data table."""

    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        """Join two tables on a common key."""
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        """Filter the table based on a condition."""
        filtered_table = Table(self.table_name + '_filtered', [])
        for item in self.table:
            if condition(item):
                filtered_table.table.append(item)
        return filtered_table

    def select(self, attributes_list):
        """Select specific attributes from the table."""
        selected_table = []
        for item in self.table:
            selected_item = {key: item[key] for key in attributes_list if key in item}
            selected_table.append(selected_item)
        return selected_table

    def insert(self, entry):
        """Insert a new entry into the table."""
        self.table.append(entry)

    def update(self, key, value, condition):
        """Update entries in the table based on a condition."""
        for item in self.table:
            if condition(item):
                item[key] = value

    def __str__(self):
        return f"{self.table_name}: {str(self.table)}"

# Example usage
persons = read_file('persons.csv')
login = read_file('login.csv')
projects = read_file('projects.csv')
advisor_pending_request = read_file('advisor_pending_request.csv')
member_pending_request = read_file('member_pending_request.csv')

persons_table = Table('persons', persons)
login_table = Table('login', login)
projects_table = Table('projects', projects)
advisor_pending_request_table = Table('advisor_pending_request', advisor_pending_request)
member_pending_request_table = Table('member_pending_request', member_pending_request)

my_DB = Database()
my_DB.insert(persons_table)
my_DB.insert(login_table)
my_DB.insert(projects_table)
my_DB.insert(advisor_pending_request_table)
my_DB.insert(member_pending_request_table)