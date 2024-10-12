import openai
import os
from dotenv import load_dotenv
from datetime import datetime

def get_user_info():
    name = input("Please enter your name: ")
    bio = input("Please provide a brief bio or any relevant information about yourself: ")
    return name, bio

def generate_workout_plan(name, bio):
    load_dotenv()
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
    Name: {name}
    Bio: {bio}

    Based on the information provided, create a personalized workout plan for the next week. 
    The plan should include:
    1. Types of exercises for each day
    2. Duration of each session
    3. Any specific recommendations based on the user's bio
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
