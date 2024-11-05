from classify import Classify
from models import PDFMetadata, db
from datetime import datetime
from celery_config import make_celery
from app import celery

@celery.task
def classify_pdf_task(pdf_id):
    category = Classify.classify()            # Classify the PDF

    # Update database with classification result
    pdf_metadata = PDFMetadata.query.get(pdf_id)
    pdf_metadata.category = category
    pdf_metadata.status = "Completed"
    pdf_metadata.result_time = datetime.utcnow()

    db.session.commit()
    return category