GET_USER_BY_USERNAME = """
SELECT user_id, username, name, email, role, password_hash
FROM users
WHERE username = %s
"""

GET_USERS_BY_ROLE = """
SELECT user_id, username, name, email, role, created_at
FROM users
WHERE role = %s
LIMIT %s OFFSET %s
"""

ADD_USER = """
INSERT INTO users (username, name, email, role, password_hash) 
VALUES (%s, %s, %s, %s, %s)
"""
UPDATE_USER_WITH_PASSWORD = """
UPDATE users
SET 
    name = COALESCE(%s, name),
    email = COALESCE(%s, email),
    role = COALESCE(%s, role),
    password_hash = COALESCE(%s, password_hash)
WHERE user_id = %s
"""

UPDATE_USER = """
UPDATE users
SET 
    name = COALESCE(%s, name),
    email = COALESCE(%s, email),
    role = COALESCE(%s, role)
WHERE user_id = %s
"""

SOFT_DELETE_USER = """
UPDATE users 
SET role = 'inactive'
SET email = NULL
WHERE user_id = %s
"""


# Class Management Queries
GET_ALL_CLASSES = """
SELECT c.class_id, c.class_name, c.coordinator_id, u.name as coordinator_name
FROM classes c
LEFT JOIN users u ON c.coordinator_id = u.user_id
"""

GET_CLASS_BY_ID = """
SELECT c.class_id, c.class_name, c.coordinator_id, u.name as coordinator_name
FROM classes c
LEFT JOIN users u ON c.coordinator_id = u.user_id
WHERE c.class_id = %s
"""

ADD_CLASS = """
INSERT INTO classes (class_name, coordinator_id)
VALUES (%s, %s)
"""

UPDATE_CLASS = """
UPDATE classes
SET class_name = %s, coordinator_id = %s
WHERE class_id = %s
"""

DELETE_CLASS = """
DELETE FROM classes
WHERE class_id = %s
"""

GET_ALL_TEACHERS = """
SELECT user_id, name
FROM users
WHERE role = 'teacher'
"""


# Subject Management Queries
GET_ALL_SUBJECTS = """
SELECT s.subject_id, s.subject_name, s.class_id, s.teacher_id,
       c.class_name, u.name as teacher_name
FROM subjects s
LEFT JOIN classes c ON s.class_id = c.class_id
LEFT JOIN users u ON s.teacher_id = u.user_id
"""

GET_SUBJECT_BY_ID = """
SELECT s.subject_id, s.subject_name, s.class_id, s.teacher_id,
       c.class_name, u.name as teacher_name
FROM subjects s
LEFT JOIN classes c ON s.class_id = c.class_id
LEFT JOIN users u ON s.teacher_id = u.user_id
WHERE s.subject_id = %s
"""

ADD_SUBJECT = """
INSERT INTO subjects (subject_name, class_id, teacher_id)
VALUES (%s, %s, %s)
"""

UPDATE_SUBJECT = """
UPDATE subjects
SET subject_name = %s, class_id = %s, teacher_id = %s
WHERE subject_id = %s
"""

DELETE_SUBJECT = """
DELETE FROM subjects
WHERE subject_id = %s
"""



# Time Table Management Queries
GET_TIMETABLE_BY_CLASS = """
SELECT t.timetable_id, t.class_id, t.subject_id, t.teacher_id, 
       t.day, TIME_FORMAT(t.start_time, '%H:%i') as start_time, 
       TIME_FORMAT(t.end_time, '%H:%i') as end_time,
       c.class_name, s.subject_name, u.name as teacher_name
FROM timetable t
JOIN classes c ON t.class_id = c.class_id
JOIN subjects s ON t.subject_id = s.subject_id
JOIN users u ON t.teacher_id = u.user_id
WHERE t.class_id = %s
ORDER BY FIELD(t.day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
         t.start_time
"""

GET_ALL_TIMETABLE_ENTRIES = """
SELECT t.timetable_id, t.class_id, t.subject_id, t.teacher_id, 
       t.day, TIME_FORMAT(t.start_time, '%H:%i') as start_time, 
       TIME_FORMAT(t.end_time, '%H:%i') as end_time,
       c.class_name, s.subject_name, u.name as teacher_name
FROM timetable t
JOIN classes c ON t.class_id = c.class_id
JOIN subjects s ON t.subject_id = s.subject_id
JOIN users u ON t.teacher_id = u.user_id
ORDER BY c.class_name,
         FIELD(t.day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
         t.start_time
"""

ADD_TIMETABLE_ENTRY = """
INSERT INTO timetable (class_id, subject_id, teacher_id, day, start_time, end_time)
VALUES (%s, %s, %s, %s, %s, %s)
"""

UPDATE_TIMETABLE_ENTRY = """
UPDATE timetable
SET class_id = %s, subject_id = %s, teacher_id = %s, 
    day = %s, start_time = %s, end_time = %s
WHERE timetable_id = %s
"""

DELETE_TIMETABLE_ENTRY = """
DELETE FROM timetable
WHERE timetable_id = %s
"""

CHECK_SCHEDULE_CONFLICT = """
SELECT COUNT(*) as conflict_count
FROM timetable
WHERE class_id = %s 
  AND day = %s
  AND ((start_time BETWEEN %s AND %s) 
       OR (end_time BETWEEN %s AND %s)
       OR (start_time <= %s AND end_time >= %s))
  AND timetable_id != COALESCE(%s, 0)
"""



# Exam Management Queries
GET_ALL_EXAMS = """
SELECT e.exam_id, e.exam_name, e.class_id, e.exam_date, c.class_name
FROM exams e
JOIN classes c ON e.class_id = c.class_id
ORDER BY e.exam_date DESC
"""

GET_EXAMS_BY_CLASS = """
SELECT e.exam_id, e.exam_name, e.class_id, e.exam_date, c.class_name
FROM exams e
JOIN classes c ON e.class_id = c.class_id
WHERE e.class_id = %s
ORDER BY e.exam_date DESC
"""

ADD_EXAM = """
INSERT INTO exams (exam_name, class_id, exam_date)
VALUES (%s, %s, %s)
"""

UPDATE_EXAM = """
UPDATE exams
SET exam_name = %s, class_id = %s, exam_date = %s
WHERE exam_id = %s
"""

DELETE_EXAM = """
DELETE FROM exams
WHERE exam_id = %s
"""