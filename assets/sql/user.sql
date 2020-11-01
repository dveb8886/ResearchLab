-- :name user_create
create table if not exists user (
    id integer primary key,
    username varchar(25),
    password varchar(25)
);

-- :name user_add :insert
insert into user (username)
values (:username)

-- :name user_changepass :affected
update user set password = :password
where id = :id

-- :name user_find :one
select * from user where id = :id;

-- :name user_find_byname :one
select * from user where username = :username;

-- :name user_search :many
select * from user where username like :search;

-- :name user_get_many_by_id :many
select * from user where id in :user_ids