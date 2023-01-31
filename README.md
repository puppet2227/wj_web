安装python库
pip install pymysql    
pip install Django==2.1   
#数据库
sudo service mysql start
python manage.py makemigrations   
python manage.py migrate 
#安装vue库
npm i element-ui -S 
npm install echarts --save
#开启两服务
python manage.py runserver 0:8000   
npm run serve  

   