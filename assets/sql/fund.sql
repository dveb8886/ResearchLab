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

-- :name fund_list :many
select * from fund where prof = :prof_id;

-- :name fund_find :one
select * from fund where id = :id;

-- :name fund_add :insert
insert into fund (fund_name, fund_manager, fund_vintage, fund_nav, fund_unfunded, prof)
values (:fund_name, :fund_manager, :fund_vintage, :fund_nav, :fund_unfunded, :prof);
