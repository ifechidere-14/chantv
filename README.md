# Chan-TV

A Django streaming platform foundation with a database-backed catalogue, channel guide, search, watch pages, authentication, watchlists, favourites, and admin management.

## Run locally

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the website and `/admin/` to manage channels, programmes, schedules, and users.

## Connect real streaming content

In Django Admin, create or edit a `Programme` and set `video_url` to an authorised MP4 or HLS stream. Set `image_url` for its poster. Add `Channel` records with their authorised `stream_url` values, then add `ScheduleItem` records for the TV guide.

The project includes SQLite by default for local development. For production, set a strong `SECRET_KEY`, `DEBUG = False`, `ALLOWED_HOSTS`, HTTPS settings, and move to PostgreSQL or another managed database.

Only use video, channel, movie, and sports feeds for which you own or have distribution rights.

## Deploy to Render

1. Push this repository to GitHub or GitLab.
2. In Render, choose **New > Blueprint** and connect the repository.
3. Render will use `render.yaml` to create the web service and PostgreSQL database.
4. Add `ADMIN_USERNAME` and `ADMIN_PASSWORD` in the service Environment settings. The deploy migration creates that superuser automatically, so Render Free does not require Shell access. Use `admin` for `ADMIN_USERNAME` and choose a strong value for `ADMIN_PASSWORD`. Existing users are never overwritten on later deploys.

Set `CSRF_TRUSTED_ORIGINS` to the exact HTTPS URL Render gives your service if you change the default service name. Do not deploy the development `admin/admin` password.
