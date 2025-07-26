# student_manager.py
class StudentDataManager:
    def __init__(self, db):
        self.db = db

    def get_students(self):
        return self.db.execute_query("SELECT student_id, name FROM Student_table")

    def get_student_info(self, student_id):
        return self.db.execute_query("SELECT * FROM Student_table WHERE student_id = %s", (student_id,))

    def get_programming_skills(self, student_id):
        return self.db.execute_query("SELECT * FROM Programming_table WHERE student_id = %s", (student_id,))

    def get_soft_skills(self, student_id):
        return self.db.execute_query("SELECT * FROM Soft_skills WHERE student_id = %s", (student_id,))

    def get_placement_info(self, student_id):
        return self.db.execute_query("SELECT * FROM Placement_table WHERE student_id = %s", (student_id,))
