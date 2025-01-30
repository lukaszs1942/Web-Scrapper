from flask import Flask, render_template
from models import db, ScrapedData

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
db.init_app(app)

@app.route('/')
def index():
    data = ScrapedData.query.all()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)