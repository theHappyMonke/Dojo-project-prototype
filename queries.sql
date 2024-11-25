DROP TABLE activities_for_sessions;
DROP TABLE activities_in_sessions;
DROP TABLE booking;
DROP TABLE cards;
DROP TABLE contact;
DROP TABLE leads;
DROP TABLE reviews;
DROP TABLE sessions;
DROP TABLE timeslot;
DROP TABLE users;
DROP TABLE access_rights;

INSERT INTO reviews VALUES (NULL, 'This is a quote about the company', 'author');
INSERT INTO leads VALUES (NULL, '/static/employee_photos/logo.png', 'Steve', 'John', 'sj@example.com', 'This is a quote about me');
INSERT INTO leads VALUES (NULL, '/static/employee_photos/logo.png', 'Albert', 'Stef', 'AS@example.com', 'This is a quote about me');
INSERT INTO leads VALUES (NULL, '/static/employee_photos/logo.png', 'Lee', 'Botting', '23bottingl849@collyers.ac.uk', 'I am Lee :)');
INSERT INTO activities_for_sessions VALUES (NULL, 'Run');
INSERT INTO activities_for_sessions VALUES (NULL, 'Jump');
INSERT INTO activities_for_sessions VALUES (NULL, 'Skip');
INSERT INTO activities_in_sessions VALUES (NULL, 1, 1);
INSERT INTO activities_in_sessions VALUES (NULL, 1, 2);
INSERT INTO activities_in_sessions VALUES (NULL, 1, 3);
INSERT INTO timeslot VALUES (NULL, 1, '00:00', '12:00');
INSERT INTO access_rights VALUES (NULL, 'user', 0);
INSERT INTO access_rights VALUES (NULL, 'organiser', 0);
INSERT INTO access_rights VALUES (NULL, 'lead', 0);
INSERT INTO access_rights VALUES (NULL, 'admin', 0);

UPDATE users SET access = 4 WHERE id = 1
UPDATE access_rights SET quantity = 0 WHERE id = 1;
UPDATE access_rights SET quantity = 1 WHERE id = 4;