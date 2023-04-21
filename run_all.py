import subprocess
import time
import os
import capstone_ingest
from pathlib import Path
from scraper import RealtorScraper
from sqlalchemy import create_engine
import capstone_schema

db_connection_string = "postgresql://postgres: @localhost/capstone"

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    return process

def get_scrape_data():
    # Run scraper and pull new data for ingest
    r = RealtorScraper(page_numbers=10)
    df = r.create_dataframe()
    df.to_csv('houses.csv', index=False)

def create_and_populate_db():
    ingest = capstone_ingest.DataIngestion(db_connection_string)
    # Run the insert file to populate the database tables
    file_path = 'houses.csv'
    ingest.ingest_csv(file_path)

if __name__ == '__main__':
    
    db_connection_string = "postgresql://postgres: @localhost/capstone"
    engine = create_engine(db_connection_string)
    capstone_schema.create_schema(engine)

    flask_process = run_command("python app.py")
    time.sleep(3)  # Wait for the Flask API to start
    streamlit_process = run_command("streamlit run streamlit.py")

    try:
        while True:
            get_scrape_data()
            create_and_populate_db()
            time.sleep(3600)  # Run the scraper and ingest every hour

    except KeyboardInterrupt:
        flask_process.terminate()
        streamlit_process.terminate()