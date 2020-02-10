-- :name stat_find_by_name :one
select * from stat where stat_name = :stat_name and fund = :fund;