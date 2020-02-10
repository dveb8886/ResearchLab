-- :name stat_update
update stat
set stat_name = :stat_name,
    color_line = :color_line,
    color_fill = :color_fill
where id = :stat_id