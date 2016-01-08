use d0018e_ecommerce;

INSERT INTO categories (id, name)
VALUES (1, "laptops"), (2, "desktops"), (3, "monitors"), 
       (4, "keyboards"), (5, "mice"), (6, "books");


INSERT INTO products (name, price, stock_quantity, rating, category_id)
VALUES ("Macbook Air 10-inch", 10995, 2, 0.0, 1), 
       ("Samsung Series 9 ultrabook", 12495, 1, 0.0, 1), 
       ("Dell Family Computer", 4999, 5, 0.0, 2),
       ("HP Office Computer", 6995, 3, 0.0, 2),
       ("HP Gaming Deluxe", 13795, 1, 0.0, 2),
       ("BenQ 24-inch Full-HD", 1795, 2, 0.0, 3),
       ("Logitech generic keyboard", 195, 7, 0.0, 4),
       ("Logitech gaming keyboard", 399, 5, 0.0, 4),
       ("Logitech gaming mouse", 599, 1, 0.0, 5),
       ("Django for noobs", 299, 1, 0.0, 6);
