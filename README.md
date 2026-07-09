# Google Cloud Healthcare Analytics Pipeline

An end-to-end healthcare analytics pipeline built with Python, Google Cloud Platform, BigQuery, and Looker Studio using public CMS (Centers for Medicare & Medicaid Services) healthcare data.

This project demonstrates how to:

- Extract healthcare data from the CMS API
- Archive raw JSON data in Google Cloud Storage
- Transform raw API data into analytics-ready tables using Pandas
- Load transformed data into BigQuery
- Build interactive dashboards in Looker Studio
- Apply software engineering and data engineering best practices, including modular code, environment configuration, and Git version control

## Technology Stack

- Python
- Google Cloud Storage
- BigQuery
- Pandas
- REST APIs
- Looker Studio
- Git & GitHub

## Project Architecture

```text
                CMS Healthcare API
                        │
                        ▼
              Python Extraction Layer
                        │
                        ▼
         Google Cloud Storage (Raw JSON)
                        │
                        ▼
          Pandas Transformation Layer
                        │
                        ▼
             Google BigQuery Dataset
                        │
                        ▼
              Looker Studio Dashboard
```
## Repository Structure

```text
google-cloud-healthcare-analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dashboards/
│
├── docs/
│
├── sql/
│
├── src/
│   ├── extract/
│   ├── load/
│   ├── transform/
│   └── utils/
│
├── tests/
│
├── .env.example
├── requirements.txt
└── README.md
```

## What I Learned

Building this project helped me strengthen my understanding of modern cloud-based data engineering and analytics workflows. Throughout the project I gained experience with:

- Working with REST APIs to extract public healthcare data
- Designing an end-to-end ETL pipeline
- Organizing Python projects using reusable modules
- Managing configuration with environment variables
- Storing raw data in Google Cloud Storage
- Transforming JSON data into analytics-ready tables using Pandas
- Loading data into BigQuery for analytical reporting
- Using Git and GitHub to manage incremental development
- Building cloud-native analytics solutions following industry best practices

