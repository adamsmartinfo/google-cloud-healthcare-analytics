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
                      Hospital General Information Pipeline
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
     Extract                     Transform                    Load
         │                           │                           │
         ▼                           ▼                           ▼
 Google Cloud Storage         Pandas DataFrame             Google BigQuery
    (Raw JSON)               (Analytics Ready)             (Data Warehouse)
                                                                     │
                                                                     ▼
                                                            Looker Studio
                                                         Executive Dashboard
```

### Shared Components

All dataset pipelines use the shared components in `src/common/`:

* **cms_client.py** – Communicates with the CMS REST API
* **storage.py** – Uploads raw data to Google Cloud Storage
* **bigquery.py** – Loads transformed data into BigQuery
* **config.py** – Reads project configuration from environment variables

This architecture allows additional CMS datasets to be added as independent pipelines while reusing the same cloud infrastructure and shared utilities.


## Repository Structure

```text
google-cloud-healthcare-analytics/
│
├── data/
│   ├── raw/                  # Raw CMS API responses
│   └── processed/            # Future processed data exports
│
├── dashboards/               # Looker Studio documentation
│
├── docs/                     # Project documentation
│
├── sql/                      # BigQuery SQL scripts
│
├── src/
│   ├── common/               # Shared utilities
│   │   ├── bigquery.py
│   │   ├── cms_client.py
│   │   ├── config.py
│   │   └── storage.py
│   │
│   ├── pipelines/
│   │   └── hospital_general_information/
│   │       ├── extract.py
│   │       ├── transform.py
│   │       ├── load.py
│   │       └── pipeline.py
│   │
│   └── main.py               # Future orchestration entry point
│
├── tests/                    # Automated tests (planned)
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

## Project Roadmap

This project is being developed as a scalable healthcare analytics platform using publicly available CMS datasets and Google Cloud Platform.

### Phase 1 — Foundation ✅

* Build Google Cloud project
* Extract CMS Hospital General Information data
* Archive raw JSON in Google Cloud Storage
* Transform data using Pandas
* Load data into BigQuery
* Build initial Looker Studio dashboard

### Phase 2 — Pipeline Architecture ✅

* Refactor into reusable shared components
* Create dataset-specific pipeline architecture
* Support full dataset ingestion with API pagination
* Improve project documentation

### Phase 3 — Healthcare Analytics

Planned additions include:

* Hospital Readmissions
* Patient Experience (HCAHPS)
* Mortality Measures
* Timely & Effective Care
* Healthcare-Associated Infections
* Emergency Department Throughput

Each dataset will be implemented as an independent pipeline while reusing the shared cloud infrastructure.

### Phase 4 — Executive Reporting

Planned dashboards include:

* Executive Healthcare Overview
* Hospital Quality Dashboard
* Patient Experience Dashboard
* Operational Performance Dashboard
* Geographic Analysis Dashboard

### Phase 5 — Production Engineering

Future enhancements include:

* Automated daily ingestion
* Cloud Scheduler orchestration
* Incremental data loading
* Data quality validation
* Automated testing with pytest
* CI/CD with GitHub Actions
* Monitoring and logging
