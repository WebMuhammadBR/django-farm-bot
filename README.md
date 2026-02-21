# django-farm-bot

TETRATEX uchun Django + Telegram bot loyihasi.

## Deploy uchun tayyorlangan narsalar
- `config/settings.py` env o'zgaruvchilar bilan production-safe ko'rinishga o'tkazildi.
- `whitenoise` orqali static fayllarni productionda berish yoqildi.
- `gunicorn` + `Procfile` qo'shildi (Railway/Render/Heroku uslubidagi deploylar uchun).
- `.env.example` qo'shildi.

## Tez deploy checklist
1. Virtual environment yarating va kutubxonalarni o'rnating.
2. `.env.example` dan `.env` ochib, qiymatlarni to'ldiring.
3. `DJANGO_DEBUG=False` qiling.
4. Domainlaringizni `DJANGO_ALLOWED_HOSTS` va `DJANGO_CSRF_TRUSTED_ORIGINS` ga kiriting.
5. `python manage.py collectstatic --noinput`
6. `python manage.py migrate --noinput`
7. `gunicorn config.wsgi:application --bind 0.0.0.0:8000`

## Lokal ishga tushirish
```bash
pip install pipenv
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py runserver
```

## Muhim env o'zgaruvchilar
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
