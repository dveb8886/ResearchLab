-- :name role_user_create
create table if not exists role_user (
    id integer primary key,
    user_id integer,
    role_id integer
);

-- :name role_create
create table if not exists role (
    id integer primary key,
    name varchar(25),
    active integer
);

-- :name user_get_roles :many
select r.*
from role r
join role_user ru on r.id = ru.role_id
where ru.user_id = :user_id

-- :name role_add :insert
insert into role (name, active)
values (:name, :active)

-- :name role_find :one
select * from role where id = :id;

-- :name role_find_byname :one
select * from role where name = :name;

-- :name user_add_to_role :insert
insert into role_user (user_id, role_id)
values (:user_id, :role_id)

-- :name user_remove_from_role
delete from role_user
where user_id = :user_id and role_id = :role_id

-- :name enable_role :affected
update role set active = :active
where id = :id




---- :name grant_create
--create table if not exists grant (
--    id integer primary key,
--    permission_id integer,
--    role_id integer,
--    active integer
--);
--
---- :name permission_create
--create table if not exists permission (
--    id integer primary key,
--    resource_id integer,
--    name varchar(25),
--    active integer
--);
--
---- :name resource
--create table if not exists resource (
--    id integer primary key,
--    name varchar(25),
--    active integer
--);


