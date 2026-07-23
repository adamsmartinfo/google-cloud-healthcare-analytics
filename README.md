# Google Cloud Healthcare Analytics Platform

An end-to-end healthcare analytics platform that automates the ingestion, transformation, warehousing, and analysis of publicly available CMS (Centers for Medicare & Medicaid Services) hospital performance data using Google Cloud Platform.

The project demonstrates the complete analytics lifecycle—from cloud data engineering and dimensional modeling to executive business intelligence and AI-powered natural language analytics.

## Live Applications

- 🌐 **AI Analytics Web App:** https://ai-hospital-researcher-263128805643.us-west2.run.app
- 📊 **Executive Dashboard:** https://datastudio.google.com/reporting/71783706-f467-41ae-b63c-bcdf7c65e9c5

---

# Executive Summary

Healthcare organizations rely on CMS quality reporting data to evaluate hospital performance, patient outcomes, patient experience, and reimbursement programs. Although these datasets are publicly available, they are distributed across multiple APIs with inconsistent schemas, varying data types, and different business definitions, making meaningful analysis difficult.

This project addresses those challenges by building a modern cloud analytics platform that automatically extracts, validates, standardizes, and warehouses CMS data into a centralized BigQuery environment using a Medallion (Bronze → Silver → Gold) architecture.

The curated warehouse powers two complementary analytics experiences:

- **Executive Business Intelligence** through interactive Looker Studio dashboards.
- **AI-Powered Analytics** through a Streamlit application that enables users to explore the warehouse using natural language.

The result is a scalable analytics platform that demonstrates modern Analytics Engineering, Data Engineering, Business Intelligence, Cloud Engineering, and AI application development.

---

# Business Problem

CMS publishes thousands of hospital quality metrics covering areas such as:

- Hospital Overall Ratings
- Patient Experience (HCAHPS)
- Hospital Readmissions
- Mortality Measures
- Timely & Effective Care
- Healthcare-Associated Infections
- Outpatient Imaging Efficiency
- Value-Based Purchasing
- Hospital-Acquired Condition Reduction Program

While these datasets are valuable individually, they present several engineering challenges:

- Data is distributed across multiple REST APIs.
- Schemas differ across datasets.
- Data types are inconsistent.
- Business definitions vary between sources.
- No centralized reporting model exists.
- Significant engineering work is required before meaningful analysis can begin.

Organizations wishing to analyze hospital performance across these datasets must first build reliable pipelines capable of ingesting, validating, standardizing, modeling, and maintaining the data over time.

---

# Solution

This platform provides an automated cloud-native analytics solution that:

- Extracts data from nine CMS REST APIs.
- Archives raw source data in Google Cloud Storage.
- Standardizes data using a metadata-driven transformation framework.
- Loads data into a BigQuery Medallion warehouse.
- Builds business-ready dimensional models.
- Delivers executive dashboards through Looker Studio.
- Extends the warehouse with an AI-powered analytics application built with Streamlit and LangGraph.
- Deploys the AI application publicly using Docker and Google Cloud Run.

The platform demonstrates how a well-designed cloud data warehouse can support both traditional business intelligence and modern AI-assisted analytics.

---

# Project Highlights

### Data Engineering

- 9 automated CMS data ingestion pipelines
- Metadata-driven schema registry
- Automated SQL generation
- Bronze → Silver → Gold Medallion architecture
- BigQuery dimensional data warehouse
- Fully automated monthly cloud execution

### Business Intelligence

- Executive KPI dashboard
- Interactive geographic visualizations
- State performance comparisons
- Hospital performance drill-downs
- Cross-filtering and interactive reporting

### AI Analytics

- Natural language analytics interface
- LangGraph agent workflow
- Automatic SQL generation
- BigQuery query execution
- AI-generated result explanations
- Automatic data visualizations

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
| AI Framework | LangGraph |
| LLM | GitHub Models (GPT-4.1 Mini) |
| Web Application | Streamlit |
| Deployment | Docker, Google Cloud Run |
| Automation | Cloud Functions Gen2, Cloud Scheduler |
| Version Control | Git & GitHub |

---

# Platform Architecture

The platform follows a modern cloud analytics architecture that transforms fragmented healthcare datasets into business-ready analytical assets. Public CMS data is ingested through automated Python ETL pipelines, standardized using a metadata-driven transformation framework, and stored in a Medallion (Bronze → Silver → Gold) data warehouse within BigQuery.

