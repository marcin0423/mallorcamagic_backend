FROM python:3.9-buster
WORKDIR /backend
COPY . .
EXPOSE 8000
RUN pip install --upgrade pip
RUN pip install -r requirments.txt
RUN python3 manage.py migrate
RUN python3 manage.py collectstatic --noinput
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
