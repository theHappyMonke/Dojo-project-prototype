DROP TABLE activity;
DROP TABLE booking;
DROP TABLE card;
DROP TABLE contact;
DROP TABLE lead;
DROP TABLE organiser;
DROP TABLE reviews;
DROP TABLE session;
DROP TABLE timeslot;
DROP TABLE user;

INSERT INTO review VALUES (NULL, 'This is a quote about the company', 'author');
INSERT INTO organiser VALUES (NULL, '/static/employee_photos/logo.png', 'John', 'Steve', 'sj@example.com', 'pass', 'This is a quote about me');
INSERT INTO leads VALUES (NULL, '/static/employee_photos/logo.png', 'Steve', 'John', 'sj@example.com', 'This is a quote about me');
INSERT INTO leads VALUES (NULL, '/static/employee_photos/logo.png', 'Albert', 'Stef', 'AS@example.com', 'This is a quote about me');
INSERT INTO leads VALUES (NULL, '/static/employee_photos/logo.png', 'Lee', 'Botting', 'Lee@example.com', 'I am Lee :)');
INSERT INTO user (forname, surname, email, password, admin) VALUES ('Admin', 'Admin', 'Admin@email.com', , False)
INSERT INTO activity VALUES (NULL, 1, 'Activity 1');
INSERT INTO activity VALUES (NULL, 1, 'Activity 2');
INSERT INTO activity VALUES (NULL, 1, 'Activity 3');
INSERT INTO timeslot VALUES (NULL, 1, '00:00', '12:00');