The curated Gold layer serves as the single source of truth for both executive dashboards and AI-powered natural language analytics.

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
                     ┌─────────┴─────────┐
                     ▼                   ▼
          Looker Studio           AI Analytics
      Executive Dashboard         Web Application

---

# Executive Business Intelligence

The first analytics experience built on top of the curated Gold warehouse is an executive dashboard developed in Looker Studio.

Rather than requiring users to query raw healthcare datasets, the dashboard presents key performance indicators and visualizations that allow executives to quickly assess hospital quality, patient outcomes, and reimbursement metrics.

Current dashboard capabilities include:

- Executive KPI scorecards
- Interactive geographic hospital map
- State-level performance comparisons
- Hospital rating distribution
- Top and Bottom 10 state rankings
- Detailed hospital performance table
- Interactive filtering across all visualizations

Key performance indicators include:

- Total Hospitals
- Average CMS Overall Rating
- Average Value-Based Purchasing Score
- Average Hospital-Acquired Condition Score
- Medicare Payment Reduction Counts

> **Screenshot Placeholder**
>
> Insert the primary Looker Studio dashboard screenshot here.

The dashboard demonstrates how curated healthcare data can be transformed into executive-ready business intelligence that supports operational decision making.

---

# AI Analytics Web Application

To extend the capabilities of the platform beyond traditional dashboards, I developed an AI-powered analytics application using Streamlit and LangGraph.

Instead of navigating dashboards or writing SQL, users can ask questions about hospital performance using natural language. The application translates user requests into SQL, retrieves data from the BigQuery warehouse, explains the results, and generates visualizations automatically.

Example questions include:

- Which states have the highest average hospital ratings?
- Show the average Value-Based Purchasing score by state.
- Which hospitals received Medicare payment reductions?
- Compare hospital ratings across Utah.

For every request, the application:

1. Interprets the user's question.
2. Generates SQL using an LLM.
3. Validates the generated query.
4. Executes the query against BigQuery.
5. Returns the results.
6. Explains the findings in plain language.
7. Automatically creates an appropriate visualization.

> **Screenshot Placeholder**
>
> Insert the main AI application screenshot here.

---

# AI Application Features

Current capabilities include:

- Natural language analytics
- LangGraph workflow orchestration
- Automatic SQL generation
- SQL transparency
- BigQuery integration
- AI-generated explanations
- Interactive data tables
- Automatic chart generation
- Public web deployment using Google Cloud Run

---

# AI Architecture

The AI application uses a LangGraph workflow to transform natural language questions into actionable business insights.

```text
                User Question
                      │
                      ▼
            Streamlit Web Interface
                      │
                      ▼
               LangGraph Workflow
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
Interpret Query   Generate SQL   Validate SQL
      │               │                │
      └───────────────┼────────────────┘
                      ▼
                Google BigQuery
                      │
                      ▼
                Query Results
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 AI Explanation            Visualization Engine
        │                           │
        └─────────────┬─────────────┘
                      ▼
             Streamlit Application

---

# Repository Structure

```text
google-cloud-healthcare-analytics/

├── app/                     # Streamlit AI Analytics application
│   ├── app.py
│   ├── pages/
│   └── components/
│
├── src/
│   ├── common/
│   ├── pipelines/
│   ├── warehouse/
│   └── ai/
│
├── deployment/
│
├── dashboards/
│
├── docs/
│
├── Dockerfile
├── deploy_streamlit.sh
├── requirements.txt
└── README.md

---

# Next Steps

Potential enhancements that could be added in future iterations include:

- Expanding the data warehouse with additional CMS datasets
- User authentication and role-based access
- Conversation history for AI analytics sessions
- Exporting AI-generated analyses to PDF or Excel
- Retrieval-Augmented Generation (RAG) using CMS documentation
- Predictive analytics and machine learning models
- Infrastructure as Code (Terraform)
- Automated unit and integration testing

---

# Conclusion

This project demonstrates the complete analytics lifecycle, beginning with raw public healthcare data and ending with multiple analytics experiences built on a trusted cloud data warehouse.

The platform combines modern Analytics Engineering, Data Engineering, Business Intelligence, Cloud Engineering, and AI application development into a single end-to-end solution.

By separating data ingestion, warehouse engineering, reporting, and AI into modular components, the platform is designed to be scalable, maintainable, and extensible while demonstrating technologies commonly used in enterprise analytics organizations.

---

# Acknowledgements

Healthcare data is provided by the **Centers for Medicare & Medicaid Services (CMS)** through the CMS Provider Data APIs.

This project was developed for educational and portfolio purposes using publicly available datasets.

---

# License

This project is licensed under the MIT License.

