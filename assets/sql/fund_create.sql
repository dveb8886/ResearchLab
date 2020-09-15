-- :name fund_create
create table if not exists fund (
    id integer primary key,
    fund_name varchar(25),
    fund_manager varchar(25),
    fund_vintage int,
    fund_nav decimal(18, 3),
    fund_unfunded decimal(18, 3),
    prof int
);