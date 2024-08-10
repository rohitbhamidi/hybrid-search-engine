import threading
import uuid
from collections import defaultdict
from copy import deepcopy

class Database:
    def __init__(self):
        # Data storage with branches for versioning
        self.data = defaultdict(dict)  # branch_name -> {id: record}
        self.current_branch = 'main'
        self.lock = threading.Lock()
        self.transactions = []  # To keep track of ongoing transactions
        self.next_id = 0  # Auto-incrementing ID counter
    
    def _generate_id(self):
        """Generate a unique ID for a new record."""
        new_id = str(uuid.uuid4())  # Alternatively, self.next_id can be used for simple auto-increment
        self.next_id += 1
        return new_id
    
    def begin_transaction(self):
        """Begin a new transaction."""
        with self.lock:
            transaction = deepcopy(self.data[self.current_branch])
            self.transactions.append(transaction)
    
    def commit_transaction(self):
        """Commit the current transaction."""
        with self.lock:
            if not self.transactions:
                raise Exception("No active transaction to commit.")
            self.transactions.pop()
            # Placeholder for future persistence to S3
    
    def rollback_transaction(self):
        """Rollback the current transaction."""
        with self.lock:
            if not self.transactions:
                raise Exception("No active transaction to rollback.")
            last_transaction = self.transactions.pop()
            self.data[self.current_branch] = last_transaction
    
    def insert(self, record):
        """Insert a new record into the database."""
        with self.lock:
            record_id = self._generate_id()
            self.data[self.current_branch][record_id] = record
        return record_id

    
    def update(self, record_id, updated_record):
        """Update an existing record."""
        with self.lock:
            if record_id not in self.data[self.current_branch]:
                raise KeyError(f"Record with ID {record_id} not found.")
            self.data[self.current_branch][record_id] = updated_record
    
    def delete(self, record_id):
        """Delete a record from the database."""
        with self.lock:
            if record_id in self.data[self.current_branch]:
                del self.data[self.current_branch][record_id]
            else:
                raise KeyError(f"Record with ID {record_id} not found.")
    
    def read(self, record_id):
        """Read a record from the database."""
        with self.lock:
            return self.data[self.current_branch].get(record_id, None)
    
    def create_branch(self, branch_name):
        """Create a new branch for versioning."""
        with self.lock:
            if branch_name in self.data:
                raise ValueError(f"Branch {branch_name} already exists.")
            self.data[branch_name] = deepcopy(self.data[self.current_branch])
    
    def switch_branch(self, branch_name):
        """Switch to a different branch."""
        with self.lock:
            if branch_name not in self.data:
                raise ValueError(f"Branch {branch_name} does not exist.")
            self.current_branch = branch_name
    
    def get_all_records(self):
        """Retrieve all records in the current branch."""
        with self.lock:
            return deepcopy(self.data[self.current_branch])

    # Placeholder for future data persistence to S3
    def persist_to_s3(self):
        """Persist current state to S3 (not yet implemented)."""
        pass
