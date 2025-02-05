-- MySQL Script generated by MySQL Workbench
-- Sat Feb 18 17:57:59 2017
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema ece1779_a1
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ece1779_a1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ece1779_a1`
  DEFAULT CHARACTER SET utf8;
USE `ece1779_a1`;

-- -----------------------------------------------------
-- Table `ece1779_a1`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1779_a1`.`users`;

CREATE TABLE IF NOT EXISTS `ece1779_a1`.`users` (
  `id`       INT         NOT NULL AUTO_INCREMENT,
  `login`    VARCHAR(16) NOT NULL,
  `password` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ece1779_a1`.`images`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1779_a1`.`images`;

CREATE TABLE IF NOT EXISTS `ece1779_a1`.`images` (
  `id`     INT          NOT NULL AUTO_INCREMENT,
  `userId` INT          NOT NULL,
  `key1`   VARCHAR(255) NOT NULL,
  `key2`   VARCHAR(255) NOT NULL,
  `key3`   VARCHAR(255) NOT NULL,
  `key4`   VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_images_users_idx` (`userId` ASC),
  CONSTRAINT `fk_images_users`
  FOREIGN KEY (`userId`)
  REFERENCES `ece1779_a1`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
  ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `ece1779_a1`.`setting`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ece1779_a1`.`setting`;

CREATE TABLE IF NOT EXISTS `ece1779_a1`.`setting` (
  `autoScaling` INT NOT NULL,
  `cpuGrow`     INT NOT NULL,
  `cpuShrink`   INT NOT NULL,
  `ratioExpand` INT NOT NULL,
  `ratioShrink` INT NOT NULL
)
  ENGINE = InnoDB;

INSERT INTO setting (autoScaling, cpuGrow, cpuShrink, ratioExpand, ratioShrink) VALUES (0, 90, 10, 2, 2);


SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;
