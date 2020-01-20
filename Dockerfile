FROM alexisgra/falcon-alpine-python-3.7.4:latest

ADD profile-system.py ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir pymongo
EXPOSE 8083

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:8083 'profile-system:setup_profile()'"]


