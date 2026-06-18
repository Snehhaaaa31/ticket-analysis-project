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
