-- :name stat_readvalues :many
select * from value
where stat = :stat_id;