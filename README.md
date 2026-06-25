# Job Market Intelligence Platform: Skill-Demand-Velocity-Analytics-Prototype

## Executive Summary
Traditional job boards and labor market reports provide a static snapshot of what companies want *today*. This platform was built to predict what companies will need *tomorrow*. 

Instead of measuring the absolute volume of job requirements, this pipeline calculates **Skill Demand Velocity**—the month-over-month acceleration (or deceleration) of specific technical skills within targeted roles (e.g., Product Management, Strategy, Data Analytics). 

By leveraging an LLM to parse unstructured job descriptions and an SQL-based analytical warehouse to calculate trend deltas, this tool isolates emerging market signals before they become mainstream requirements.

---

##  The Core Innovation: Skill Demand Velocity
Absolute job counts are heavily biased toward legacy technologies. To find true market momentum, this platform uses a custom metric:

1. **Adoption Rate:** `(Jobs requiring Skill X / Total jobs in that Role) * 100`
2. **Velocity Engine (SQL `LAG()`):** `Current Month Adoption Rate - Previous Month Adoption Rate`
3. **Emerging Signal Threshold:** Filters for skills showing a strictly positive velocity (e.g., +1.00% MoM) with a statistically significant minimum job count to eliminate small-sample noise.

---

##  System Architecture & Data Flow

This repository contains the backend infrastructure and analytical engine, structured into four distinct layers:

1. **Ingestion Layer:** Raw job market data loaded into a PostgreSQL database.
2. **AI Extraction Layer (`extract_skills.py`):** Utilizes the Google Gemini 2.5 Flash API to parse unstructured text blocks and extract normalized, confidence-scored technical skills via forced JSON schemas.
3. **Analytics Warehouse (`build_warehouse.py` & `calculate_velocity.py`):** Transforms raw event data into a dimensional Fact Table, utilizing SQL Common Table Expressions (CTEs) and Window Functions to calculate month-over-month adoption trajectories.
4. **Presentation Layer:** A Power BI dashboard connected directly to the pre-computed, heavily filtered `emerging_skills_final` table for zero-latency insights.

---

## Tech Stack
* **Language:** Python 3.x
* **Database:** PostgreSQL (pgAdmin 4 / psycopg2)
* **AI/LLM:** Google Generative AI (Gemini 2.5 Flash)
* **Business Intelligence:** Microsoft Power BI

---

## Data Source & Project Scope
### Dataset
You can download the dataset used in this project from the release section of this repo.
### Why a Historical Dataset Was Used
The original vision for this project was to build a fully automated job market intelligence pipeline that continuously collects job postings from online job boards and analyzes emerging skill trends over time.   

During development, I explored scraping data from major job platforms. However, modern job websites employ various anti-bot mechanisms such as CAPTCHAs, authentication requirements, rate limiting, and frequent frontend changes, making reliable large-scale data collection difficult without dedicated infrastructure and ongoing maintenance.  

Since the primary objective of this project was to develop and validate the Skill Demand Velocity methodology, I chose to use a historical job-posting dataset instead of building a production-grade scraping system.

This approach allowed me to focus on the core analytical components of the project:
* Data cleaning and preparation
* Skill extraction and normalization
* Monthly skill adoption analysis
* Skill Demand Velocity calculation
* Emerging skill detection
* Dashboard development and business insights

### Future Enhancements
A future version of this project could integrate live job data from APIs, ATS platforms, or other reliable sources to continuously update skill demand trends and provide real-time workforce intelligence.
