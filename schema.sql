SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema d0018e_ecommerce
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema d0018e_ecommerce
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `d0018e_ecommerce` DEFAULT CHARACTER SET utf8 ;
USE `d0018e_ecommerce` ;

-- -----------------------------------------------------
-- Table `d0018e_ecommerce`.`categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `d0018e_ecommerce`.`categories` ;

CREATE TABLE IF NOT EXISTS `d0018e_ecommerce`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `parent_id` INT NULL,
  `name` NVARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`),
  INDEX `categories_parent_id_idx` (`parent_id` ASC),
  CONSTRAINT `categories_parent_id`
    FOREIGN KEY (`parent_id`)
    REFERENCES `d0018e_ecommerce`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `d0018e_ecommerce`.`products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `d0018e_ecommerce`.`products` ;

CREATE TABLE IF NOT EXISTS `d0018e_ecommerce`.`products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NULL,
  `name` NVARCHAR(255) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `stock_quantity` INT NULL,
  `rating` DOUBLE NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `products_category_id_idx` (`category_id` ASC),
  CONSTRAINT `products_category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `d0018e_ecommerce`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `d0018e_ecommerce`.`customers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `d0018e_ecommerce`.`customers` ;

CREATE TABLE IF NOT EXISTS `d0018e_ecommerce`.`customers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` NVARCHAR(255) NOT NULL,
  `password` NVARCHAR(255) NOT NULL,
  `name` NVARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `last_login` DATETIME,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `customers_email_udx` (`email` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `d0018e_ecommerce`.`reviews`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `d0018e_ecommerce`.`reviews` ;

CREATE TABLE IF NOT EXISTS `d0018e_ecommerce`.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `comment` NVARCHAR(4096) NULL,
  `rating` INT NOT NULL,
  `product_id` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `reviews_product_id_idx` (`product_id` ASC),
  INDEX `reviews_customer_id_idx` (`customer_id` ASC),
  UNIQUE INDEX `customer_product_udx` (`product_id` ASC, `customer_id` ASC),
  CONSTRAINT `reviews_product_id_fk`
    FOREIGN KEY (`product_id`)
    REFERENCES `d0018e_ecommerce`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `reviews_customer_id_fk`
    FOREIGN KEY (`customer_id`)
    REFERENCES `d0018e_ecommerce`.`customers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `d0018e_ecommerce`.`orders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `d0018e_ecommerce`.`orders` ;

CREATE TABLE IF NOT EXISTS `d0018e_ecommerce`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `fulfilled` TINYINT(1) NOT NULL,
  `created_at` DATETIME NOT NULL,
  `fulfilled_at` DATETIME NULL,
  `price` DECIMAL(10,2) NULL,
  PRIMARY KEY (`id`),
  INDEX `orders_customer_id_idx` (`customer_id` ASC),
  CONSTRAINT `orders_customer_id_fk`
    FOREIGN KEY (`customer_id`)
    REFERENCES `d0018e_ecommerce`.`customers` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `d0018e_ecommerce`.`orderitems`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `d0018e_ecommerce`.`orderitems` ;

CREATE TABLE IF NOT EXISTS `d0018e_ecommerce`.`orderitems` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `price` DECIMAL(10,2) NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `orderitems_order_id_idx` (`order_id` ASC),
  INDEX `orderitems_product_id_idx` (`product_id` ASC),
  UNIQUE INDEX `orderitems_product_order_udx` (`order_id` ASC, `product_id` ASC),
  CONSTRAINT `orderitems_order_id_fk`
    FOREIGN KEY (`order_id`)
    REFERENCES `d0018e_ecommerce`.`orders` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `orderitems_product_id_fk`
    FOREIGN KEY (`product_id`)
    REFERENCES `d0018e_ecommerce`.`products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
