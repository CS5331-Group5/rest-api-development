# Create a separate user from root, if necessary
# CREATE USER 'new_user'@'%' IDENTIFIED BY PASSWORD 'password';
# Grant privileges on new_user
# GRANT ALL PRIVILEGES ON cs5331_secret_diary.* TO 'new_user'@'%' WITH GRANT OPTION;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
  `encrypted_password` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
  `fullname` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
  `age` INT(11) NOT NULL DEFAULT 0,
  `sign_in_count` INT(11) NOT NULL DEFAULT 0,
  `locked_at` TIMESTAMP NULL DEFAULT NULL,
  `session_token` VARCHAR(255) COLLATE utf8_unicode_ci NOT NULL,
  `session_created_at` TIMESTAMP NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_user_on_username` (`username`),
  UNIQUE KEY `index_user_on_session_token` (`session_token`)
) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `diary`;

CREATE TABLE `diary` (
  `entry_id` INT NOT NULL AUTO_INCREMENT,
  `author_id` INT(11) NOT NULL,
  `entry_date` TIMESTAMP NULL DEFAULT NULL,
  `entry_title` VARCHAR(100) COLLATE utf8_unicode_ci,
  `entry_text` TEXT COLLATE utf8_unicode_ci,
  `entry_is_public` BOOL NOT NULL,
  PRIMARY KEY (`entry_id`),
  UNIQUE KEY `index_user_on_entry_id` (`entry_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


