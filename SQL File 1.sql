create database if not exists backend_db;

create table user ( 
id int auto_increment primary key,
name varchar(255) not null,
email varchar (255) not null,
password varchar (255) not null
);

use backend_db;

insert  into user (name, email, password)
values (1, "Sam Larry", "dhee@gmail.com", "Sam123"),
(2, "Joe Boy", "joeey@publica.com", "joejoe23");

select * from users;

select id, name from user;