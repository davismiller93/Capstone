import subprocess
import time
import os
import capstone_ingest
from pathlib import Path
from scraper import RealtorScraper

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    return process

def create_db():
    # Run the schema file to create the database tables
    os.system("capstone_schema.py")

def get_scrape_data():
    # Run scraper and pull new data for ingest
    r = RealtorScraper(page_numbers=10)
    df = r.create_dataframe()
    df.to_csv('houses.csv', index=False)

def populate_db():
    ingest = capstone_ingest()
    # Run the insert file to populate the database tables
    file_path = 'houses.csv'
    ingest.ingest_csv(file_path)

if __name__ == '__main__':
    create_db()

    flask_process = run_command("python app.py")
    time.sleep(3)  # Wait for the Flask API to start
    streamlit_process = run_command("streamlit run streamlit.py")

    try:
        while True:
            get_scrape_data()
            populate_db()
            time.sleep(3600)  # Run the scraper and ingest every hour

    except KeyboardInterrupt:
        flask_process.terminate()
        streamlit_process.terminate()