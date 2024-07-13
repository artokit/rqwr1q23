FROM python:3.9

#
WORKDIR /code
EXPOSE 8000

#
COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env
COPY ./alembic.ini /code/alembic.ini

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./src /code/src

CMD ["fastapi", "run", "src/main.py", "--port", "8000"]