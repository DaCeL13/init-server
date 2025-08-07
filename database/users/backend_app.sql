CREATE USER 'backend_app'@'localhost' IDENTIFIED BY 'Backapp@v1.';

GRANT ALL PRIVILEGES ON grupo_g.* TO 'backend_app'@'localhost';

FLUSH PRIVILEGES;
