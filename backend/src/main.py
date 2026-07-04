from fastapi import FastAPI, status, HTTPException


from data_generation import Person, Customers, Review, Reviews


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


@app.get("/customer={customer_id}", status_code=status.HTTP_207_MULTI_STATUS)
async def route_customer(customer_id):
    # if customer not found or out of index range - throw error 404
    if int(customer_id) > len(customers.people):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return {customers.people[int(customer_id)]}
