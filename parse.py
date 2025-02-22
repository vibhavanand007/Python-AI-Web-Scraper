import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_groq(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Prepare the prompt
        prompt = template.format(dom_content=chunk, parse_description=parse_description)

        # Call the Groq API
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert text extractor."},
                {"role": "user", "content": prompt},
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0  # Set to 0.0 for deterministic results
        )

        # Extract the AI's response
        ai_response = response.choices[0].message.content.strip()
        print(f'Parsed batch {i} of {len(dom_chunks)}')
        parsed_results.append(ai_response)

    return '\n'.join(parsed_results)