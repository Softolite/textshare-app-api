# textshare-app-backend
python/django server for the textshare app


run make migrations command:
docker-compose run --rm app sh -c "python manage.py makemigrations"

apply the migrations:
docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"

if migrations doesn't work, try clearing the volume:
docker volume list
docker volume rm <volume-id>

run unit tests:
docker-compose run --rm app sh -c "flake8 && python manage.py test"

run the app:
docker-compose up