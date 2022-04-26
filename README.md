# Project Title

## AutoInvoice Generator

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>
This is an an app that handles the order handling of products in the backend. Firebase token authentication is used to authenticate users and the apps features include: 
-  get available products list
-  order products based on quantity
-  update existing order
-  dynamically generate invoice in pdf format

## Getting Started <a name = "getting_started"></a>
Clone the project repository
```
git clone https://github.com/shadyskies/AutoInvoice.git
```

### Prerequisites

Since this project requires firebase config to be done, create your own firebase application and generate key for the service account. Download the keys json and add it to the project root. Add your own web app config to the ftoken.html as well as firebase.js files. Now the backend is ready to work with firebase.


### Installing

Create a virtualenv and install the required dependencies
```
pip3 install -r requirements.txt
```
Migrate the schema to database.
```
python3 manage.py migrate 
```

Create a superuser
```
python3 manage.py createsuperuser
```

## Usage <a name = "usage"></a>

Start the server
```
python3 manage.py runserver
```