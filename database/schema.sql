
CREATE TABLE jobs_raw (
    job_id VARCHAR(255) PRIMARY KEY,
    source VARCHAR(100),
    company VARCHAR(255),
    job_title VARCHAR(255),
    location VARCHAR(255),
    job_description TEXT,
    date_scraped DATE
);

select *
from jobs_raw

CREATE TABLE IF NOT EXISTS skills_extracted (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(255) REFERENCES jobs_raw(job_id),
    skill VARCHAR(1000)
);

select * from skills_extracted
select * from fact_job_skill_month --created in build_warehouse.py
select * from skill_velocity_monthly --created in calculate_velocity.py
select * from focused_role_velocity --created in create_filtered_table.py
select * from emerging_skills_final --detect_emerging_skills.py
