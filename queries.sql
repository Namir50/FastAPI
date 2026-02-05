select * from products where "on sale" =true and "Price" >50;

select * from products where id in (1,2,3);

select * from products;

select * from products where "Name" like '%TV';

select * from products where "Name" not like '%e%';

select * from products order by "Price";

select * from products order by "Price" desc;

select * from products order by "created at" desc; 

select * from products where "Price" > 10 order by "Price" ASC limit 3;

select * from products where "Price" > 10 order by "Price" ASC offset 3;

select * from products where "Price" > 10 order by "Price" ASC limit 3 offset 3;

Insert into products ("Name", "Price") Values('battery', '5');

Insert into products ("Name", "Price") Values('cover', '2') returning *;


Insert into products ("Name", "Price") Values('desk', '2') returning "Name","Price";


delete from products where "Name" = 'desk';

delete from products where "Name" = 'cover' returning *;


update products set "Price" = 250 where "id" = 1;

update products set "Price" = 17 where "Name" = 'power bank' returning *;
