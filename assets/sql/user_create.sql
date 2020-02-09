-- :name user_create
create table if not exists user (
    id integer primary key,
    user_name varchar(25),
    org int
);