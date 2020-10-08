-- :name stat_create
create table if not exists stat (
    id integer primary key,
    stat_name varchar(25),
    fund int,
    color_line varchar(25),
    color_fill varchar(25)
);

-- :name stat_add :insert
insert into stat (stat_name, fund)
values (:stat_name, :fund);

-- :name stat_clearvalues
delete from value
where stat = :stat_id;

-- :name stat_delete
delete from stat
where id = :stat_id;

-- :name stat_find :one
select * from stat where id = :id;

-- :name stat_find_by_name :one
select * from stat where stat_name = :stat_name and fund = :fund;

-- :name stat_list :many
select * from stat where fund = :fund_id;

-- :name stat_readvalues :many
select x_date, y_value from value
where stat = :stat_id
order by x_date;

-- :name stat_update
update stat
set stat_name = :stat_name,
    color_line = :color_line,
    color_fill = :color_fill
where id = :stat_id