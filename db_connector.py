# db_connector.py
import mysql.connector
import pandas as pd

class DatabaseConnector:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        if not self.conn or not self.conn.is_connected():
            self.conn = mysql.connector.connect(**self.config)
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute_query(self, query, params=None):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)

    def get_student_names(self):
        self.connect()
        cursor = self.conn.cursor()
        query = "SELECT student_id, name FROM Student_table"
        cursor.execute(query)
        rows = cursor.fetchall()
        return {name: student_id for student_id, name in rows}

    def get_student_info(self, student_id):
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM Student_table WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

    def get_programming_info(self, student_id):
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM Programming_table WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

    def get_soft_skills_info(self, student_id):
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM Soft_skills WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()

    def get_placement_info(self, student_id):
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        query = "SELECT * FROM Placement_table WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        return cursor.fetchone()
