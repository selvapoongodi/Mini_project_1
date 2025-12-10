CREATE TABLE first_schema.userlist (
	username varchar (100) primary key,
    password_hash varchar (255),
    role varchar (100)
    );
    
insert into first_schema.userlist
values ('client1','stu123', 'client'),
('client2','stu123', 'client'),
('client3','stu123', 'client'),
('client4','stu123', 'client'),
('client5','stu123', 'client'),
('client6','stu123', 'client'),
('client7','stu123', 'client'),
('client8','stu123', 'client'),
('client9','stu123', 'client'),
('client10','stu123', 'client'),
('support1','adm123', 'support'),
('support2','adm123', 'support'),
('support3','adm123', 'support'),
('support4','adm123', 'support'),
('support5','adm123', 'support'),
('support6','adm123', 'support'),
('support7','adm123', 'support'),
('support8','adm123', 'support'),
('support9','adm123', 'support'),
('support10','adm123', 'support');

CREATE TABLE queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_username VARCHAR(100),
    email VARCHAR(100),
    mobile VARCHAR(20),
    heading VARCHAR(255),
    description TEXT,
    status VARCHAR(20),
    created_time DATETIME,
    closed_time DATETIME
);

select * from first_schema.userlist;

select * from queries;