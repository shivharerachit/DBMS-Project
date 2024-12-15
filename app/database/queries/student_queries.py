GET_STUDENT_TIMETABLE = """
SELECT 
    c.class_name,
    s.subject_name,
    t.day,
    t.start_time,
    t.end_time,
    u.name AS teacher_name
FROM timetable t
JOIN classes c ON t.class_id = c.class_id
JOIN subjects s ON t.subject_id = s.subject_id
JOIN users u ON t.teacher_id = u.user_id
WHERE c.class_id = (
    SELECT class_id 
    FROM attendance 
    WHERE student_id = %s 
    LIMIT 1
)
"""
GET_STUDENT_RESULTS = """
SELECT 
    s.subject_name,
    r.marks_obtained,
    r.max_marks,
    r.grade
FROM results r
JOIN subjects s ON r.subject_id = s.subject_id
WHERE r.student_id = %s
"""