CREATE table tasks (
    task_id INT PRIMARY KEY,
    task_name TEXT,
    task_complete BOOLEAN
);

INSERT INTO tasks (task_id, task_name, task_complete) VALUES
(1, 'task1', FALSE),
(2, 'task2', FALSE),
(3, 'task3', FALSE);

SELECT * FROM tasks;
-- psql -h localhost -U username -d database_name -f filename.sql