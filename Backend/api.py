from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import pytest
import openai  # Add this import
import os  # Add this import
from openai import OpenAI  # Import the OpenAI class

app = Flask(__name__)
CORS(app)

# Create an instance of the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_workout_plan(workout_plan):
    days = re.split(r'Day \d+:', workout_plan)[1:]  # Split by day, remove empty first element
    parsed_plan = []
    
    for day in days:
        exercises = re.findall(r'(\d+\.\s*[\w\s]+):\s*([\w\s]+)', day)
        day_plan = [{"name": ex[0].strip(), "details": ex[1].strip()} for ex in exercises]
        parsed_plan.append(day_plan)
    
    return parsed_plan

def generate_workout_plan(name, bio):
    # Implement the workout plan generation using OpenAI's API
    prompt = f"Generate a 5-day workout plan for {name}. Bio: {bio}\n\nFormat the response as follows:\nDay 1:\n1. Exercise: Details\n2. Exercise: Details\n...\nDay 2:\n1. Exercise: Details\n2. Exercise: Details\n...\n\nAfter the 5-day plan, provide a list of sources."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional fitness trainer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )

    generated_text = response.choices[0].message.content.strip()

    # Split the generated text into workout plan and sources
    parts = generated_text.split("\n\n")
    workout_plan = "\n\n".join(parts[:5])  # First 5 parts are the 5-day plan
    sources = parts[5] if len(parts) > 5 else ""

    return workout_plan, sources

@app.route('/generate_workout', methods=['POST'])
def generate_workout_api():
    name = request.args.get('name')
    bio = request.args.get('bio')
    
    if not name or not bio:
        return jsonify({"error": "Name and bio are required query parameters"}), 400
    
    workout_plan, sources = generate_workout_plan(name, bio)
    
    parsed_workout_plan = parse_workout_plan(workout_plan)
    
    response = {
        "workout_plan": parsed_workout_plan,
        "sources": sources
    }
    
    return jsonify(response)

@app.route('/generate_workout', methods=['GET'])
def generate_workout_get():
    return jsonify({"error": "This endpoint only supports POST requests"}), 405

if __name__ == "__main__":
    app.run(debug=True)

# Test functions
def test_parse_workout_plan():
    sample_plan = """Day 1: 1. Push-ups: 3 sets of 10 reps
Day 2: 1. Squats: 3 sets of 12 reps"""
    result = parse_workout_plan(sample_plan)
    assert len(result) == 2
    assert result[0][0]['name'] == '1. Push-ups'
    assert result[0][0]['details'] == '3 sets of 10 reps'
    assert result[1][0]['name'] == '1. Squats'
    assert result[1][0]['details'] == '3 sets of 12 reps'

def test_generate_workout_api():
    with app.test_client() as client:
        response = client.post('/generate_workout?name=John%20Doe&bio=I%20am%20a%2030-year-old%20office%20worker%20looking%20to%20get%20fit.')
        assert response.status_code == 200
        data = response.get_json()
        assert 'workout_plan' in data
        assert 'sources' in data

def test_missing_data():
    with app.test_client() as client:
        response = client.post('/generate_workout?name=John%20Doe')
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Name and bio are required query parameters'

def test_generate_workout_get():
    with app.test_client() as client:
        response = client.get('/generate_workout')
        assert response.status_code == 405
        data = response.get_json()
        assert data['error'] == 'This endpoint only supports POST requests'

if __name__ == "__main__":
    pytest.main([__file__])
