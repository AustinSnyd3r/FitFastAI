import openai
import os
from dotenv import load_dotenv
from datetime import datetime
import requests

def get_user_info():
    name = input("Please enter your name: ")
    bio = input("Please provide a brief bio or any relevant information about yourself: ")
    return name, bio

def query_perplexity(query):
    load_dotenv()
    api_key = os.getenv('PERPLEXITY_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "query": query,
        "max_tokens": 1000
    }
    response = requests.post("https://api.perplexity.ai/chat/completions", json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['text']
    else:
        return None

def generate_workout_plan(name, bio):
    load_dotenv()
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Query Perplexity for supporting documents
    perplexity_query = f"Provide information on creating a personalized workout plan for {name} with the following bio: {bio}"
    supporting_info = query_perplexity(perplexity_query)

    prompt = f"""
    Name: {name}
    Bio: {bio}

    Supporting Information:
    {supporting_info}

    Based on the information provided and the supporting information, create a personalized workout plan for the next week. 
    The plan should include:
    1. Types of exercises for each day
    2. Duration of each session
    3. Any specific recommendations based on the user's bio and the supporting information
    4. A workout for each day of the week (exactly 5 days)
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful fitness assistant. Create a workout plan for exactly 5 days."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def save_workout_plan(name, workout_plan):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"Lessons/{name.lower().replace(' ', '_')}_{timestamp}_workout_plan.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as file:
        file.write(workout_plan)
    return filename

def main():
    name, bio = get_user_info()
    workout_plan = generate_workout_plan(name, bio)
    
    print("\nYour personalized workout plan for the next week (5 days):")
    print(workout_plan)

    filename = save_workout_plan(name, workout_plan)
    print(f"\nYour 5-day workout plan has been saved to {filename}")

if __name__ == "__main__":
    main()
