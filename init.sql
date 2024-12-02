CREATE USER referral_admin WITH PASSWORD 'referral_password';
CREATE DATABASE my_referral_system_db OWNER referral_admin;
GRANT ALL PRIVILEGES ON DATABASE my_referral_system_db TO referral_admin;