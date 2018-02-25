# Create a separate user from root, if necessary
# CREATE USER 'new_user'@'%' IDENTIFIED BY PASSWORD 'password';
# Grant privileges on new_user
# GRANT ALL PRIVILEGES ON cs5331_secret_diary.* TO 'new_user'@'%' WITH GRANT OPTION;

# Create database tables
CREATE TABLE diary_user ( `userid` INT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE, `username` VARCHAR(255) NOT NULL UNIQUE, `password` VARCHAR(255) NOT NULL, `fullname` VARCHAR(255) NOT NULL, `age` INT(3) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
CREATE TABLE diary_session ( `userid` INT NOT NULL UNIQUE, `session_token` VARCHAR(255) NOT NULL UNIQUE, `session_expiry` DATE NOT NULL ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
CREATE TABLE diary_entry ( `entry_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE, `userid` INT NOT NULL, `entry_date` DATE NOT NULL, `entry_is_public` INT NOT NULL, `entry_text` VARCHAR(255) ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

# Create database index for diary entry table
CREATE UNIQUE INDEX `diary_entry_table_index` ON `diary_entry` ( `entry_id` DESC);

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
