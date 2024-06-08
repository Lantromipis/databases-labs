SET SEARCH_PATH TO src;

INSERT INTO category (category_id, name, percent, min_payment) VALUES (1, 'default', 0.0, 0.0);
INSERT INTO category (category_id,name, percent, min_payment) VALUES (2, 'bronze', 0.05, 20000.0);
INSERT INTO category (category_id,name, percent, min_payment) VALUES (3, 'silver', 0.1, 50000.0);
INSERT INTO category (category_id,name, percent, min_payment) VALUES (4, 'gold', 0.15, 100000.0);
INSERT INTO category (category_id,name, percent, min_payment) VALUES (5, 'platinum', 0.2, 200000.0);

INSERT INTO dish (dish_id, name, price) VALUES (1, 'beef tartare', 500);
INSERT INTO dish (dish_id, name, price) VALUES (2, 'beef steak', 1200);
INSERT INTO dish (dish_id, name, price) VALUES (3, 'fried chicken', 450);
INSERT INTO dish (dish_id, name, price) VALUES (4, 'chicken soup', 300);
INSERT INTO dish (dish_id, name, price) VALUES (5, 'pizza margarita', 500);
INSERT INTO dish (dish_id, name, price) VALUES (6, 'pizza pepperoni', 600);
INSERT INTO dish (dish_id, name, price) VALUES (7, 'pizza four cheeses', 600);
INSERT INTO dish (dish_id, name, price) VALUES (8, 'apple juice', 150);
INSERT INTO dish (dish_id, name, price) VALUES (9, 'cherry joice', 150);
INSERT INTO dish (dish_id, name, price) VALUES (10, 'orange juice', 150);
INSERT INTO dish (dish_id, name, price) VALUES (11, 'french fries', 250);
INSERT INTO dish (dish_id, name, price) VALUES (12, 'boiled potato', 250);
INSERT INTO dish (dish_id, name, price) VALUES (13, 'draniki', 350);

INSERT INTO client (client_id, bonus_balance, category_id) VALUES (1, 13.42 , 1);
INSERT INTO client (client_id, bonus_balance, category_id) VALUES (2, 158.0 , 2);
INSERT INTO client (client_id, bonus_balance, category_id) VALUES (3, 1838.35 , 4);

INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (1, 1, 2, 1, '2024-05-09 18:40:25.000000', 1000, 100);
INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (1, 2, 1, 1, '2024-05-09 18:40:25.000000', 1200, 200);
INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (1, 3, 3, 1, '2024-05-09 18:40:25.000000', 1350, 200);

INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (2, 5, 1, 1, '2024-05-09 18:40:25.000000', 500, 0);
INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (2, 6, 3, 1, '2024-05-09 18:40:25.000000', 1800, 50);
INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (2, 7, 2, 1, '2024-05-09 18:40:25.000000', 1200, 100);

INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (3, 8, 2, 1, '2024-05-09 18:40:25.000000', 300, 10);
INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (3, 11, 4, 1, '2024-05-09 18:40:25.000000', 1000, 50);
INSERT INTO payment (client_id, dish_id, dish_amount, order_id, order_time, order_sum, tips) VALUES (3, 13, 3, 1, '2024-05-09 18:40:25.000000', 1050, 50);