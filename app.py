import logging
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

class ScrapedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    diff = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"ScrapedData('{self.content}', '{self.timestamp}')"

@app.route('/')
def index():
    data = ScrapedData.query.all()
    return render_template('index.html', data=data)

@app.route('/history')
def history():
    data = ScrapedData.query.all()
    return render_template('history.html', data=data)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    app.logger.debug(f"Received URL to scrape: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()[:200]  # Extract first 200 characters of text content
        app.logger.debug(f"Scraped content: {content}")
        
        # Calculate diff if previous data exists
        previous_data = ScrapedData.query.order_by(ScrapedData.timestamp.desc()).first()
        diff = None
        if previous_data:
            diff = '\n'.join([line for line in content.splitlines() if line not in previous_data.content.splitlines()])
        
        new_data = ScrapedData(content=content, timestamp=datetime.utcnow(), diff=diff)
        db.session.add(new_data)
        db.session.commit()
        app.logger.debug("Scraped data saved to database")
    except requests.RequestException as e:
        app.logger.error(f"Error scraping {url}: {e}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables
    app.run(debug=True)