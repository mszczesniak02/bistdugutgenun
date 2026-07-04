import pandas as pd

from pydantic import BaseModel


class PersonCreate(BaseModel):
    first_name: str
    last_name: str
    sex: bool
    email: str


class PersonUpdate(BaseModel):
    first_name: str
    last_name: str
    sex: bool
    email: str


class Person:
    index: int = -1
    first_name: str = "defaut"
    last_name: str = "defaut"
    sex: bool = False  # false - men
    email: str = "default"

    def __init__(self, index, firstname, lastname, sex, email):
        self.index = index
        self.first_name = firstname
        self.last_name = lastname
        self.sex = sex
        self.email = email

    def get(self):
        return self

    def __str__(self):
        return f"{self.index}: {self.first_name} {self.last_name},{self.email}"


class Customers:

    people = []

    def __init__(self):
        raw_data: pd.DataFrame = pd.read_csv("../data/people-1000.csv")
        person_data = raw_data[[
            "Index", "First Name", "Last Name", "Sex", "Email"]]

        for person in person_data.iterrows():
            [id, fname, lname, sex, email] = person[1].values

            self.people.append(Person(
                id, fname, lname, (True if (sex == "Male") else False), email
            ))

    def get_random(self):
        return self.people[67]

    def get(self, id):
        if id < len(self.people):
            return self.people[id]

    def add_person(self, person_data: PersonCreate) -> Person:
        # Generowanie nowego ID na podstawie długości listy
        new_id = len(self.people)
        new_person = Person(
            index=new_id,
            firstname=person_data.first_name,
            lastname=person_data.last_name,
            sex=person_data.sex,
            email=person_data.email
        )
        self.people.append(new_person)
        return new_person

    def update_person(self, id: int, person_data: PersonUpdate) -> Person:
        # Bezpośrednia aktualizacja atrybutów obiektu
        person = self.people[id]
        person.first_name = person_data.first_name
        person.last_name = person_data.last_name
        person.sex = person_data.sex
        person.email = person_data.email
        return person

    def delete_person(self, id: int):
        # Usuwanie odbywa się poprzez usunięcie obiektu z listy.
        # Uwaga: W architekturze opartej na listach zmiana indeksów może
        # zaburzyć spójność danych. Poniżej zaimplementowano logiczne usunięcie (null).
        self.people[id] = None


class Review:
    id: int = -1
    customer_id: int = -1
    product: str = "default"
    rating: int = -1
    desc: str = "default"

    def __init__(self, id, customer, product, rating, desc):
        self.id = id
        self.customer_id = customer
        self.product = product
        self.rating = rating
        self.desc = desc

    def get(self):
        return self

    def __str__(self):
        return f"{self.id}: Rating: {self.rating} Product: {self.product}, Description: {self.desc}"


class Reviews:
    reviews = []

    def __init__(self):
        raw_data = pd.read_csv("../data/customer-reviews-1000.csv")
        review_data = raw_data[[
            "Index", "Review ID", "Product Name", "Rating", "Review Text"]]

        for person in review_data.iterrows():
            [cid, id, product, rating, desc] = person[1].values

            self.reviews.append(Review(
                id, cid, product, rating, desc
            ))

    def get_random(self):
        return self.reviews[67]

    # def get(self, id):
        # return
