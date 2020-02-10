-- :name stat_readvalues :many
select x_date, y_value from value
where stat = :stat_id
order by x_date;