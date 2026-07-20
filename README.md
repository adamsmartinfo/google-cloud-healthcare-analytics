# Google Cloud Healthcare Analytics Platform

An end-to-end Analytics Engineering platform that automates the ingestion, standardization, warehousing, and visualization of publicly available CMS (Centers for Medicare & Medicaid Services) hospital performance data using Google Cloud Platform.

Built using Python, Google Cloud Storage, BigQuery, Cloud Functions Gen2, Cloud Scheduler, and Looker Studio, this project demonstrates modern cloud data engineering practices through a fully automated Medallion (Bronze → Silver → Gold) architecture that transforms fragmented healthcare datasets into executive-ready business intelligence.

---

# Executive Summary

Healthcare organizations, researchers, and analysts rely on CMS quality reporting data to evaluate hospital performance, patient outcomes, safety measures, and reimbursement programs. While these datasets are publicly available, they are distributed across numerous independent APIs with inconsistent schemas, varying data types, and separate business definitions, making comprehensive analysis both time-consuming and technically challenging.

This project solves that problem by building a production-style cloud analytics platform that automatically extracts, validates, standardizes, warehouses, and models CMS hospital quality data into a centralized analytics environment optimized for executive reporting and business intelligence.

The platform currently integrates nine independent CMS datasets, stores raw source data in Google Cloud Storage, builds a dimensional data warehouse in BigQuery using a Medallion architecture, and delivers executive dashboards through Looker Studio. The entire platform executes automatically each month using Cloud Scheduler and Cloud Functions Gen2 without requiring any local infrastructure.

---

# Business Problem

The Centers for Medicare & Medicaid Services publishes thousands of hospital quality metrics covering:

- Hospital Quality Ratings
- Patient Experience (HCAHPS)
- Hospital Readmissions
- Mortality Measures
- Timely & Effective Care
- Healthcare-Associated Infections
- Outpatient Imaging Efficiency
- Value-Based Purchasing
- Hospital-Acquired Condition Reduction Program

Although individually valuable, these datasets present several engineering challenges:

- Data is distributed across multiple REST APIs.
- Each dataset contains different schemas and field names.
- Data types are inconsistent across sources.
- Business definitions vary between datasets.
- No unified reporting model exists for enterprise analytics.
- Significant engineering effort is required before meaningful business analysis can begin.

Organizations wishing to analyze hospital performance across these datasets must first build robust data engineering pipelines capable of ingesting, validating, standardizing, modeling, and maintaining the information over time.

---

# Solution

This platform addresses those challenges by providing an automated cloud-native analytics solution that:

- Extracts data from nine independent CMS REST APIs.
- Archives raw JSON data within Google Cloud Storage.
- Validates and standardizes inconsistent source data.
- Automatically generates warehouse SQL from centralized metadata.
- Loads standardized datasets into a Medallion (Bronze → Silver → Gold) data warehouse.
- Builds dimensional business models optimized for analytics.
- Powers executive dashboards through Looker Studio.
- Refreshes the complete platform automatically each month using Cloud Scheduler and Cloud Functions.

The result is a centralized analytics platform capable of supporting executive reporting, operational analysis, healthcare benchmarking, and future analytical expansion.

---

# Project Highlights

Current platform capabilities include:

- 9 independent CMS data ingestion pipelines
- Fully modular Python ETL framework
- Google Cloud Storage raw data archive
- Metadata-driven schema registry
- Automated SQL generation
- Bronze → Silver → Gold warehouse architecture
- BigQuery dimensional data warehouse
- Executive reporting data models
- Interactive Looker Studio dashboards
- Automated monthly cloud execution
- Cloud Functions Gen2 orchestration
- Cloud Scheduler automation
- Secure serverless deployment
- Reusable shared pipeline framework

---

# Technology Stack

| Category | Technologies |
|-----------|--------------|
| Programming | Python |
| Cloud Platform | Google Cloud Platform |
| Data Storage | Google Cloud Storage |
| Data Warehouse | BigQuery |
| Data Processing | Pandas |
| APIs | CMS REST APIs |
| Business Intelligence | Looker Studio |
| Automation | Cloud Functions Gen2, Cloud Scheduler |
| Version Control | Git & GitHub |

---

# High-Level Architecture

```text
                    CMS Healthcare REST APIs
                               │
                               ▼
                 Python ETL Pipeline Framework
                               │
                               ▼
               Google Cloud Storage (Raw JSON)
                               │
                               ▼
                    healthcare_bronze
                   Raw Source Data Layer
                               │
                               ▼
             Metadata-Driven Schema Registry
                               │
                               ▼
                  Automated SQL Generation
                               │
                               ▼
                    healthcare_silver
              Cleaned & Standardized Data
                               │
                               ▼
                     healthcare_gold
             Business-Ready Dimensional Models
                               │
                               ▼
                     Looker Studio
                Executive Performance Dashboard
```

