# A Default Restaurant API for your Busniess 


An example of REST API Made by following industry best practices using the power of Django Rest Framework

### Scope

A fully functioning API project for the Little Lemon restaurant so that the client application developers can use the APIs to develop web and mobile applications. People with different roles will be able to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders and finally deliver the orders. 


# Table of Contents

1. [Installing](#installing)
   - [Clone the project](#clone-the-project)
   - [Install dependencies & activate virtualenv](#install-dependencies--activate-virtualenv)
   - [Apply migrations (Optional)](#apply-migrations-optional)
   - [Running](#running)
     - [A development server](#a-development-server)

2. [PROJECT DESCRIPTION](#project-description)
   - [1. User Groups](#1-user-groups)
   - [2. Error Checks and proper status codes](#2-error-checks-and-proper-status-codes)
   - [3. API ENDPOINTS](#3-api-endpoints)
     - [User registration and token generation endpoints](#user-registration-and-token-generation-endpoints)
     - [Menu items endpoints](#menu-items-endpoints)
     - [User group management endpoints](#user-group-management-endpoints)
     - [Cart management endpoints](#cart-management-endpoints)
     - [Order Management endpoints](#order-management-endpoints)
   - [4. Filtering, Pagination, and Sorting](#4-filtering-pagination-and-sorting)
   - [5. Throttling](#5-throttling)
   - [Learned Topics](#learned-topics)


<hr>




## Installing

### Clone the project

```bash
git clone https://github.com/nabeelahmedjh/littlelemon-REST-API.git
```

### Install dependencies & activate virtualenv

#### Running the virtualenv using pipenv

```bash
pipenv shell 

```

#### Install dependencies

```bash
pipenv install 
```
this is install all the dependencies mentioned in the pipfile

### Apply migrations (Optional)

```bash
python source/manage.py migrate
```

### Running

#### A development server

Just run this command:

```bash
python source/manage.py runserver
```

# PROJECT DESCRIPTION

### 1.  User Groups
The Project consists of three user groups:

- Manager

- Delivery crew

- Normal users - Customers

### 2. Error Checks and proper status codes
The project display error messages with appropriate HTTP status codes for specific errors. These include when someone requests a non-existing item, makes unauthorized API requests, or sends invalid data in a POST, PUT or PATCH request. Here is a full list.

| HTTP Status Code | Reason                                               |
|------------------|------------------------------------------------------|
| 200              | Ok                                                   |
| 201              | Created                                              |
| 400              | Bad request                                          |
| 401              | Unauthorized (Authentication failed)                 |
| 403              | Forbidden (Authorization failed for current token)   |
| 404              | Not found (Non-existing resource requested)          |


### 3. API ENDPOINTS

Here are all the API routes for this project grouped into several categories.

 - #### **User registeration and token generation endpoints**

| Endpoint              | Role                         | Method | Purpose                                                                                     |
|-----------------------|------------------------------|--------|---------------------------------------------------------------------------------------------|
| /api/users            | No role required             | POST   | Creates a new user with name, email, and password                                          |
| /api/users/users/me/  | Anyone with a valid user token | GET    | Displays only the current user                                                              |
| /token/login/         | Anyone with a valid username and password | POST   | Generates access tokens that can be used in other API calls in this project    |

<br>

- #### **Menu items endpoints**

| Endpoint                  | Role                             | Method            | Purpose                                           |
|---------------------------|----------------------------------|-------------------|---------------------------------------------------|
| /api/menu-items           | Customer, delivery crew          | GET               | Lists all menu items. Return a 200 – Ok HTTP status code |
| /api/menu-items           | Customer, delivery crew          | POST, PUT, PATCH, DELETE | Denies access and returns 403 – Unauthorized HTTP status code |
| /api/menu-items/{menuItem}| Customer, delivery crew          | GET               | Lists single menu item                            |
| /api/menu-items/{menuItem}| Customer, delivery crew          | POST, PUT, PATCH, DELETE | Returns 403 - Unauthorized                        |
| /api/menu-items           | Manager                          | GET               | Lists all menu items                              |
| /api/menu-items           | Manager                          | POST              | Creates a new menu item and returns 201 - Created |
| /api/menu-items/{menuItem}| Manager                          | GET               | Lists single menu item                            |
| /api/menu-items/{menuItem}| Manager                          | PUT, PATCH        | Updates single menu item                          |
| /api/menu-items/{menuItem}| Manager                          | DELETE            | Deletes menu item                                 |

<br>

- #### **User group management endpoints**
| Endpoint                             | Role      | Method | Purpose                                                                                    |
|--------------------------------------|-----------|--------|--------------------------------------------------------------------------------------------|
| /api/groups/manager/users            | Manager   | GET    | Returns all managers                                                                       |
| /api/groups/manager/users            | Manager   | POST   | Assigns the user in the payload to the manager group and returns 201-Created             |
| /api/groups/manager/users/{userId}   | Manager   | DELETE | Removes this particular user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found |
| /api/groups/delivery-crew/users      | Manager   | GET    | Returns all delivery crew                                                                  |
| /api/groups/delivery-crew/users      | Manager   | POST   | Assigns the user in the payload to the delivery crew group and returns 201-Created HTTP    |
| /api/groups/delivery-crew/users/{userId}| Manager | DELETE | Removes this user from the manager group and returns 200 – Success if everything is okay. If the user is not found, returns 404 – Not found |

<br>

- #### **Cart management endpoints**

| Endpoint                         | Role     | Method | Purpose                                                                             |
|----------------------------------|----------|--------|-------------------------------------------------------------------------------------|
| /api/cart/menu-items             | Customer | GET    | Returns current items in the cart for the current user token                       |
| /api/cart/menu-items             | Customer | POST   | Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items |
| /api/cart/menu-items             | Customer | DELETE | Deletes all menu items created by the current user token                            |

<br>

- #### **Order Management endpoints**
| Endpoint                          | Role          | Method   | Purpose                                                                                               |
|-----------------------------------|---------------|----------|-------------------------------------------------------------------------------------------------------|
| /api/orders                       | Customer      | GET      | Returns all orders with order items created by this user                                             |
| /api/orders                       | Customer      | POST     | Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user. |
| /api/orders/{orderId}             | Customer      | GET      | Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code. |
| /api/orders                       | Manager       | GET      | Returns all orders with order items by all users                                                      |
| /api/orders/{orderId}             | Customer      | PUT, PATCH | Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1. If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery. If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered. |
| /api/orders/{orderId}             | Manager       | DELETE   | Deletes this order                                                                                   |
| /api/orders                       | Delivery crew | GET      | Returns all orders with order items assigned to the delivery crew                                    |
| /api/orders/{orderId}             | Delivery crew | PATCH    | A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order. |

<br>

### 4. Filtering, Pagination and sorting

Implemented proper filtering, pagination and sorting capabilities for /api/menu-items and /api/orders endpoints

### 5. Throttling

Finally, Added some throttling for the authenticated users and anonymous or unauthenticated users



## Learned Topics

- Django Authenication
- Making API's
- Django Rest Framework
- Error Checking
- Djoser
- REST best practices
- filtering, pagination, searching
- Rate limiting or Throttling

