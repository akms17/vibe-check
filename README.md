# Travel Agency Data Explorer

This repository provides a small example of using Streamlit together with
OpenAI to translate natural language questions into SQL queries against a
sample SQLite database. The results are visualised with D3.js.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate the sample database:
   ```bash
   python -m travel_explorer.generate_db
   ```
3. Set your OpenAI API key in the environment:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run src/travel_explorer/app.py
   ```

## Running Tests

Execute unit tests with `pytest`:
```bash
pytest
```

## Usage

Enter a natural language query (for example, "show total bookings by country"),
and the app will generate and execute a SQL statement. The results are shown in
a table and visualised with a simple D3 bar chart using the first two columns of
the query output.