---

# Automated Cloud Architecture

The platform operates as a fully automated serverless solution hosted within Google Cloud Platform.

```text
                  Cloud Scheduler
                (Monthly Schedule)
                         │
                         ▼
            Cloud Functions Gen2 (HTTP)
                         │
                         ▼
              run_all_pipelines.py
             Pipeline Orchestration Layer
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
 Hospital Info      Readmissions      HCAHPS
        │                │                │
        └────────────────┼────────────────┘
                         │
                  Remaining CMS APIs
                         │
                         ▼
                Google Cloud Storage
                         │
                         ▼
               Bronze → Silver → Gold
                         │
                         ▼
               Looker Studio Dashboard
```

# Medallion Data Warehouse

The platform implements a Medallion Architecture to progressively improve data quality as it moves through the analytics pipeline.

```text
                    Bronze
                 Raw CMS Data
                      │
                      ▼
                    Silver
         Cleaned, Typed & Standardized
                      │
                      ▼
                     Gold
      Business-Ready Dimensional Models
                      │
                      ▼
          Executive Reporting & Analytics
```

Each layer serves a distinct purpose, allowing raw source data to remain unchanged while providing increasingly refined datasets optimized for business intelligence and analytical reporting.

---

# Bronze Layer

The Bronze layer stores the original CMS datasets exactly as received from each API.

Objectives:

- Preserve source system fidelity
- Maintain historical snapshots
- Support data lineage
- Enable auditing and troubleshooting
- Provide a reliable foundation for downstream transformations

Current Bronze datasets include:

- Hospital General Information
- Hospital Readmissions
- HCAHPS Patient Experience
- Hospital Mortality
- Timely & Effective Care
- Healthcare-Associated Infections
- Outpatient Imaging Efficiency
- Hospital Value-Based Purchasing
- Hospital-Acquired Condition Reduction Program

Characteristics:

- Raw JSON ingestion
- Minimal transformation
- One table per CMS dataset
- Cloud Storage archive maintained for every refresh

---

# Silver Layer

The Silver layer transforms raw CMS datasets into standardized analytical tables.

Rather than manually writing transformation SQL for every dataset, the platform generates warehouse SQL automatically from a centralized schema registry.

Key transformations include:

- SAFE_CAST data conversions
- Boolean normalization
- Date parsing
- Numeric validation
- Field standardization
- Null handling
- Business rule application
- Consistent naming conventions

Benefits:

- Consistent warehouse design
- Reduced manual development
- Easer onboarding of new datasets
- Metadata-driven transformations
- Improved maintainability

---

# Gold Layer

The Gold layer contains business-ready dimensional models optimized for reporting and analytics.

Rather than exposing raw CMS datasets directly to dashboard users, the Gold layer combines information across multiple source systems into intuitive business entities.

Current Gold models include:

## Dimension Tables

- dim_hospital

Provides standardized descriptive information for every hospital including:

- Facility identifiers
- Geographic information
- Hospital characteristics
- Ownership
- Hospital type
- Location attributes

---

## Fact Tables

### fact_hospital_performance_summary

Combines metrics across multiple CMS datasets into a single executive reporting model.

Current measures include:

- CMS Overall Hospital Rating
- Value-Based Purchasing Score
- Hospital-Acquired Condition Score
- Medicare Payment Reduction Indicator
- Hospital Performance Metrics
- Geographic attributes
- Organizational characteristics

This dimensional model powers the executive dashboard built in Looker Studio.

---

# Project Structure

```text
google-cloud-healthcare-analytics/

├── data/
│
├── dashboards/
│
├── deployment/
│   ├── deploy.sh
│   └── env.cloud.yaml
│
├── docs/
│
├── src/
│   ├── common/
│   │   ├── config.py
│   │   ├── bigquery.py
│   │   ├── storage.py
│   │   ├── cms_api.py
│   │   └── utilities.py
│   │
│   ├── pipelines/
│   │   ├── hospital_general_information/
│   │   ├── hospital_readmissions/
│   │   ├── hospital_hcahps/
│   │   ├── hospital_mortality/
│   │   ├── hospital_timely_effective_care/
│   │   ├── hospital_hai/
│   │   ├── hospital_outpatient_imaging/
│   │   ├── hospital_value_based_purchasing/
│   │   └── hospital_hac_reduction/
│   │
│   └── warehouse/
│       ├── schemas.py
│       ├── sql_generator.py
│       ├── build_silver.py
│       └── build_gold.py
│
├── run_all_pipelines.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Data Pipeline Framework

Each CMS dataset is implemented as an independent ETL pipeline.

```text
Extract
    │
    ▼
Transform
    │
    ▼
Load
    │
    ▼
