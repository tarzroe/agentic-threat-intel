import time
import google.generativeai as genai

def call_gemini(prompt, system_instruction=None, max_retries=3):
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    target_model = None
    for m_name in available_models:
        if 'flash' in m_name:
            target_model = m_name
            break
    if not target_model:
        target_model = available_models[0] if available_models else 'gemini-pro'

    model = genai.GenerativeModel(
        model_name=target_model,
        system_instruction=system_instruction
    )

    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "500 POST" in str(e) and attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise
    return "Error: Could not generate content after multiple retries."
