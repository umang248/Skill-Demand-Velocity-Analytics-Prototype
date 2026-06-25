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
2. **AI Extraction Layer (`extract_skills.py`):** Utilizes the Google Gemini 1.5 Flash API to parse unstructured text blocks and extract normalized, confidence-scored technical skills via forced JSON schemas.
3. **Analytics Warehouse (`build_warehouse.py` & `calculate_velocity.py`):** Transforms raw event data into a dimensional Fact Table, utilizing SQL Common Table Expressions (CTEs) and Window Functions to calculate month-over-month adoption trajectories.
4. **Presentation Layer:** A Power BI dashboard connected directly to the pre-computed, heavily filtered `emerging_skills_final` table for zero-latency insights.
