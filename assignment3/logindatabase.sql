CREATE TABLE IF NOT EXISTS users (
    id INTERGER NOT NULL PRIMARY KEY,
    username VARCHAR(20) NOT NULL, 
    password VARCHAR(20) NOT NULL,
    type INTEGER NOT NULL
);


INSERT INTO users VALUES(1, 'student1', 'student1',0);
INSERT INTO users VALUES(2, 'student2', 'student2',0); 
INSERT INTO users VALUES(3, 'instructor1', 'instructor1',1); 
INSERT INTO users VALUES(4, 'instructor2', 'instructor2',1); 



CREATE TABLE IF NOT EXISTS marks (
    id INTERGER NOT NULL,
    name VARCHAR(20) NOT NULL,
    mark INTERGER CHECK(Mark>0) NOT NULL
);


INSERT INTO marks VALUES(1, 'Student1', '50');
INSERT INTO marks VALUES(1, 'Student1', '100');