# Diplom project
> :ramen: It is a social network project where users can share their recipes. 
> *They can share their recipes, subscribe to other users, add recipes to their 'favorites' and to their 'shopping list', as well as download a PDF list of products for recipes in their 'shopping list'.*
### Currently working at
- http://foodie.ddns.net/recipes
### Author
Sofia
____
### Backend development technologies
- Python 3.7
- Django 2.2.19
- Docker 20.10.8
- nginx 1.18.0-0ubuntu1.2
____
### Launching project in dev mode
- Install and activate the virtual environment
- Install dependencies from the file requirements.txt
```bash
pip install -r requirements.txt
``` 
- In the file folder manage.py run the command:
```bash
python3 manage.py runserver
```
____
### Launching project in Docker
- Install the image from DockerHub
```bash
docker pull anokhovskaya/foodgram-project-react
``` 
- You need to assemble the container and run
```bash
docker-compose up -d --build
``` 
- You need to make migrations
```bash
docker-compose exec web python manage.py migrate --noinput
```
- You need to create admin user
```bash
docker-compose exec web python manage.py createsuperuser
```
- You need to collect static
```bash
docker-compose exec web python manage.py collectstatic --no-input
```
- You need to create a file .env with environment variables for working with the database


