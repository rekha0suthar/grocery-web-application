# Grocery Store Web Application

## Demo Video - https://drive.google.com/file/d/1ZohEOUIFfpIQE_fatzBn49H30AK9q0IE/view

## React version of application - https://github.com/rekha0suthar/grocery-store-react-version

### Admin Side
![f57f9e23-7cf9-4b7e-a31e-67dc80762398](https://github.com/rekha0suthar/grocery-web-application/assets/71004640/1c02c9f9-8906-45a0-a313-32666fdc85ea)

### User Side
![3e55f4c7-5f35-485a-acff-2097e7521358](https://github.com/rekha0suthar/grocery-web-application/assets/71004640/ea430cc1-66fa-4cd3-b0f3-c2ee008e7af5)

### Store Manager Side
![4162e8e6-a847-4752-a6f0-f6f55b278f3a](https://github.com/rekha0suthar/grocery-web-application/assets/71004640/ecbd72c6-c3e9-4dc4-a223-57c1a4d43c0c)
![e71e8061-d672-4b40-b561-8f5c3d40e043](https://github.com/rekha0suthar/grocery-web-application/assets/71004640/a7ec7548-d20e-49f5-b227-ce940a10ca36)


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
