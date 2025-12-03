--  Create a students table
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

--  Create a grade table
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY ,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),
    FOREIGN KEY (student_id) REFERENCES students (id)
);

-- Inserting data in table students
INSERT INTO students (full_name, birth_year) VALUES
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Inserting data in the grades table
INSERT INTO grades (student_id, subject, grade) VALUES
(1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
(2, 'Math', 75), (2, 'History', 83), (2, 'English', 79), 
(3, 'Science', 95),(3, 'Math', 91), (3, 'Art', 89),
(4, 'Math', 84), (4, 'Science', 88), (4, 'Physical Education', 93),
(5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
(6, 'Science', 72),(6, 'Math', 78), (6, 'English', 81),
(7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
(8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
(9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92);


-- Find all the grades of a particular student (for example, Alice Johnson)
SELECT g.subject, g.grade
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson';

-- Calculate the average score for each student
SELECT s.id, s.full_name, AVG(g.grade) AS average_grade
FROM grades g
JOIN students s ON g.student_id = s.id
GROUP BY s.id, s.full_name;

-- Compile a list of students born after 2004
SELECT id, full_name, birth_year
FROM students
WHERE birth_year > 2004;

-- Display all items and their average scores
SELECT subject, AVG(grade) AS average_grade
FROM grades
GROUP BY subject;

-- Find top 3 students with the highest average scores
SELECT s.id, s.full_name, AVG(g.grade) AS average_grade
FROM grades g
JOIN students s ON g.student_id = s.id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Show all students who got less than 80 points in any subject
SELECT DISTINCT s.id, s.full_name
FROM grades g
JOIN students s ON g.student_id = s.id
WHERE g.grade < 80;

-- Create indexes to optimize queries
CREATE INDEX idx_students_birth_year ON students (birth_year);
CREATE INDEX idx_grades_student_id ON grades (student_id);
CREATE INDEX idx_grades_subject ON grades (subject);
CREATE INDEX idx_grades_grade ON grades (grade);