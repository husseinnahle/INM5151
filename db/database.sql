create table sujet (
  id integer primary key,
  nom varchar(30) unique,
  informations text
);

create table user (
  id integer primary key,
  username varchar(25) unique,
  email varchar(100),
  salt varchar(32),
  hash varchar(128),
  member integer,
  progress text,
  type_id integer references user_type (id)
);

create table user_type (
  id integer primary key,
  description varchar (20) unique
);

insert into user_type (id, description) values (1, 'admin');
insert into user_type (id, description) values (2, 'instructor');
insert into user_type (id, description) values (3, 'user');