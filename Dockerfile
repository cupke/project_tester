FROM python:3.10
COPY . /usr/src/app/bot/
WORKDIR /usr/src/app/bot/
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /usr/src/app/bot/requirements.txt
CMD ["python", "start.py"]