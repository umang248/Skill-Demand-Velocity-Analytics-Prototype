import psycopg2

# 1. Database Credentials
DB_HOST = "localhost"
DB_NAME = "job_skill"      
DB_USER = "postgres"      
DB_PASSWORD = "your_password" # Update this!

# 2. Define the specific roles you want to isolate
# Note: Ensure the spelling matches your database exactly. 
target_roles = ('Product Manager', 'Data Enigineer', 'AI Engineer - Experienced', 'AI Prompt Engineer', 'BI Analyst - Experienced', 'Big Data Specialist', 'Business Ana;yst', 'Cloud Engineer - Experienced', 'Fintech Engineer', 'Market Research Analyst', 'Product Designer', 'Python Developer', 'SEO Specialist', 'UI Designer',  )

print(f"Creating a new targeted table for: {target_roles}...")

try:
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    
    # 3. Clear the table if it already exists so we can safely re-run this script
    cursor.execute("DROP TABLE IF EXISTS focused_role_velocity;")
    
    # 4. The CTAS Command (Create Table As Select)
    # The %s allows psycopg2 to safely inject your target_roles list
    query = """
        CREATE TABLE focused_role_velocity AS
        SELECT *
        FROM skill_velocity_monthly
        WHERE job_role IN %s
        ORDER BY job_role ASC, velocity DESC;
    """
    
    cursor.execute(query, (target_roles,))
    
    # 5. Verify the results
    cursor.execute("SELECT COUNT(*) FROM focused_role_velocity;")
    total_rows = cursor.fetchone()[0]
    
    conn.commit()
    print(f"Success! The 'focused_role_velocity' table has been created with {total_rows} rows.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()