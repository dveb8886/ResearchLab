-- :name stat_create
create table if not exists stat (
    id integer primary key,
    stat_name varchar(25),
    fund int,
    color_line varchar(25),
    color_fill varchar(25)
);