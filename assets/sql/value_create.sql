-- :name value_create
create table if not exists value (
    id integer primary key,
    stat int,
    x_date int,
    y_value real
);