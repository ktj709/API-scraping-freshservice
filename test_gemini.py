# test_gemini.py
from config import Config
from google import genai

def test_gemini():
    if not Config.GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found. Check your .env file.")
        return

    try:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=["Hello Gemini, can you confirm you are working?"]
        )
        print("✅ Gemini response:")
        print(response.text)
    except Exception as e:
        print("❌ Error calling Gemini:", e)

if __name__ == "__main__":
    test_gemini()
