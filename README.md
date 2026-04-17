# Flask Diet App (Docker Ready)

A simple diet tracker built with Flask. You can add meals, track daily calories/macros, and delete meals.

## Features

- Add meals with calories, protein, carbs, and fat
- Filter by date
- Daily totals
- SQLite storage
- Docker and Docker Compose support

## Run Locally (without Docker)

1. Create virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate it:

   ```bash
   # Windows (cmd)
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start app:

   ```bash
   python app.py
   ```

5. Open:

   ```
   http://localhost:5000
   ```

## Run With Docker

### Option 1: Docker Compose

```bash
docker compose up --build
```

### Option 2: Docker build/run

```bash
docker build -t flask-diet-app:latest .
docker run -p 5000:5000 -e SECRET_KEY=my-secret flask-diet-app:latest
```

## Publish to Docker Hub

1. Login to Docker Hub:

   ```bash
   docker login
   ```

2. Build image with your Docker Hub username:

   ```bash
   docker build -t YOUR_DOCKERHUB_USERNAME/flask-diet-app:1.0.0 .
   ```

3. Push image:

   ```bash
   docker push YOUR_DOCKERHUB_USERNAME/flask-diet-app:1.0.0
   ```

4. Anyone can run your image:

   ```bash
   docker run -p 5000:5000 -e SECRET_KEY=change-me YOUR_DOCKERHUB_USERNAME/flask-diet-app:1.0.0
   ```

## Notes

- SQLite file is stored in the `instance/` folder.
- For production, set a strong `SECRET_KEY`.
