# pdf_diff_checker
# Assignment

Notes: 

we have two endpoints: 
1. /upload to upload the files
2. /status/<int:pdf_id> get status

I have used celery to manage async task through redis message borker

Assumptions:
1. ML model(Can use Amazon Textract to Extract text from PDFs.
	and Amazon Comprehend  to Use the extracted text to classify the document into predefined categories like “Warranty,” “Transactions,” and “Troubleshooting.”)
2. File upload(can be achieved through s3) but for now I have taken only file name as input

Process:

Upload will take entry into PDFMetadata and submit the celery task
than celery task will take that id and call ML model and then update the status as process completed.

Pending tasks:

1. Dockerization for easy up and running of the project.
2. Documentation of the methods and description of the complex logic.
3. File checking for viruses
4. Validation of the size of the files etc.


Tools Used: 

1. Celery for async processing
2. Redis for message broker
3. Flask as API development
