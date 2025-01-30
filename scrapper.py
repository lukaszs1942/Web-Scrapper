import requests
from bs4 import BeautifulSoup
from models import db, ScrapedData
from app import app
from datetime import datetime
import difflib

def scrape_data():
    response = requests.get('https://example.com')
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text()

    with app.app_context():
        previous_data = ScrapedData.query.order_by(ScrapedData.timestamp.desc()).first()
        diff = None
        if previous_data:
            diff = '\n'.join(difflib.unified_diff(previous_data.content.splitlines(), content.splitlines()))

        new_data = ScrapedData(content=content, timestamp=datetime.now(), diff=diff)
        db.session.add(new_data)
        db.session.commit()

if __name__ == '__main__':
    scrape_data()