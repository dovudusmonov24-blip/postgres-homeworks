-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products
    ADD CONSTRAINT check_unit_price_positive CHECK (unit_price > 0);
 
-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
ALTER TABLE products
    ADD CONSTRAINT check_discontinued_values CHECK (discontinued IN (0, 1));
 
-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
CREATE TABLE discontinued_products AS
SELECT *
FROM products
WHERE discontinued = 1;
 
-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key. Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.
-- Внешний ключ order_details -> products (fk_order_details_products) не даст удалить продукты,
-- на которые уже есть ссылки в order_details. Так как исторические записи в order_details
-- удалять нельзя, снимаем ограничение внешнего ключа (саму историю заказов при этом не трогаем):
ALTER TABLE order_details
    DROP CONSTRAINT fk_order_details_products;
 
DELETE FROM products
WHERE discontinued = 1;
