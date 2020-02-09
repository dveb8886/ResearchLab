-- :name stat_create
create table if not exists stat (
    id integer primary key,
    stat_name varchar(25),
    fund int
);