/*Hay algún seller con múltiples publicaciones? En caso de que si, con
cuantas?*/
select count(id) as 'publicaciones' , seller_id from items where seller_id in
    (select seller_id from items  group by seller_id having count(seller_id) > 1) 
    group by seller_id

/*Cuál es el precio promedio en dólares?*/
 select AVG(usd_price) from items

 /*Métodos de Shipping que ofrecen?*/
select distinct logistic_type from items


/*Porcentaje de artículos con garantía?*/
SET @total := (select count(*) from items where (warranty is not null) and (warranty != 'Sem garantia'));
select 
    CONCAT(ROUND(@total  * 100 / count(id), 2), '%')  AS porcentaje
 from
items;