SELECT dm.id as deliveryman_id,
       dm.name as deliveryman_name,
       count(o.id)   as orders_amount,
       sum(o.cost)   as orders_total_cost,
       avg(d.rating) as rating,
       sum(d.tips) as tips,
       sum(o.cost) * 0.5 as company_commission,
       deliveryman_order_income(o.cost, d.rating) as deliveryman_order_income
FROM dds.dm_deliveryman dm
         JOIN dds.dm_delivery d ON d.deliveryman_id = dm.id
         JOIN dds.dm_order o on o.id = d.order_id
WHERE o.final_status = 'CLOSED'
  AND o.order_date BETWEEN '2024-04-21' AND '2024-05-21'
GROUP BY dm.id, dm.name;