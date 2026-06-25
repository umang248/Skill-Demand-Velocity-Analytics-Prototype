import psycopg2

# 1. Database Credentials
DB_HOST = "localhost"
DB_NAME = "job_skill"      
DB_USER = "postgres"      
DB_PASSWORD = "your_password" # Update this!

print("Applying statistical filters for Emerging Skill Detection...")

try:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    
    # 2. Create the final "Golden" table for Power BI
    print("Generating final dashboard view...")
    cursor.execute("DROP TABLE IF EXISTS emerging_skills_final;")
    
    # 3. Apply your architectural thresholds (Velocity > 10%, Mentions > 2)
    cursor.execute("""
        CREATE TABLE emerging_skills_final AS
        SELECT 
            month, 
            job_role, 
            skill, 
            job_count, 
            adoption_rate, 
            velocity
        FROM focused_role_velocity
        WHERE velocity >= 10.00 
          AND job_count >= 2
        ORDER BY velocity DESC, job_count DESC;
    """)
    
    # 4. Check the results
    cursor.execute("SELECT COUNT(*) FROM emerging_skills_final;")
    total_signals = cursor.fetchone()[0]
    
    conn.commit()
    print(f"Filter complete! Identified {total_signals} highly validated emerging skill signals.")
    print("Your data pipeline is 100% complete and ready for Power BI.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()