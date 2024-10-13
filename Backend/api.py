from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import requests
import re
import json
import sys

app = Flask(__name__)
CORS(app)

load_dotenv()
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def query_perplexity(query):
    api_key = os.getenv('PERPLEXITY_API_KEY')
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query}
        ]
    }
    response = requests.post("https://api.perplexity.ai/chat/completions", json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'], response.json().get('sources', [])
    else:
        print(f"Error querying Perplexity API: {response.status_code}", file=sys.stderr)
        print(f"Response content: {response.text}", file=sys.stderr)
        return None, []

def generate_workout_plan(name, bio):
    perplexity_query = f"Provide information on creating a personalized workout plan for {name} with the following bio: {bio}"
    supporting_info, sources = query_perplexity(perplexity_query)
    
    if supporting_info is None:
        supporting_info = ""
        sources = []

    sources_text = "\n".join([f"- {source}" for source in sources])

    prompt = f"""
    Name: {name}
    Bio: {bio}

    Supporting Information:
    {supporting_info}

    Sources:
    {sources_text}

    Based on the information provided, create a personalized workout plan for exactly 5 days.
    For each day, provide:
    1. Types of exercises
    2. Duration of each session
    3. Any specific recommendations

    Format the response as follows:
    Day 1:
    Exercises: [List exercises here]
    Duration: [Duration here]
    Recommendations: [Recommendations here]

    Day 2:
    ...

    Continue this format for all 5 days.
    """

    try:
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
        return response.choices[0].message.content.strip(), sources
    except Exception as e:
        print(f"Error generating workout plan: {str(e)}", file=sys.stderr)
        return None, []

def parse_workout_plan(plan_text):
    days = re.split(r'Day \d+:', plan_text)[1:]  # Split by day, remove empty first element
    parsed_plan = []
    
    for day in days:
        day_dict = {}
        exercises_match = re.search(r'Exercises:(.*?)Duration:', day, re.DOTALL)
        duration_match = re.search(r'Duration:(.*?)Recommendations:', day, re.DOTALL)
        recommendations_match = re.search(r'Recommendations:(.*)', day, re.DOTALL)
        
        if exercises_match:
            day_dict['exercises'] = exercises_match.group(1).strip()
        if duration_match:
            day_dict['duration'] = duration_match.group(1).strip()
        if recommendations_match:
            day_dict['recommendations'] = recommendations_match.group(1).strip()
        
        parsed_plan.append(day_dict)
    
    return parsed_plan

@app.route('/generate_workout', methods=['POST'])
def generate_workout_api():
    name = request.args.get('name')
    bio = request.args.get('bio')
    
    if not name or not bio:
        return jsonify({"error": "Name and bio are required query parameters"}), 400
    
    workout_plan, sources = generate_workout_plan(name, bio)
    
    if workout_plan is None:
        return jsonify({"error": "Failed to generate workout plan"}), 500
    
    try:
        parsed_workout_plan = parse_workout_plan(workout_plan)
    except Exception as e:
        print(f"Error parsing workout plan: {str(e)}", file=sys.stderr)
        return jsonify({"error": "Failed to parse workout plan"}), 500
    
    response = {
        "workout_plan": parsed_workout_plan,
        "sources": sources
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
