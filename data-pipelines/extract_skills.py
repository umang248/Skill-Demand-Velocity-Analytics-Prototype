import psycopg2
import google.generativeai as genai
import json
import time

# 1. Your Credentials
DB_HOST = "localhost"
DB_NAME = "job_skill"      
DB_USER = "postgres"      
DB_PASSWORD = "your_password" # Your pgAdmin password
GEMINI_API_KEY = "your_gemini_api_key" # Paste your Google API key here

# 2. Configure the AI
genai.configure(api_key=GEMINI_API_KEY)
# We use the 'flash' model because it is incredibly fast and perfect for text extraction
model = genai.GenerativeModel('gemini-2.5-flash')

print("Connecting to the database...")

try:
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    cursor = conn.cursor()
    
    # 3. Fetch just 5 jobs to test the pipeline (I don't want to burn your API limits yet!)
    print("Fetching 5 un-processed jobs...")
    cursor.execute("""
        SELECT job_id, job_description 
        FROM jobs_raw 
        WHERE job_id NOT IN (SELECT DISTINCT job_id FROM skills_extracted)
        LIMIT 5; 
    """)
    jobs = cursor.fetchall()
    
    if not jobs:
        print("No new jobs to process!")
    
    for job_id, description in jobs:
        print(f"\nAnalyzing Job ID: {job_id}...")
        
        # 4. The Prompt Engine: Telling Gemini exactly what we want
        prompt = f"""
        You are a specialized Data Engineer AI. Extract the core technical and professional skills from the following job description.
        Return the exact output as a raw JSON array of objects. Do not include markdown formatting or explanation text.
        Format example: [{{"skill": "Python"}}, {{"skill": "Data Analysis"}}]
        
        Job Description:
        {description}
        """
        
        # 5. Call the API
        response = model.generate_content(prompt)
        
        # 6. Clean the AI's response to ensure it is pure JSON
        raw_text = response.text.strip().replace("```json", "").replace("```", "")
        
        try:
            skills_data = json.loads(raw_text)
            
            # 7. Save each extracted skill to the database
            for item in skills_data:
                skill_name = item.get("skill", "Unknown")
                
                
                cursor.execute("""
                    INSERT INTO skills_extracted (job_id, skill)
                    VALUES (%s, %s)
                """, (job_id, skill_name))
            
            print(f"Successfully extracted {len(skills_data)} skills!")
            conn.commit()
            
        except json.JSONDecodeError:
            print("Error: Gemini did not return valid JSON. Skipping to next job.")
            conn.rollback() # Undo this specific transaction so we don't break the database
            
        # Add a 2-second pause so we don't overwhelm the free API tier
        time.sleep(2)

    print("\nExtraction test complete!")

except Exception as e:
    print(f"A massive error occurred: {e}")

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()