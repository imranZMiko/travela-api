# Travela API
The backend API for the [Travela](https://github.com/NaimaHasan/travela) website.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/imranZMiko/travela-api.git
cd travela-api
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

## Usage

To launch the development server and start using the API, run the following command:

```bash
python manage.py runserver
```
