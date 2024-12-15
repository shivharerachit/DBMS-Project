GET_TEACHER_CLASSES = """
SELECT DISTINCT
    c.class_id,
    c.class_name
FROM timetable t
JOIN classes c ON t.class_id = c.class_id
WHERE t.teacher_id = %s
ORDER BY c.class_name
"""

GET_TEACHER_SCHEDULE = """
SELECT 
    c.class_name,
    s.subject_name,
    t.day,
    t.start_time,
    t.end_time
FROM timetable t
JOIN classes c ON t.class_id = c.class_id
JOIN subjects s ON t.subject_id = s.subject_id
WHERE t.teacher_id = %s
ORDER BY t.day, t.start_time
"""

MARK_ATTENDANCE = """
INSERT INTO attendance (student_id, class_id, date, status) 
VALUES (%s, %s, %s, %s)
"""

GET_CLASS_STUDENTS = """
SELECT 
    u.user_id,
    u.name,
    u.username
FROM users u
JOIN student_classes sc ON u.user_id = sc.student_id
WHERE sc.class_id = %s AND u.role = 'student'
ORDER BY u.name
"""