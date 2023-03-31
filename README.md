# The project of the store online 

Django project for managing local shop online with products and categories of products, 
managing the cart, orders and also a payment system.


## Installation

Python3 must be already installed

### Installing using GitHub

Install PostgreSQL and create db

```shell
git clone https://github.com/Viktor-Beniukh/online-store-service.git
cd online_store_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   
```
You need to create `.env` file and add there the variables with your according values: 
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;
- `STRIPE_PUBLIC_KEY` & `STRIPE_SECRET_KEY`: your keys received after registration on the Stripe website.


## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`


## Features

- Authentication functionally for User:
  - registration and authorisation;
  - create and edit user credentials;
  - create and edit user profile;
  - change password if you need;
  - reset password if you forgot your password.

- Managing products and categories of products directly from website:
  - add, update, remove products and categories of products (only an admin);
  - managing the product cart and orders;
  - opportunity of the orders history tracing;
  - possible to leave ratings, reviews and comments to a product.

- Implementation online payment system (Stripe Payment)
- Powerful admin panel for advanced managing


### How to create superuser
- Run `docker-compose up` command, and check with `docker ps`, that 2 services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there;


## Check project functionality

Superuser credentials for test the functionality of this project:
- username: `usermigrate`;
- password: `userpassword`.
