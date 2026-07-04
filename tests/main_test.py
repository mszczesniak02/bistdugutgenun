from fastapi.testclient import TestClient
from backend.src.main import app


client = TestClient(app)


def test_read_root():
    # Weryfikacja kodu statusu HTTP i struktury JSON dla ścieżki głównej
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to < Bist Du Gut Genun >."}


def test_read_customer_valid():
    response = client.get("/customer/0")
    assert response.status_code == 200

    data = response.json()

    # Sprawdzenie, czy odpowiedź jest listą
    assert isinstance(data, list)

    # Sprawdzenie, czy lista nie jest pusta i posiada poprawne pola
    assert len(data) > 0
    assert "first_name" in data[0]
    assert data[0]["index"] == 1  # lub odpowiednia logika dla Twojego indeksu


def test_read_customer_invalid_out_of_bounds():
    # Testowanie obsługi błędu - RFC 9110 status 404
    response = client.get("/customer/99999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found. Index out of bounds."}


def test_read_customer_invalid_type():
    # Testowanie obsługi błędu walidacji typu - RFC 4918 status 422
    response = client.get("/customer/invalid_string")
    assert response.status_code == 422
