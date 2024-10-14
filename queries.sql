DROP TABLE card;
DROP TABLE session;
DROP TABLE lead;
DROP TABLE organiser;
DROP TABLE user;
DROP TABLE booking;

INSERT INTO organiser VALUES (NULL, 'John', 'Steve', 'sj@example.com', 'pass');
INSERT INTO lead VALUES (NULL, 'Steve', 'John', 'sj@example.com', 'pass');
INSERT INTO lead VALUES (NULL, 'Albert', 'Stef', 'AS@example.com', 'pass');
INSERT INTO session VALUES (NULL, 'Session 1', '£50.00', 'Tomorrow', 'Outside', 'jump', 'skip', 'hop', '1', '2', '3', 1, 1);