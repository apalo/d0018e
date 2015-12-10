use d0018e_ecommerce;

INSERT INTO categories (id, name)
VALUES (1, "laptops"), (2, "desktops"), (3, "monitors"), 
       (4, "keyboards"), (5, "mice"), (6, "books");


INSERT INTO products (name, price, stock_quantity, rating, category_id)
VALUES ("Macbook Air 10-inch", 10995, 2, 4.9, 1), 
       ("Samsung Series 9 ultrabook", 12495, 1, 4.7, 1), 
       ("Dell Family Computer", 4999, 5, 3.7, 2),
       ("HP Office Computer", 6995, 3, 3.9, 2),
       ("HP Gaming Deluxe", 13795, 1, 4.2, 2),
       ("BenQ 24-inch Full-HD", 1795, 2, 4.9, 3),
       ("Logitech generic keyboard", 195, 7, 4.3, 4),
       ("Logotech gaming keyboard", 399, 5, 4.1, 4),
       ("Logitech gaming mouse", 599, 1, 3.9, 5),
       ("Django for noobs", 299, 1, 5.0, 6);
