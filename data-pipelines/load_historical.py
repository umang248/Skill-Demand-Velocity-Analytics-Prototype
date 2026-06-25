import csv
import psycopg2

# 1. Update with your actual PostgreSQL credentials
DB_HOST = "localhost"
DB_NAME = "job_skill"      
DB_USER = "postgres"      
DB_PASSWORD = "your_password_here" # Put your pgAdmin/PostgreSQL password here

# 2. Point this to the file we just added dates to!
csv_file_path = r"file_path" # update this!

print("Connecting to the database...")

try:
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("Successfully connected to PostgreSQL!\nLoading data...")

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        jobs_added = 0
        for row in csv_reader:
            
            # 3. Map your specific CSV columns to our variables
            job_id = row.get('JobID', f'fallback_id_{jobs_added}')
            job_title = row.get('Title', 'Unknown Role')
            date_scraped = row.get('date_scraped', '2025-01-01')
            
            # 4. Fill in the missing columns with generic data
            source = "Kaggle Historical"
            company = "Undisclosed Company"
            location = "Remote"
            
            # 5. Stitch the text columns together to create a rich job description for the AI
            skills = row.get('Skills', '')
            responsibilities = row.get('Responsibilities', '')
            keywords = row.get('Keywords', '')
            
            job_description = f"Responsibilities: {responsibilities}\nSkills Required: {skills}\nKeywords: {keywords}"

            # 6. Insert into PostgreSQL
            insert_query = """
                INSERT INTO jobs_raw (job_id, source, company, job_title, location, job_description, date_scraped)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (job_id) DO NOTHING;
            """
            
            cursor.execute(insert_query, (
                job_id, source, company, job_title, location, job_description, date_scraped
            ))
            jobs_added += 1

    conn.commit()
    print(f"Success! {jobs_added} historical jobs have been mapped and loaded into the database.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()