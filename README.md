# Grocery Store Web Application

## Project setup
## to run frontend side code, run below command
```
cd frontend
npm install
npm run serve
```
## to run backend side code, run below command
```
cd backend
python app.py

```
## to send monthly report, export csv report run below command
```
celery -A task.celery worker --loglevel=info
```

## to send reminder, run additional below command
```
python reminder.py

```
