-- :name org_create
create table if not exists organization (
    id integer primary key,
    org_name varchar(25)
);

-- :name org_add :insert
insert into organization (org_name)
values (:org_name)

-- :name org_find :one
select * from organization where id = :id;

-- :name org_list :many
select * from organization;
