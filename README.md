# textshare App Backend
Python/Django backend server for the textshare.top app

## App Structure

## CICD Flow

Here is an illustration of a full CICD flow for textshare.top backend app from developer commit to k8s deployment

<img width="788" alt="Screenshot 2023-11-25 at 16 45 27" src="https://github.com/Softolite/textshare-app-api/assets/5890558/b64e1f56-2221-4314-97b1-a7c028e8172e">

## Developer guidelines

run make migrations command:
> docker-compose run --rm app sh -c "python manage.py makemigrations"

apply the migrations:
> docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"

if migrations doesn't work, try clearing the volume:
> docker volume list
>
> docker volume rm <volume-id>

run unit tests:
> docker-compose run --rm app sh -c "flake8 && python manage.py test"

run the app:

> docker-compose up

