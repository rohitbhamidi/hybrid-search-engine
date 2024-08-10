import pytest

def test_insert(db, sample_record):
    """Test inserting a record with auto-assigned ID."""
    record_id = db.insert(sample_record)
    assert record_id is not None, "Insert should return a valid record ID"
    
    # Verify the record is stored correctly
    stored_record = db.read(record_id)
    assert stored_record == sample_record, f"Expected {sample_record}, but got {stored_record}"

def test_update(db, sample_record):
    """Test updating an existing record."""
    record_id = db.insert(sample_record)
    
    updated_record = {"name": "Updated Record", "value": 200}
    db.update(record_id, updated_record)
    
    # Verify the record is updated
    stored_record = db.read(record_id)
    assert stored_record == updated_record, f"Expected {updated_record}, but got {stored_record}"

def test_delete(db, sample_record):
    """Test deleting a record."""
    record_id = db.insert(sample_record)
    db.delete(record_id)
    
    # Verify the record is deleted
    stored_record = db.read(record_id)
    assert stored_record is None, f"Record with ID {record_id} should be deleted, but it still exists"

def test_read_nonexistent_record(db):
    """Test reading a record that does not exist."""
    non_existent_id = "non-existent-id"
    stored_record = db.read(non_existent_id)
    assert stored_record is None, f"Expected None, but got {stored_record}"

def test_create_and_switch_branch(db, sample_record):
    """Test creating and switching branches."""
    db.insert(sample_record)
    
    # Create a new branch and switch to it
    new_branch_name = "feature-branch"
    db.create_branch(new_branch_name)
    db.switch_branch(new_branch_name)
    
    # Verify that the new branch contains the same records as the main branch initially
    all_records = db.get_all_records()
    assert len(all_records) == 1, "New branch should contain the same records as the main branch"
    
    # Insert a new record into the new branch and verify that it doesn't affect the main branch
    new_record = {"name": "New Record", "value": 200}
    db.insert(new_record)
    
    db.switch_branch('main')
    all_records_main = db.get_all_records()
    assert len(all_records_main) == 1, "Main branch should still contain the original record"
    
    db.switch_branch(new_branch_name)
    all_records_feature = db.get_all_records()
    assert len(all_records_feature) == 2, "Feature branch should contain both records"
    
    # Switch back to the main branch and verify the original record is still there
    db.switch_branch('main')
    all_records = db.get_all_records()
    assert len(all_records) == 1, "Main branch should still contain the original record"

def test_transaction_commit(db, sample_record):
    """Test committing a transaction."""
    db.begin_transaction()
    
    record_id = db.insert(sample_record)
    db.commit_transaction()
    
    # Verify that the record is stored correctly after commit
    stored_record = db.read(record_id)
    assert stored_record == sample_record, f"Expected {sample_record} after commit, but got {stored_record}"

def test_transaction_rollback(db, sample_record):
    """Test rolling back a transaction."""
    db.begin_transaction()
    
    record_id = db.insert(sample_record)
    db.rollback_transaction()
    
    # Verify that the record is not stored after rollback
    stored_record = db.read(record_id)
    assert stored_record is None, f"Record with ID {record_id} should not exist after rollback, but it does"

def test_switch_to_nonexistent_branch(db):
    """Test switching to a non-existent branch."""
    with pytest.raises(ValueError, match="Branch non-existent-branch does not exist"):
        db.switch_branch("non-existent-branch")

def test_create_existing_branch(db):
    """Test creating a branch that already exists."""
    db.create_branch('existing-branch')
    with pytest.raises(ValueError, match="Branch existing-branch already exists"):
        db.create_branch('existing-branch')
