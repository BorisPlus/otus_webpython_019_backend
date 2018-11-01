import os
import sys

app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_path not in sys.path:
    sys.path.append(app_path)

from bug_report.backend.config import db, db_file

if __name__ == '__main__':
    if os.path.exists(db_file):
        os.remove(db_file)
    db.create_all()
