-- :name org_create
create table if not exists organization (
    id integer primary key,
    org_name varchar(25)
);