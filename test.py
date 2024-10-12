import openai
import os
from dotenv import load_dotenv

def get_user_info():
    name = input("Please enter your name: ")
    bio = input("Please provide a brief bio or any relevant information about yourself: ")
    return name, bio

def generate_workout_plan(name, bio):
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

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

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def main():
    name, bio = get_user_info()
    workout_plan = generate_workout_plan(name, bio)
    
    print("\nYour personalized workout plan for the next week:")
    print(workout_plan)

if __name__ == "__main__":
    main()
