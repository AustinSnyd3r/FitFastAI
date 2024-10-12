import openai
import os
from dotenv import load_dotenv

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
    1. Types of exercises
    2. Frequency of workouts
    3. Duration of each session
    4. Any specific recommendations based on the user's bio
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful fitness assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        n=1,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def main():
    name, bio = get_user_info()
    workout_plan = generate_workout_plan(name, bio)
    
    print("\nYour personalized workout plan for the next week:")
    print(workout_plan)

if __name__ == "__main__":
    main()
