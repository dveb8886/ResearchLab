-- :name fund_add :insert
insert into fund (fund_name, fund_manager, fund_vintage, fund_nav, fund_unfunded, prof)
values (:fund_name, :fund_manager, :fund_vintage, :fund_nav, :fund_unfunded, :prof);