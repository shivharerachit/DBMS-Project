from typing import Dict, Optional, List
from .connection import DatabaseConnection
from .queries.user_queries import *
from .queries.teacher_queries import *
from .queries.student_queries import *
from datetime import datetime

class SchoolManagementSystem:
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_USER_BY_USERNAME, (username,))
                return db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        
    def get_users_by_role(self, role: str, limit: int, offset: int) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_USERS_BY_ROLE, (role, limit, offset))
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching users by role: {e}")
            return []
        
    def update_user(self, username, update_data):
        try:
            user = self.get_user_by_username(username)
            if not user:
                return False
            
            name = update_data.get('name')
            email = update_data.get('email')
            role = update_data.get('role')
            password_hash = update_data.get('password_hash')
            
            if password_hash:
                with DatabaseConnection(self.db_config) as db:
                    db.cursor.execute(UPDATE_USER_WITH_PASSWORD, 
                                (name, email, role, password_hash, user['user_id']))
            else:
                with DatabaseConnection(self.db_config) as db:
                    db.cursor.execute(UPDATE_USER, 
                                (name, email, role, user['user_id']))
            return True
        
        except Exception as e:
            print(f"Error fetching users by role: {e}")
            return []

    def delete_user(self, username):
        try:
            user = self.get_user_by_username(username)
            if not user:
                return False
            
            with  DatabaseConnection(self.db_config) as db:
                db.cursor.execute(SOFT_DELETE_USER, (user['user_id'],))
            
            return True
        
        except Exception as err:
            print(f"Error deleting user: {err}")
            return False
        
    def create_user(self, username: str, name: str, email: str, 
                   role: str, password_hash: str) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(ADD_USER, 
                                (username, name, email, role, password_hash))
            return True
        except Exception as e:
            print(f"Error creating user: {e}")
            return False
        
    # Class Management Methods
    def get_all_classes(self) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_ALL_CLASSES)
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching classes: {e}")
            return []

    def get_class_by_id(self, class_id: int) -> Optional[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_CLASS_BY_ID, (class_id,))
                return db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching class: {e}")
            return None

    def create_class(self, class_name: str, coordinator_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(ADD_CLASS, (class_name, coordinator_id))
            return True
        except Exception as e:
            print(f"Error creating class: {e}")
            return False

    def update_class(self, class_id: int, class_name: str, coordinator_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(UPDATE_CLASS, (class_name, coordinator_id, class_id))
            return True
        except Exception as e:
            print(f"Error updating class: {e}")
            return False

    def delete_class(self, class_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(DELETE_CLASS, (class_id,))
            return True
        except Exception as e:
            print(f"Error deleting class: {e}")
            return False

    def get_all_teachers(self) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_ALL_TEACHERS)
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching teachers: {e}")
            return []
        
    # Subject Management Methods
    def get_all_subjects(self) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_ALL_SUBJECTS)
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching subjects: {e}")
            return []

    def get_subject_by_id(self, subject_id: int) -> Optional[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_SUBJECT_BY_ID, (subject_id,))
                return db.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching subject: {e}")
            return None

    def create_subject(self, subject_name: str, class_id: int, teacher_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(ADD_SUBJECT, (subject_name, class_id, teacher_id))
            return True
        except Exception as e:
            print(f"Error creating subject: {e}")
            return False

    def update_subject(self, subject_id: int, subject_name: str, class_id: int, teacher_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(UPDATE_SUBJECT, (subject_name, class_id, teacher_id, subject_id))
            return True
        except Exception as e:
            print(f"Error updating subject: {e}")
            return False

    def delete_subject(self, subject_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(DELETE_SUBJECT, (subject_id,))
            return True
        except Exception as e:
            print(f"Error deleting subject: {e}")
            return False
        

    # Time Table Management Methods
    def get_timetable_by_class(self, class_id: int) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_TIMETABLE_BY_CLASS, (class_id,))
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching timetable: {e}")
            return []

    def get_all_timetable_entries(self) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_ALL_TIMETABLE_ENTRIES)
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all timetable entries: {e}")
            return []

    def check_schedule_conflict(self, class_id: int, day: str, start_time: str, 
                              end_time: str, timetable_id: Optional[int] = None) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(CHECK_SCHEDULE_CONFLICT, 
                                (class_id, day, start_time, end_time, 
                                 start_time, end_time, start_time, end_time, timetable_id))
                result = db.cursor.fetchone()
                return result['conflict_count'] > 0
        except Exception as e:
            print(f"Error checking schedule conflict: {e}")
            return True

    def create_timetable_entry(self, class_id: int, subject_id: int, teacher_id: int,
                             day: str, start_time: str, end_time: str) -> bool:
        try:
            if self.check_schedule_conflict(class_id, day, start_time, end_time):
                return False

            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(ADD_TIMETABLE_ENTRY, 
                                (class_id, subject_id, teacher_id, day, start_time, end_time))
            return True
        except Exception as e:
            print(f"Error creating timetable entry: {e}")
            return False

    def update_timetable_entry(self, timetable_id: int, class_id: int, subject_id: int,
                             teacher_id: int, day: str, start_time: str, end_time: str) -> bool:
        try:
            if self.check_schedule_conflict(class_id, day, start_time, end_time, timetable_id):
                return False

            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(UPDATE_TIMETABLE_ENTRY,
                                (class_id, subject_id, teacher_id, day, 
                                 start_time, end_time, timetable_id))
            return True
        except Exception as e:
            print(f"Error updating timetable entry: {e}")
            return False

    def delete_timetable_entry(self, timetable_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(DELETE_TIMETABLE_ENTRY, (timetable_id,))
            return True
        except Exception as e:
            print(f"Error deleting timetable entry: {e}")
            return False
        

    def get_all_exams(self) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_ALL_EXAMS)
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching exams: {e}")
            return []

    def get_exams_by_class(self, class_id: int) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_EXAMS_BY_CLASS, (class_id,))
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching exams by class: {e}")
            return []

    def create_exam(self, exam_name: str, class_id: int, exam_date: str) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(ADD_EXAM, (exam_name, class_id, exam_date))
            return True
        except Exception as e:
            print(f"Error creating exam: {e}")
            return False

    def update_exam(self, exam_id: int, exam_name: str, class_id: int, exam_date: str) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(UPDATE_EXAM, (exam_name, class_id, exam_date, exam_id))
            return True
        except Exception as e:
            print(f"Error updating exam: {e}")
            return False

    def delete_exam(self, exam_id: int) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(DELETE_EXAM, (exam_id,))
            return True
        except Exception as e:
            print(f"Error deleting exam: {e}")
            return False
        









    # Teacher Management Methods

    def get_teacher_classes(self, teacher_id: int) -> List[Dict]:
            try:
                with DatabaseConnection(self.db_config) as db:
                    db.cursor.execute(GET_TEACHER_CLASSES, (teacher_id,))
                    return db.cursor.fetchall()
            except Exception as e:
                print(f"Error fetching teacher classes: {e}")
                return []
            
    def get_teacher_schedule(self, teacher_id: int) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_TEACHER_SCHEDULE, (teacher_id,))
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching teacher schedule: {e}")
            return []
        
        
    def mark_student_attendance(self, student_id: int, class_id: int, 
                              status: str) -> bool:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(MARK_ATTENDANCE, 
                                (student_id, class_id, 
                                 datetime.now().date(), status))
            return True
        except Exception as e:
            print(f"Error marking attendance: {e}")
            return False
        
    def get_class_students(self, class_id: int) -> List[Dict]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_CLASS_STUDENTS, (class_id,))
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching class students: {e}")
            return []
        





    # Student Management Methods

    def get_student_timetable(self, student_id: int) -> Optional[List[Dict]]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_STUDENT_TIMETABLE, (student_id,))
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching timetable: {e}")
            return None
        
    def get_student_performance(self, student_id: int) -> Optional[List[Dict]]:
        try:
            with DatabaseConnection(self.db_config) as db:
                db.cursor.execute(GET_STUDENT_RESULTS, (student_id,))
                return db.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching student results: {e}")
            return None