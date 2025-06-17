import os
import sqlite3
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html

from .generate_db import create_sample_db
from .openai_utils import translate_to_sql

# Load OpenAI API key from environment variable
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

DATABASE = 'bookings.db'

st.title('Travel Agency Data Explorer')

# Input for natural language query
user_query = st.text_input('Enter your query about bookings:')

if user_query:
    try:
        sql_query = translate_to_sql(user_query)
        st.code(sql_query, language='sql')

        # Execute SQL query
        conn = sqlite3.connect(DATABASE)
        try:
            df = pd.read_sql_query(sql_query, conn)
        except Exception as e:
            st.error(f'SQL error: {e}')
            df = None
        conn.close()

        if df is not None and not df.empty:
            st.dataframe(df)

            # Basic D3 bar chart using first two columns
            if len(df.columns) >= 2:
                data_json = df.to_json(orient='records')
                x_col = df.columns[0]
                y_col = df.columns[1]
                d3_script = f"""
                <div id='chart'></div>
                <script src='https://d3js.org/d3.v7.min.js'></script>
                <script>
                const data = {data_json};
                const margin = {{top: 20, right: 30, bottom: 40, left: 40}},
                      width = 600 - margin.left - margin.right,
                      height = 400 - margin.top - margin.bottom;
                const svg = d3.select('#chart')
                    .append('svg')
                    .attr('width', width + margin.left + margin.right)
                    .attr('height', height + margin.top + margin.bottom)
                    .append('g')
                    .attr('transform', `translate(${{margin.left}},${{margin.top}})`);
                const x = d3.scaleBand()
                    .domain(data.map(d => d['{x_col}']))
                    .range([0, width])
                    .padding(0.1);
                const y = d3.scaleLinear()
                    .domain([0, d3.max(data, d => +d['{y_col}'])])
                    .nice()
                    .range([height, 0]);
                svg.append('g')
                    .attr('class', 'x-axis')
                    .attr('transform', `translate(0,${{height}})`)
                    .call(d3.axisBottom(x));
                svg.append('g')
                    .attr('class', 'y-axis')
                    .call(d3.axisLeft(y));
                svg.selectAll('.bar')
                    .data(data)
                    .enter()
                    .append('rect')
                    .attr('class', 'bar')
                    .attr('x', d => x(d['{x_col}']))
                    .attr('y', d => y(+d['{y_col}']))
                    .attr('width', x.bandwidth())
                    .attr('height', d => height - y(+d['{y_col}']))
                    .attr('fill', 'steelblue');
                </script>
                """
                html(d3_script, height=450)
            else:
                st.write('Not enough columns for chart.')
        else:
            st.write('No results.')
    except Exception as e:
        st.error(f'Error generating SQL: {e}')
