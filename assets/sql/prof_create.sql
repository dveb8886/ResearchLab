-- :name prof_create
create table if not exists profile (
    id integer primary key,
    prof_name varchar(25),
    org int
);
