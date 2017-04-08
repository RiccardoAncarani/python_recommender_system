# Python Recommender System
## A small (and still buggy) framework for product recommendations
### Still in dev.

# Theory
This recommender system uses a technique called **User Based Collaborative filtering**.

A user based collaborative filter is a kind of filter that recommends products to a user that users like him bought. 

Mathematically speaking, in this model each user is a N-dimensional vector, where N is the number of products in the dataset, the similarity between two users is measured via cosine, that ranges from -1 to +1.

- +1 means that the two users have the same purchcase history
- -1 means that the two users have the opposite purchcase history

# Implementation
This framework is built with Flask, and uses SQLAlchemy for ORM

# Endpoints
## /api/new/customer/name
Insert a new customer into the DB

```bash
curl http://127.0.0.1:5000/api/new/customer/riccardo
{ "status" : "insert ok" }

```

## /api/new/item/name
Insert a new item into the DB

```bash
curl http://127.0.0.1:5000/api/new/item/hammer
{ "status" : "insert ok" }
```

## /api/new/purchcase/customer/item
Insert a new event, customer bought item

```bash
curl http://127.0.0.1:5000/api/new/purchcase/riccardo/hammer
{ "status" : "insert ok" }
```

## /api/predict/customer
Get a prediction for the user named customer, return the vector of the nearest user with similar purchcases, this is still dev. but in the final version this API will return the names of the items that are recommended for customer.

Now it just consider the nearest user, but the assumption that the nearest user necessarily has *more* items than customer is just wrong, I'll implement it ASAP.

```bash
curl http://127.0.0.1:5000/api/predict/riccardo
{ "response" : "apparently meaningless vector" }
```

## /api/update_matrix
This API update the global matrix that holds all the user vectors.

His aim is to provide a manual way to keeping the matrix updated just when is needed, otherwise the matrix would be rebuilt every insertion into the DB.

```bash
curl http://127.0.0.1:5000/api/update_matrix
{ "response" : "Matrix updated" }
```


If you look at the source, there are more endpoints but they are just for debugging purpose.

# Defining how the matrix is sensitive to updates
You'll have to keep the global matrix updated, otherwise this system is pretty useless.

I choose to have a buffer of insert operation before the matrix is rebuilt, you have the freedom to edit this parameter in order to meet your needs:

```python
...
buffer = 2 # This is the number of insert events before an update
events = 0 # This is the global counter of insert events
...
```
