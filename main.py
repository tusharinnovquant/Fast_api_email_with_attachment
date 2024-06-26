from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal, UserDB
import csv
from emailing import send_email_async

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    email: str

@app.get("/users/")
async def read_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()

    with open("users.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["id", "name", "email"])
        for user in users:
            writer.writerow([user.id, user.name, user.email])

    await send_email_async(
        subject="User data",
        message="This is the Data.",
        from_addr="vikas@innovquant.com",
        to_addr="tushar.innovquant@gmail.com",
        csv_file="users.csv",
    )

    return {"message": "Data is retrieved and email sent"}