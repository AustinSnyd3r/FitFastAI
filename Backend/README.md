# Backend

This is the backend for the FitFastAI project. Please refer to the project's [README](../README.md) for more information.

## Setup

make a new virtual environment:

```bash
python -m venv venv
```

install dependencies:

```bash
pip install -r requirements.txt
```

Running the server

```bash
python api.py
```

or from the root directory:

```bash
python Backend/api.py
```

*Additionally, the Flask server can be run with `flask run` from the root directory, but this is untested.*

## Testing

Testing is currently implemented using `pytest`. To run the tests:

```bash
pytest
```

Additionally, tests can be run with Postman manually.
i.e. with such query: `http://127.0.0.1:5000/generate_workout?name=Alice Williams&bio=I am a kyokushin white belt who has delayed training for one week looking to jump back in.`

Please refer to the root [README](../README.md) for more information on how to run the frontend.