Pipeline Coordinator
```

Every pipeline follows the same reusable architecture and shares common utility modules for:

- CMS API communication
- Cloud Storage operations
- BigQuery integration
- Configuration management
- Logging
- Error handling

This modular approach allows new CMS datasets to be added with minimal additional development while maintaining a consistent project structure.

---

# Metadata-Driven Schema Registry

One of the core architectural decisions within this project is the use of a centralized schema registry.

Rather than hard-coding warehouse schemas throughout the project, every dataset is defined once within a metadata repository.

Each field contains metadata including:

- Business name
- Business definition
- BigQuery data type
- Nullable status
- Transformation rules

The schema registry serves as the single source of truth for the warehouse.

---

# Automated SQL Generation

Instead of manually maintaining hundreds of lines of warehouse SQL, the platform automatically generates BigQuery SQL from the schema registry.

This approach provides several advantages:

- Consistent data typing
- Standardized transformations
- Reduced maintenance effort
- Easier expansion to new datasets
- Improved documentation
- Lower risk of implementation errors

By separating metadata from implementation logic, the platform becomes significantly easier to maintain and extend as additional CMS datasets are incorporated.

---

# Executive Dashboard

The platform includes an interactive executive dashboard built in Looker Studio that enables users to analyze hospital performance across the United States.

The dashboard is powered entirely by the Gold dimensional warehouse and provides executive-level insights into hospital quality, safety, and value-based purchasing performance.

Current dashboard capabilities include:

- Executive KPI scorecards
- Interactive geographic hospital map
- State-level performance comparisons
- Hospital rating distribution analysis
- Top and Bottom 10 state rankings
- Detailed hospital performance table
- Interactive filtering across all visualizations

Key performance indicators include:

- Total Hospitals
- Average CMS Overall Rating
- Average Value-Based Purchasing Score
- Average Hospital-Acquired Condition Score
- Medicare Payment Reduction Counts

The dashboard demonstrates how standardized healthcare data can be transformed into actionable business intelligence for executive decision-making.


---

# Production Features

The platform was designed using modern Analytics Engineering and cloud-native design principles.

Current production features include:

- Fully automated monthly cloud execution
- Serverless architecture using Cloud Functions Gen2
- Cloud Scheduler orchestration
- Metadata-driven warehouse generation
- Automated SQL generation
- Modular ETL framework
- Centralized configuration management
- Reusable pipeline architecture
- BigQuery dimensional warehouse
- Executive reporting layer
- Secure cloud deployment
- Scalable architecture for additional CMS datasets

---

# Technical Skills Demonstrated

This project demonstrates practical experience across multiple areas of modern Analytics Engineering and Cloud Data Engineering.

### Analytics Engineering

- Medallion Architecture
- Dimensional Modeling
- Metadata-Driven Development
- Data Warehouse Design
- Data Standardization
- Business Intelligence

### Data Engineering

- ETL Pipeline Development
- REST API Integration
- Cloud Data Pipelines
- Data Validation
- Data Transformation
- Schema Management

### Google Cloud Platform

- Google Cloud Storage
- BigQuery
- Cloud Functions Gen2
- Cloud Scheduler
- Serverless Computing

### Software Engineering

- Python
- Modular Application Architecture
- Configuration Management
- Reusable Components
- Logging
- Error Handling
- Git
- GitHub

---

# Current Project Status

## Completed

✅ Google Cloud infrastructure

✅ CMS API ingestion framework

✅ Nine independent ETL pipelines

✅ Google Cloud Storage raw archive

✅ Bronze warehouse layer

✅ Silver warehouse layer

✅ Gold dimensional warehouse

✅ Metadata-driven schema registry

✅ Automated SQL generation

✅ Executive reporting data model

✅ Looker Studio dashboard

✅ Cloud Functions deployment

✅ Cloud Scheduler monthly automation

---

# Future Enhancements

Potential future improvements include:


- Data quality monitoring framework
- Automated unit and integration testing
- Infrastructure as Code (Terraform)
- Additional Gold dimensional models
- Predictive analytics and machine learning
- Expanded healthcare quality metrics

---

# Why This Project

This project was created to demonstrate how modern cloud technologies and Analytics Engineering practices can transform fragmented public healthcare data into a scalable, automated business intelligence platform.

Rather than focusing solely on data visualization, the project emphasizes the complete analytics lifecycle—from data acquisition and cloud storage through warehouse engineering, dimensional modeling, automation, and executive reporting.

The overall architecture reflects many of the same design principles used within enterprise analytics organizations, including modular software design, reusable ETL pipelines, metadata-driven development, serverless cloud computing, and dimensional data warehousing.

---

# Acknowledgements

Healthcare data provided by the **Centers for Medicare & Medicaid Services (CMS)** through the CMS Provider Data APIs.

This project was developed for educational and portfolio purposes to demonstrate practical cloud data engineering, analytics engineering, and business intelligence skills using publicly available datasets.

---

# License

This repository is released under the MIT License.

