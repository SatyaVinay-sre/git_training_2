INSERT INTO Role (name) VALUES ('admin');
INSERT INTO Role (name) VALUES ('it');
INSERT INTO Role (name) VALUES ('user');

INSERT INTO User (uname, password, dateJoined) 
VALUES ('admin', 'abc', CURRENT_TIMESTAMP);

INSERT INTO User (uname, password, dateJoined) 
VALUES ('wiley', 'abc', CURRENT_TIMESTAMP);

