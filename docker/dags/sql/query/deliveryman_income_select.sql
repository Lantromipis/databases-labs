SELECT dm.id                                      as deliveryman_id,
       dm.name                                    as deliveryman_name,
       t.year                                     as year,
       min(t.month) + 1                           as month,
       count(o.id)                                as orders_amount,
       sum(o.cost)                                as orders_total_cost,
       avg(d.rating)                              as rating,
       sum(d.tips)                                as tips,
       sum(o.cost) * 0.5                          as company_commission,
       deliveryman_order_income(o.cost, d.rating) as deliveryman_order_income
FROM dds.dm_deliveryman dm
         JOIN dds.fact_delivery d ON d.deliveryman_id = dm.id
         JOIN dds.dm_order o on o.id = d.order_id
         JOIN dds.dm_time t on t.id = o.order_time_id
WHERE o.final_status = 'CLOSED'
  AND t.time_mark
    BETWEEN (
        case
            when date_part('day', now()) < 21
                then
                (
                    case
                        when date_part('month', now()) = 1
                            then make_date((date_part('year', now()) - 1)::int, 11, 21)
                        when date_part('month', now()) = 2
                            then make_date((date_part('year', now()) - 1)::int, 12, 21)
                        else
                            make_date(date_part('year', now())::int, (date_part('month', now()) - 2)::int, 21)
                        end
                    )
            else
                (
                    case
                        when date_part('month', now()) = 1
                            then make_date((date_part('year', now()) - 1)::int, 12, 21)
                        else
                            make_date(date_part('year', now())::int, (date_part('month', now()) - 1)::int, 21)
                        end
                    )
            end
        )
    AND
    (
        case
            when date_part('day', now()) < 21
                then
                (
                    case
                        when date_part('month', now()) = 12
                            then make_date((date_part('year', now()) - 1)::int, 12, 21)
                        else
                            make_date(date_part('year', now())::int, (date_part('month', now()) - 1)::int, 21)
                        end
                    )
            else
                make_date(date_part('year', now())::int, date_part('month', now())::int, 21)
            end
        )
GROUP BY dm.id, dm.name, t.year;