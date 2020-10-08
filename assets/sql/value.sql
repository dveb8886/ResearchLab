-- :name value_create
create table if not exists value (
    id integer primary key,
    stat int,
    x_date int,
    y_value real
);

-- :name value_add :insert
insert into value (stat, x_date, y_value)
values (:stat, :x_date, :y_value);