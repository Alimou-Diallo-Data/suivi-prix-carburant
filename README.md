# Suivi des prix du pétrole et du carburant

Pipeline de données et tableau de bord pour suivre les prix de l'énergie. Un ETL collecte les cours de référence et les prix à la pompe, les stocke dans PostgreSQL, et un tableau de bord Dash les affiche. Airflow orchestre le pipeline et Docker Compose lance l'ensemble.

## Fonctionnalités

- Cours de référence récupérés avec yfinance : Brent, WTI, essence RBOB, mazout et gaz naturel.
- Prix moyens de l'essence par État américain, extraits du site de l'AAA.
- Prix dans d'autres pays à partir d'un fichier CSV saisi à la main (`world_fuel_prices.csv`).
- Historique dans PostgreSQL et vues SQL d'analyse (`sql/`).
- DAG Airflow qui enchaîne extraction, transformation et chargement (`dags/petrol_pipeline.py`).
- Tableau de bord Dash : cartes, séries temporelles et indicateurs.

## Structure

```text
app/        clients API, ETL, transformations, tableau de bord
dags/       DAG Airflow
sql/        création des tables et vues d'analyse
tests/      tests unitaires
docker-compose.yml, Dockerfile, run.py
```

## Lancement avec Docker

```bash
cp .env.example .env        # Windows : copy .env.example .env
docker compose up --build
```

- Tableau de bord : http://127.0.0.1:8050
- Airflow : http://127.0.0.1:8080

## Sans Docker

```bash
pip install -r requirements.txt
python run.py init-db
python run.py etl
python run.py dashboard
```

## Tests

```bash
pip install pytest
pytest tests/
```

## Pistes d'amélioration

- Convertir les prix dans une même devise avec une API de change.
- Ajouter un cache Redis.
- Compléter les tests unitaires.
- Déployer le tableau de bord (Render, Railway ou Fly.io).

---

Alimou Diallo · [LinkedIn](https://www.linkedin.com/in/alimou-diallo-883022bb)
