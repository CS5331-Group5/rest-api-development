# Create a separate user from root, if necessary
# CREATE USER 'new_user'@'%' IDENTIFIED BY PASSWORD 'password';
# Grant privileges on new_user
# GRANT ALL PRIVILEGES ON cs5331_secret_diary.* TO 'new_user'@'%' WITH GRANT OPTION;

INSERT INTO user (username, encrypted_password, fullname, age, sign_in_count, locked_at, session_token, session_created_at, created_at, updated_at) 
values ('AzureDiamond','$2b$12$vWIQBPSk2KfWwqLpzx.tOOSkpgkbt90KsKwVzLRVFdshtG8tE78cC','Joey Pardella',20,0,NULL,'f9b71a4f-bdbc-4966-8977-af05d9010360','2018-02-26 22:46:24','2018-02-26 22:46:24','2018-02-26 22:46:24');


