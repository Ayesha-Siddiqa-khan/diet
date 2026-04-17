import os
import sqlite3
from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret")

DB_PATH = os.path.join(app.instance_path, "diet.db")
os.makedirs(app.instance_path, exist_ok=True)


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_name TEXT NOT NULL,
                calories INTEGER NOT NULL CHECK (calories >= 0),
                protein INTEGER NOT NULL CHECK (protein >= 0),
                carbs INTEGER NOT NULL CHECK (carbs >= 0),
                fat INTEGER NOT NULL CHECK (fat >= 0),
                meal_date TEXT NOT NULL
            )
            """
        )


def parse_non_negative_int(value: str, field_name: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a number.") from exc

    if parsed < 0:
        raise ValueError(f"{field_name} must be 0 or higher.")

    return parsed


@app.route("/", methods=["GET"])
def index():
    selected_day = request.args.get("day", date.today().isoformat())

    with get_db_connection() as conn:
        meals = conn.execute(
            """
            SELECT id, meal_name, calories, protein, carbs, fat, meal_date
            FROM meals
            WHERE meal_date = ?
            ORDER BY id DESC
            """,
            (selected_day,),
        ).fetchall()

    totals = {
        "calories": sum(row["calories"] for row in meals),
        "protein": sum(row["protein"] for row in meals),
        "carbs": sum(row["carbs"] for row in meals),
        "fat": sum(row["fat"] for row in meals),
    }

    return render_template("index.html", meals=meals, totals=totals, selected_day=selected_day)


@app.route("/add", methods=["POST"])
def add_meal():
    selected_day = request.form.get("meal_date", date.today().isoformat())
    meal_name = (request.form.get("meal_name") or "").strip()

    if not meal_name:
        flash("Meal name is required.", "error")
        return redirect(url_for("index", day=selected_day))

    try:
        calories = parse_non_negative_int(request.form.get("calories", "0"), "Calories")
        protein = parse_non_negative_int(request.form.get("protein", "0"), "Protein")
        carbs = parse_non_negative_int(request.form.get("carbs", "0"), "Carbs")
        fat = parse_non_negative_int(request.form.get("fat", "0"), "Fat")
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("index", day=selected_day))

    with get_db_connection() as conn:
        conn.execute(
            """
            INSERT INTO meals (meal_name, calories, protein, carbs, fat, meal_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (meal_name, calories, protein, carbs, fat, selected_day),
        )

    flash("Meal added.", "success")
    return redirect(url_for("index", day=selected_day))


@app.route("/delete/<int:meal_id>", methods=["POST"])
def delete_meal(meal_id: int):
    selected_day = request.form.get("selected_day", date.today().isoformat())

    with get_db_connection() as conn:
        conn.execute("DELETE FROM meals WHERE id = ?", (meal_id,))

    flash("Meal removed.", "success")
    return redirect(url_for("index", day=selected_day))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
