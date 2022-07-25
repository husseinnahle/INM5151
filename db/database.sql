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
  progress text,
  type varchar
);
