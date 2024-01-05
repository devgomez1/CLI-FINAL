from models.__init__ import CURSOR, CONN



class User:

    all = {}

    def __init__(self, id, name,):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"User({self.id}, {self.name})"
    
    @property
    def reports(self):
        from models.report import Report
        return [report for report in Report.all.values() if report.user_id == self.id]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM users
            WHERE id = ?
        """
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM users
            WHERE name = ?
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)
        
    @classmethod
    def create(cls, name):
        sql = """
            INSERT INTO users (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (name,))
        CONN.commit()
        id = CURSOR.lastrowid
        return cls(id, name)
    
    def delete(self):
        sql = """
            DELETE FROM users
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del User.all[self.id]
    
    def update(self, name):
        sql = """
            UPDATE users
            SET name = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (name, self.id))
        CONN.commit()
        self.name = name
        return self
    
    @classmethod
    def all_users(cls):
        sql = """
            SELECT * FROM users
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls(*row) for row in rows]
    
    @classmethod
    def delete_all(cls):
        sql = """
            DELETE FROM users
        """
        CURSOR.execute(sql)
        CONN.commit()
        User.all = {}

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS users
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def seed(cls):
        cls.create("John")
        cls.create("Jane")
        cls.create("Jack")
        cls.create("Jill")
        cls.create("Joe")
        cls.create("Jenny")
        cls.create("Jared")
        cls.create("Jasmine")
        cls.create("Jesse")
        cls.create("Jocelyn")
        cls.create("Javier")
        cls.create("Jade")
        cls.create("Jaden")
        cls.create("Jesse")
        cls.create("Jenna")
    
    @classmethod
    def print_all(cls):
        for user in cls.all_users():
            print(user)

    @classmethod
    def print_all_reports(cls):
        for user in cls.all_users():
            print(f"{user.name}'s reports:")
            for report in user.reports:
                print(report)
            print()

    @classmethod
    def print_all_users_and_reports(cls):
        for user in cls.all_users():
            print(user)
            for report in user.reports:
                print(report)
            print()

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM users
            WHERE name = ?
        """
        print(f"Finding user with name {name}")
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)
        else:
            print("User not found.")

    @property
    def reports(self):
        from models.report import Report
        reports = list({report.id: report for report in Report.all.values() if report.user_id == self.id}.values())
        return reports

    

        