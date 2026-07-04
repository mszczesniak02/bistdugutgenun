from fastapi import FastAPI, status, HTTPException


from data_generation import *


customers = Customers()
reviews = Reviews()


# print(customers.people[1])

app = FastAPI()


@app.get("/")
async def route_root():
    return {"message": "Welcome to < Bist Du Gut Genun >."}


@app.get("/customers")
async def route_customers():
    return {"customers": customers.people}


@app.get("/customer/{customer_id}")
async def route_customer(customer_id: int):

    # if customer not found or out of index range - throw error 404
    if customer_id < 0 or customer_id >= len(customers.people):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found. Index out of bounds."
        )

    return {customers.people[int(customer_id)]}


@app.put("/customer/{customer_id}", status_code=status.HTTP_200_OK)
async def update_customer(customer_id: int, customer: PersonUpdate):
    if customer_id < 0 or customer_id >= len(customers.people) or customers.people[customer_id] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )

    updated_customer = customers.update_person(customer_id, customer)
    return {"customer": updated_customer}

# Usunięcie zasobu - RFC 9110, sekcja 9.3.5


@app.delete("/customer/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int):
    if customer_id < 0 or customer_id >= len(customers.people) or customers.people[customer_id] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found."
        )

    customers.delete_person(customer_id)
    return  # Status 204 nie zwraca ciała odpowiedzi


@app.get("/reviews")
async def route_reviews():
    return {"reviews": reviews.reviews}


@app.get("/review/{review_id}")
async def route_review(review_id: int):
    # Korekta: użycie len(reviews.reviews)
    if review_id < 0 or review_id >= len(reviews.reviews):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found. Index out of bounds."
        )

    # Serializacja do słownika
    return {"review": reviews.reviews[review_id]}


# Zaktualizowane operacje GET
@app.get("/customer/{customer_id}")
async def route_customer(customer_id: int):
    if customer_id < 0 or customer_id >= len(customers.people) or customers.people[customer_id] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found. Index out of bounds."
        )
    # Zwrócenie atrybutów za pomocą __dict__ pozwala na rzutowanie do JSON
    return {"customer": customers.people[customer_id].__dict__}
