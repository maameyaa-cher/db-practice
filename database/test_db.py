import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# test_db.py
from sqlalchemy import inspect
from database.base import engine  # Import the engine from your base.py


# Use the inspector to check connection
inspector = inspect(engine)

# Print out the list of tables (this checks if the connection works)
print(inspector.get_table_names())  # This will return an empty list if no tables are created yet
