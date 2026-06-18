# AI Ticket Analysis Automation

## Overview

An end-to-end AI-powered customer support ticket analysis system that automatically collects tickets from Google Forms, classifies them using Groq LLM, stores results in MySQL, generates Power BI insights, and sends automated email reports using n8n scheduling.

## Features

* Automated Google Forms → Google Sheets ingestion
* AI-powered ticket classification using Groq
* Incremental processing of new tickets only
* MySQL database integration
* Automated email reporting
* Flask webhook integration
* n8n workflow scheduling
* Power BI dashboard visualization

## Architecture

Google Form
→ Google Sheet
→ n8n Scheduler
→ Flask Webhook
→ Python Pipeline
→ Groq Classification
→ MySQL
→ Power BI Dashboard
→ Email Reports

## Tech Stack

* Python
* Flask
* Groq API
* MySQL
* Pandas
* SQLAlchemy
* Power BI
* n8n
* Gmail SMTP

## Project Structure

ticket-analysis-project/

├── src/

├── output/

├── n8n_workflow.json

├── requirements.txt

├── README.md

└── .env

## Setup

1. Clone repository
2. Install requirements
3. Configure .env
4. Run webhook server
5. Start n8n workflow

## Future Enhancements

* Power BI API refresh
* PDF report attachments
* Slack/Teams notifications
* Cloud deployment


**Note:** The project includes two classification modes. `classify_all.py` processes tickets individually, while `classify_batch.py` processes up to 20 tickets per batch to improve throughput and reduce API calls. Batch processing is recommended for larger datasets.



<img width="1536" height="1024" alt="workflow" src="https://github.com/user-attachments/assets/f5d977cf-a6f6-418f-8179-6df70802ff2b" />
<img width="935" height="515" alt="gmail_report" src="https://github.com/user-attachments/assets/716d3110-0c36-4086-ad65-244175fd1ff0" />
<img width="643" height="358" alt="dashboard" src="https://github.com/user-attachments/assets/cac65b54-8a9e-41cf-8356-b29f90a30c36" />
<img width="857" height="477" alt="n8n_workflow" src="https://github.com/user-attachments/assets/235f6468-3ef4-445d-8e84-084b1c13cbd6" />


