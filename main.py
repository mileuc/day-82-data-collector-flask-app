from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from send_email import send_email
from dotenv import load_dotenv
import os

load_dotenv("./.env")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height = height


db.create_all()


@app.route("/")  # mapping this url
def home():  # rendering index.html - when the url above is visited, execute this function
    is_invalid = False
    return render_template("index.html", invalid_email=is_invalid)


@app.route("/success", methods=["POST"])
def success():
    if request.method == "POST":
        email = request.form["email_name"]
        height = request.form["height_cm"]
        if db.session.query(Data).filter(Data.email == email).count() == 0:
            new_data = Data(email, height)  # our database model. instance of Data class
            db.session.add(new_data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height)).scalar()
            rounded_average_height = round(average_height, 1)
            count = db.session.query(Data.height).count()
            send_email(email, height, rounded_average_height, count)
            return render_template("success.html")
        else:
            is_invalid = True
            return render_template("index.html", invalid_email=is_invalid)


if __name__ == "__main__":  # ie. if the script is being executed and not imported...
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug = True)