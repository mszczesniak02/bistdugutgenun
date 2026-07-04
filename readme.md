# Bist Du Gut Genun

## Lokalne testy

Z katalogu głównego repozytorium:

```bash
./bin/python -m pytest -q tests/main_test.py
```

## GitHub Actions

Workflow jest w [.github/workflows/ci.yml](/home/krzeslaav/Projects/bistdugutgenun/.github/workflows/ci.yml). Działa automatycznie na `push` do `main`, na `pull_request` i ręcznie z zakładki `Actions` przez `workflow_dispatch`.

Żeby go używać:

1. Wypchnij repozytorium na GitHub.
2. Wejdź w zakładkę `Actions` i upewnij się, że workflow `CI` jest włączony.
3. Zrób `push` albo otwórz `pull request` i sprawdź wynik testów oraz builda obrazu Docker.

Workflow robi dwie rzeczy:

1. uruchamia `pytest -q tests/main_test.py`,
2. buduje obraz z `backend/dockerfile`.

## Docker

Obraz buduje się z katalogu `backend/` jako kontekstu:

```bash
docker build -t bistdugutgenun-api:latest -f backend/dockerfile backend
docker run --rm -p 8000:8000 bistdugutgenun-api:latest
```

## Minikube

1. Włącz klaster:

```bash
minikube start
```

2. Załaduj obraz do klastra Minikube:

```bash
docker build -t bistdugutgenun-api:latest -f backend/dockerfile backend
minikube image load bistdugutgenun-api:latest
```

3. Zastosuj manifesty:

```bash
kubectl apply -f k8s/deployment.yaml
```

4. Sprawdź usługę:

```bash
minikube service bistdugutgenun-api --url
```

Jeśli pod nie startuje, sprawdź najpierw:

```bash
kubectl get pods
kubectl describe pod -l app=bistdugutgenun-api
```

API będzie dostępne na porcie `8000` wewnątrz klastra, a przez `Service` typu `NodePort` na porcie `30080`.