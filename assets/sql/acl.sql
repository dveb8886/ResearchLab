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
where id = :id;

-- :name get_user_role_assignments :many
select ru.user_id as user_id, ru.role_id as role_id
from role_user ru
where ru.user_id in :user_ids and ru.role_id in :role_ids;

-- :name get_role_assignments :many
select ru.user_id, ru.role_id
from role_user ru
where ru.role_id in :role_ids;

-- :name get_roles_by_resource :many
select *
from role r
where r.name like :resource;

