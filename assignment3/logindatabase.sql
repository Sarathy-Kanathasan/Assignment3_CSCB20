CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(20) NOT NULL, 
    password VARCHAR(20) NOT NULL,
    type INTEGER NOT NULL
);


INSERT INTO users VALUES(1, 'student1', 'student1',0);
INSERT INTO users VALUES(2, 'student2', 'student2',0); 
INSERT INTO users VALUES(3, 'instructor1', 'instructor1',1); 
INSERT INTO users VALUES(4, 'instructor2', 'instructor2',1); 



CREATE TABLE IF NOT EXISTS marks (
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    mark INTEGER CHECK(mark>0) NOT NULL,
    assignment VARCHAR(30) NOT NULL
);


INSERT INTO marks VALUES(1, 'Student1', 50, 'Midterm');
INSERT INTO marks VALUES(1, 'Student1', 100, 'Assignment 1');

CREATE TABLE IF NOT EXISTS afeed (
    feedback VARCHAR(1000) NOT NULL,
    ainfo VARCHAR(1000) NOT NULL,    
    instructor VARCHAR(30) NOT NULL
);

INSERT INTO afeed VALUES ("SUCK UR MUM PUSSY HOLE I HATE THIS CLASS", 'IM UNDER THE WATER', "Instructor1");

CREATE TABLE IF NOT EXISTS remark (
    id INTEGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    assignment VARCHAR(30) NOT NULL,
    justification VARCHAR(1000)
);

INSERT INTO remark VALUES(1, 'Student1', 'Midterm', 'I want 100'); 
