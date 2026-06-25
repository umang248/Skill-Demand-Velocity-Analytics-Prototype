import psycopg2

# 1. Database Credentials
DB_HOST = "localhost"
DB_NAME = "job_skill"      
DB_USER = "postgres"      
DB_PASSWORD = "your_password" # Update this!

print("Booting up the Skill Demand Velocity Engine...")

try:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    
    # 2. Create the final analytics table
    print("Setting up the velocity table...")
    cursor.execute("DROP TABLE IF EXISTS skill_velocity_monthly;")
    cursor.execute("""
        CREATE TABLE skill_velocity_monthly (
            id SERIAL PRIMARY KEY,
            month VARCHAR(7),
            job_role VARCHAR(255),
            skill VARCHAR(100),
            job_count INT,
            adoption_rate DECIMAL(5,2),
            velocity DECIMAL(5,2)
        );
    """)
    
    # 3. The Analytics Engine (Using SQL Common Table Expressions)
    print("Calculating month-over-month adoption and velocity...")
    insert_query = """
        INSERT INTO skill_velocity_monthly (month, job_role, skill, job_count, adoption_rate, velocity)
        WITH RoleTotals AS (
            -- Step A: Find the total number of jobs per role, per month
            SELECT TO_CHAR(date_scraped, 'YYYY-MM') AS month, job_title AS job_role, COUNT(DISTINCT job_id) as total_jobs
            FROM jobs_raw
            GROUP BY 1, 2
        ),
        Adoption AS (
            -- Step B: Calculate what percentage of jobs require this skill
            SELECT 
                f.month, f.job_role, f.skill, f.job_count,
                ROUND((f.job_count::DECIMAL / r.total_jobs) * 100, 2) AS adoption_rate
            FROM fact_job_skill_month f
            JOIN RoleTotals r ON f.month = r.month AND f.job_role = r.job_role
        ),
        Velocity AS (
            -- Step C: Compare this month's adoption to last month's using LAG()
            SELECT 
                month, job_role, skill, job_count, adoption_rate,
                LAG(adoption_rate) OVER (PARTITION BY job_role, skill ORDER BY month) AS prev_month_adoption
            FROM Adoption
        )
        -- Step D: Calculate the final velocity (current - previous)
        SELECT 
            month, job_role, skill, job_count, adoption_rate,
            (adoption_rate - prev_month_adoption) AS velocity
        FROM Velocity
        WHERE prev_month_adoption IS NOT NULL -- Only keep rows where we have historical data to compare against
        ORDER BY velocity DESC;
    """
    
    cursor.execute(insert_query)
    
    cursor.execute("SELECT COUNT(*) FROM skill_velocity_monthly;")
    total_rows = cursor.fetchone()[0]
    
    conn.commit()
    print(f"Engine complete! Identified {total_rows} high-signal skill velocity trends.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()
