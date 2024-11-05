from flask import Flask, request, jsonify
from celery_config import Celery
from models import PDFMetadata, db
from celery_config import make_celery

app = Flask(__name__)
# Set up the database URL for SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Celery Configuration
app.config['broker_url'] = 'redis://127.0.0.1:6379'
app.config['result_backend'] = 'redis://127.0.0.1:6379'
app.config['broker_connection_retry_on_startup'] = True

# Initialize the database with the app
db.init_app(app)

celery = make_celery(app)
import celery_task
# celery.conf.update(app.config)

# Function to make the Celery instance

with app.app_context():
    db.create_all()

# Route to add a new user
@app.route('/upload', methods=['POST'])
def upload_pdf():
    data = request.json
    name=data['name']
    if name.endswith('.pdf'):
        # Save metadata to the database
        pdf_metadata = PDFMetadata(filename=name)
        db.session.add(pdf_metadata)
        db.session.commit()

        celery_task.classify_pdf_task.delay(pdf_metadata.id)

        return jsonify({"message": "PDF uploaded successfully!"}), 201


@app.route('/status/<int:pdf_id>', methods=['GET'])
def get_status(pdf_id):
    pdf_metadata = PDFMetadata.query.get(pdf_id)
    if not pdf_metadata:
        return jsonify({"message": "PDF not found"}), 404

    return jsonify({
        "filename": pdf_metadata.filename,
        "status": pdf_metadata.status,
        "category": pdf_metadata.category,
        "upload_time": pdf_metadata.upload_time,
        "result_time": pdf_metadata.result_time
    })
@app.route("/")
def home():
    return "My flask app"


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)