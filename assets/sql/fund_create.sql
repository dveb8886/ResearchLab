-- :name fund_create
create table if not exists fund (
    id integer primary key,
    fund_name varchar(25),
    prof int
);