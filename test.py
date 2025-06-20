import sqlite3
from unittest.mock import patch
from models.doctor import Doctor
from database.schema import SCHEMA_SQL

# Test database path (using in-memory for tests)
TEST_DB = ":memory:"

def get_test_connection():
    """Create a connection to the test database"""
    return sqlite3.connect(TEST_DB)

def setup_test_db():
    """Initialize the test database with schema and test data"""
    conn = get_test_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript(SCHEMA_SQL)

    # Insert test data
    test_data = [
        # Doctors
        ("INSERT INTO doctors (name, phone) VALUES (?, ?)",
         [("Dr. Smith", "111-1111"), ("Dr. Jones", "222-2222")]),

        # Patients
        ("INSERT INTO patients (name, phone, gender) VALUES (?, ?, ?)",
         [("Patient A", "555-0001", "Male"), ("Patient B", "555-0002", "Female")]),

        # Records
        ("INSERT INTO records (doctor_id, patient_id) VALUES (?, ?)",
         [(1, 1), (1, 2), (2, 1)]),

        # Treatments
        ("INSERT INTO treatments (record_id, name, cost, notes) VALUES (?, ?, ?, ?)",
         [(1, "Cleaning", 100.0, "Regular cleaning"),
          (1, "Filling", 150.0, "Cavity filled")]),

        # Payments
        ("INSERT INTO payments (record_id, amount, notes) VALUES (?, ?, ?)",
         [(1, 50.0, "Initial payment"), (1, 100.0, "Second payment")])
    ]

    for query, data in test_data:
        cursor.executemany(query, data)

    conn.commit()
    conn.close()

def test_records():
    """Test the records() method"""
    setup_test_db()

    # Patch the get_db_connection to use our test DB
    with patch('models.doctor.get_db_connection', wraps=get_test_connection):
        # Test getting records for doctor_id=1
        results = Doctor.records(1)
        assert len(results) == 2  # Doctor 1 has 2 records
        assert all(record.doctor_id == 1 for record in results)

        # Test getting records for doctor_id=2
        results = Doctor.records(2)
        assert len(results) == 1  # Doctor 2 has 1 record
        assert results[0].doctor_id == 2

def test_treatments():
    """Test the treatments() method"""
    setup_test_db()

    with patch('models.doctor.get_db_connection', wraps=get_test_connection):
        results = Doctor.treatments(1)
        assert len(results) == 2  # Doctor 1 has 2 treatments

        # Verify the structure of returned data
        for item in results:
            assert hasattr(item['record'], 'id')
            assert 'treatment' in item
            assert 'name' in item['treatment']
            assert 'cost' in item['treatment']

        # Verify specific values
        assert results[0]['treatment']['name'] == "Cleaning"
        assert results[1]['treatment']['cost'] == 150.0

def test_payments():
    """Test the payments() method"""
    setup_test_db()

    with patch('models.doctor.get_db_connection', wraps=get_test_connection):
        results = Doctor.payments(1)
        assert len(results) == 2  # Doctor 1 has 2 payments

        # Verify the structure
        for item in results:
            assert hasattr(item['record'], 'id')
            assert 'payment' in item
            assert 'amount' in item['payment']

        # Verify specific values
        assert results[0]['payment']['amount'] == 50.0
        assert results[1]['payment']['amount'] == 100.0

if __name__ == "__main__":
    test_records()
    test_treatments()
    test_payments()
    print("All tests passed!")
