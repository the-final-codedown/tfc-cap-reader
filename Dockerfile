FROM python:3.8.1-alpine3.11

RUN pip install --no-cache-dir pymongo falcon gunicorn

ADD profile-system.py ./

EXPOSE 8083

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8083 'profile-system:setup_profile()'"]


