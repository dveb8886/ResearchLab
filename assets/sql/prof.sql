-- :name prof_create
create table if not exists profile (
    id integer primary key,
    prof_name varchar(25),
    org int
);

-- :name prof_add :insert
insert into profile (prof_name, org)
values (:prof_name, :org)

-- :name prof_find :one
select * from profile where id = :id;

-- :name prof_list :many
select * from profile where org = :org_id;