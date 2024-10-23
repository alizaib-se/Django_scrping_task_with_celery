**Project Setup Guidelines**

Python verison: 3.11.5
1. create virtual enviroment
2. 

**About Project**

celery worker working on scheduler jobs
![img.png](img.png)


Celery beat for scheduled jobs
![img_1.png](img_1.png)


rabbit mq broker in docker container
![img_2.png](img_2.png)


rabbit mq dashboard for monitoring
![img_14.png](img_14.png)


creat a brand
![img_3.png](img_3.png)

view scraped products of listed brands
brand_id: 3
![img_4.png](img_4.png)

brand_id: 4
![img_5.png](img_5.png)

brand_id: 7
![img_6.png](img_6.png)

Curl format to scrap brand 7 products
` curl -X POST http://127.0.0.1:8000/brands/scrape/ \
-H "Content-Type: application/json" \
-d '{"brand_id": 7}'`



**DB Design with foreign key relation**

![img_9.png](img_9.png)


brand table
![img_12.png](img_12.png)


brand products
![img_13.png](img_13.png)

Django admin
brands
![img_7.png](img_7.png)

products
![img_8.png](img_8.png)

celery integration
![img_10.png](img_10.png)

celery beat integration for scheduler to update products 4 times a day
![img_11.png](img_11.png)

