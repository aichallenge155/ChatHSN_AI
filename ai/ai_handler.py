import os
import asyncio
import google.generativeai as genai
from config import AI_API_KEY, RESPONSE_STYLES


genai.configure(api_key=AI_API_KEY)

# Model seçimi
model = genai.GenerativeModel("gemini-2.0-flash")


async def generate_response(prompt, style="default"):
    """Generate an AI response with a given style"""
    try:
        # Stili seçirik və tam promptu yaradırıq
        style_prompt = RESPONSE_STYLES.get(style, RESPONSE_STYLES["default"])
        full_prompt = f"{style_prompt}\n{prompt}"

        # Asenkron çalışma için run_in_executor kullanıyoruz
        response = await asyncio.to_thread(model.generate_content, full_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_response: {e}")
        return "Üzr istəyirəm, cavab yaradıla bilmədi."

async def find_citation(topic):
    """Find a scholarly citation for a given topic"""
    try:
        prompt = f"Provide a scholarly citation (author, year, title) for the topic: {topic}"
        
        # Asenkron çalışma için run_in_executor kullanıyoruz
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in find_citation: {e}")
        return "Mövzu üçün istinad yaradıla bilmədi."

async def define_term(term):
    """Define a specific term or concept"""
    try:
        prompt = f"Define the term: {term}"

        # Asenkron çalışma için run_in_executor kullanıyoruz
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in define_term: {e}")
        return "Term izah edilə bilmədi."

def get_error_message(error):
    """Return a more user-friendly error message based on the error type"""
    if "quota" in str(error).lower():
        return "API kvota limiti aşıldı. Zəhmət olmasa bir az sonra yenidən cəhd edin."
    elif "rate" in str(error).lower():
        return "Çox sayda sorğu göndərildi. Zəhmət olmasa bir az gözləyin və yenidən cəhd edin."
    elif "invalid" in str(error).lower():
        return "API açarı etibarsızdır. Zəhmət olmasa konfiqurasiyanı yoxlayın."
    else:
        return "Üzr istəyirəm, bir xəta baş verdi. Zəhmət olmasa bir az sonra yenidən cəhd edin."

async def generate_studyplan(topic):
    """Create a 3-day study plan for the given topic"""
    try:
        prompt = f"Create a 3-day study plan for: {topic}. Be clear, structured, and motivational."
        
        # Asenkron çalışma için run_in_executor kullanıyoruz
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_studyplan: {e}")
        return "Təəssüf, plan yaradıla bilmədi."
    