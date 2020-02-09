-- :name user_add :insert
insert into user (id, user_name, org)
values (:id, :user_name, :org)