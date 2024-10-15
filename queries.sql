DROP TABLE card;
DROP TABLE session;
DROP TABLE lead;
DROP TABLE organiser;
DROP TABLE user;
DROP TABLE booking;

INSERT INTO quote VALUES (NULL, 'This is a quote about the company', 'author');
INSERT INTO organiser VALUES (NULL, '/static/employee_photos/logo.png', 'John', 'Steve', 'sj@example.com', 'pass', 'This is a quote about me');
INSERT INTO lead VALUES (NULL, '/static/employee_photos/logo.png', 'Steve', 'John', 'sj@example.com', 'pass', 'This is a quote about me');
INSERT INTO lead VALUES (NULL, '/static/employee_photos/logo.png', 'Albert', 'Stef', 'AS@example.com', 'pass', 'This is a quote about me');