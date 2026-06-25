import psycopg2

# 1. Database Credentials
DB_HOST = "localhost"
DB_NAME = "job_skill"      
DB_USER = "postgres"      
DB_PASSWORD = "your_password" # Update this!

print("Connecting to database to build the Analytics Warehouse...")

try:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    
    print("Refreshing fact table schema...")
    cursor.execute("DROP TABLE IF EXISTS fact_job_skill_month;")
    
    cursor.execute("""
        CREATE TABLE fact_job_skill_month (
            id SERIAL PRIMARY KEY,
            month VARCHAR(7), 
            job_role VARCHAR(255),
            skill VARCHAR(1000),
            job_count INT
        );
    """)
    
    print("Aggregating historical data and populating the warehouse...")

    insert_query = """
        INSERT INTO fact_job_skill_month (month, job_role, skill, job_count)
        SELECT 
            TO_CHAR(j.date_scraped, 'YYYY-MM') AS month,
            j.job_title AS job_role,
            s.skill AS skill,
            COUNT(DISTINCT j.job_id) AS job_count
        FROM 
            jobs_raw j
        JOIN 
            skills_extracted s ON j.job_id = s.job_id
        WHERE 
            s.skill IS NOT NULL
        GROUP BY 
            TO_CHAR(j.date_scraped, 'YYYY-MM'),
            j.job_title,
            s.skill
        ORDER BY 
            month DESC, job_count DESC;
    """
    
    cursor.execute(insert_query)
    
    cursor.execute("SELECT COUNT(*) FROM fact_job_skill_month;")
    total_rows = cursor.fetchone()[0]
    
    conn.commit()
    print(f"Success! The warehouse is built. Generated {total_rows} aggregated trend records.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()
