sudo apt update
sudo apt install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx


#original conf if not using reverse proxy
sudo mkdir -p /var/www/html
sudo chown -R www-data:www-data /var/www/html

##############################
cd /etc/nginx/sites-available
sudo vi web-01
sudo ln -s /etc/nginx/sites-available/web-01 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

####Errors####
cat /var/log/nginx/error.log
