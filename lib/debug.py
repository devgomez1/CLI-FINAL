from models.__init__ import CURSOR, CONN
from models.user import User
from models.report import Report
import ipdb

def reset_database():
    User.drop_table()
    User.create_table()
    Report.drop_table()  # Add this line
    Report.create_table()  # Add this line

    # Create seed data
    user1 = User.create("Alice")
    user2 = User.create("Bob")
    Report.create("Report 1 overview", user1.id, "Report 1 text")
    Report.create("Report 2 overview", user1.id, "Report 2 text")
    Report.create("Report 3 overview", user2.id, "Report 3 text")

reset_database()
ipdb.set_trace()