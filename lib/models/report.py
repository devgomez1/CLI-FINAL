from models.__init__ import CURSOR, CONN

class Report:

    all = {}

    def __init__(self, id, paragraph_overview, user_id, report_text):
        self.id = id
        self.paragraph_overview = paragraph_overview
        self.user_id = user_id
        self.report_text = report_text
    
    def __repr__(self):
        return f"Report({self.id}, {self.paragraph_overview}, {self.user_id}, {self.report_text})"
    
    def __str__(self):
        return f"Report ID: {self.id}, Title: {self.paragraph_overview}, User ID: {self.user_id}, Report Text: {self.report_text}"
    
    @property
    def user(self):
        from models.user import User
        return User.find_by_id(self.user_id)
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM reports
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            report = cls(*row)
            cls.all[id] = report  # Add this line
            return report

    @classmethod
    def find_by_paragraph_overview(cls, paragraph_overview):
        sql = """
            SELECT * FROM reports
            WHERE paragraph_overview = ?
        """
        CURSOR.execute(sql, (paragraph_overview,))
        row = CURSOR.fetchone()
        if row:
            report = cls(*row)
            cls.all[report.id] = report  # Add this line
            return report
        
        
    @classmethod
    def create(cls, paragraph_overview, user_id, report_text):
        sql = """
            INSERT INTO reports (paragraph_overview, user_id, report_text)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (paragraph_overview, user_id, report_text))
        CONN.commit()
        id = CURSOR.lastrowid
        return cls(id, paragraph_overview, user_id, report_text)
    
    @classmethod
    def delete_all(cls):
        sql = """
            DELETE FROM reports
        """
        CURSOR.execute(sql)
        CONN.commit()


    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS reports
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY,
                paragraph_overview TEXT,
                user_id INTEGER,
                report_text TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def fetch_all(cls):
        cls.all.clear()  # Clear the dictionary
        sql = """
            SELECT * FROM reports
        """
        print("Fetching all reports...")
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        for row in rows:
            report = cls(*row)
            cls.all[report.id] = report

    @classmethod
    def delete_by_id(cls, id):
        sql = """
            DELETE FROM reports WHERE id = ?
        """
        print(f"Deleting report with id {id}")
        CURSOR.execute(sql, (id,))
        if CURSOR.rowcount > 0:
            del cls.all[id]
            CONN.commit()
            print("SQL command executed, changes committed.")
        else:
            print("No report found with that ID.")

    @classmethod
    def find_by_user_id(cls, user_id):
        sql = """
            SELECT * FROM reports
            WHERE user_id = ?
        """
        print(f"Finding reports for user_id {user_id}")
        CURSOR.execute(sql, (user_id,))
        rows = CURSOR.fetchall()
        if rows:
            reports = [cls(*row) for row in rows]
            print(f"Found reports")
            return reports
        else:
            print("No reports found for this user.")
            