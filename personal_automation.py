import os
import shutil
import requests
import csv
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv


# ── LOAD ENVIRONMENT VARIABLES ───────────────────

load_dotenv()


# ── CONFIG ────────────────────────────────────────

TARGET_FOLDER = "test_folder"

FOLDERS = {
    ".pdf": "Documents",
    ".docx": "Documents",
    ".jpg": "Images",
    ".png": "Images",
    ".mp4": "Videos",
    ".mp3": "Music",
}

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
WEATHER_KEY = os.getenv("WEATHER_KEY")

LOG_FILE = "weather_log.csv"


# ── FILE ORGANIZER ────────────────────────────────

def organize_files(folder):
    """Sort files into folders by extension."""

    try:
        moved = 0

        for filename in os.listdir(folder):

            file_path = os.path.join(folder, filename)

            if not os.path.isfile(file_path):
                continue

            extension = os.path.splitext(filename)[1].lower()

            destination_folder = FOLDERS.get(
                extension,
                "Others"
            )

            destination_path = os.path.join(
                folder,
                destination_folder
            )

            os.makedirs(
                destination_path,
                exist_ok=True
            )

            shutil.move(
                file_path,
                os.path.join(
                    destination_path,
                    filename
                )
            )

            moved += 1

        return f"Moved {moved} files"

    except Exception as e:
        return f"Error organizing files: {e}"


# ── EMAIL SENDER ──────────────────────────────────

def send_email(to, subject, body):
    """Send an email using Gmail SMTP."""

    try:

        message = EmailMessage()

        message["From"] = EMAIL
        message["To"] = to
        message["Subject"] = subject

        message.set_content(body)

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                EMAIL,
                APP_PASSWORD
            )

            server.send_message(message)

        return "Email sent successfully"

    except Exception as e:
        return f"Email error: {e}"


# ── WEATHER LOGGER ────────────────────────────────

def log_weather(city):
    """Fetch current weather and save it to a CSV file."""

    try:

        url = (
            "https://api.openweathermap.org/"
            "data/2.5/weather"
        )

        params = {
            "q": city,
            "appid": WEATHER_KEY,
            "units": "metric"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        temperature = data["main"]["temp"]

        description = data["weather"][0]["description"]

        file_exists = os.path.exists(LOG_FILE)

        with open(
            LOG_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            if not file_exists:

                writer.writerow([
                    "date",
                    "city",
                    "temperature",
                    "description"
                ])

            writer.writerow([
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                city,
                temperature,
                description
            ])

        return (
            f"Weather logged: {city}, "
            f"{temperature}°C, "
            f"{description}"
        )

    except Exception as e:
        return f"Weather error: {e}"


# ── MAIN MENU ─────────────────────────────────────

def main():

    while True:

        print("\n=== MY AUTOMATION SUITE ===")

        print("1. Organize files")
        print("2. Weather log")
        print("3. Email me a status")
        print("4. Quit")

        choice = input("Choose: ")

        if choice == "1":

            result = organize_files(
                TARGET_FOLDER
            )

            print(result)

        elif choice == "2":

            city = input(
                "Enter city: "
            )

            result = log_weather(city)

            print(result)

        elif choice == "3":

            result = send_email(
                EMAIL,
                "Automation Suite Status",
                "Hello from my automation suite."
            )

            print(result)

        elif choice == "4":

            print("Bye!")

            break

        else:

            print(
                "Invalid choice. "
                "Please choose 1-4."
            )


# ── RUN PROGRAM ───────────────────────────────────

if __name__ == "__main__":
    main()