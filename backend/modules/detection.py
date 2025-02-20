# import google.generativeai as genai

# class ScamDetectionAI:
#     def __init__(self, api_key):
#         """
#         Initializes the Scam Detection AI with Gemini.
#         """
#         genai.configure(api_key=api_key)
#         self.model = genai.GenerativeModel("gemini-pro", safety_settings={
#     "HARM_CATEGORY_DANGEROUS_CONTENT": "low"
# })  # Define the Gemini model

#     def detect_scam_with_gemini(self, text, retrieved_texts):
#         """
#         Uses Gemini AI to analyze text for scam detection.
#         Handles safety filters gracefully.
#         """
#         prompt = f"""
#         You are an AI scam detection assistant. Analyze the following conversation and detect whether it's a scam.

#         **Conversation:** "{text}"

#         **Reference Scam Conversations:** {retrieved_texts}

#         If the conversation contains phishing attempts, urgent financial requests, or instructions to install software, classify it as "suspicious."
#         Otherwise, classify it as "not suspicious."

#         Provide an explanation for your classification.

#         if "scam_result": "Gemini AI refused to generate a response due to content policies." they just give scam
#         """

#         try:
#             response = self.model.generate_content(prompt)

#             # Check if the response has valid content
#             if response.candidates and response.candidates[0].content:
#                 return response.candidates[0].content.parts[0].text
#             else:
#                 return "Gemini AI refused to generate a response due to content policies."

#         except Exception as e:
#             return f"Error: {str(e)}"


import requests

class ScamDetectionAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
  # Groq API endpoint

    def detect_scam_with_llama3(self, text, retrieved_texts):
        prompt = f"""
        You are an AI scam detection assistant. Analyze the following conversation and detect whether it's a scam.

        **Conversation:** "{text}"

        **Reference Scam Conversations:** {retrieved_texts}

        If the conversation contains phishing attempts, urgent financial requests, or instructions to install software, or access through anydesk or pc accessing sofware then classify it as "suspicious."
        Otherwise, classify it as "not suspicious."

        Provide an explanation for your classification.
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response_json = response.json()

            if "choices" in response_json and response_json["choices"]:
                return response_json["choices"][0]["message"]["content"]
            elif "error" in response_json:
                return f"Error: {response_json['error']['message']}"  
            else:
                return "Error: Unexpected response format from Groq API."

        except requests.exceptions.RequestException as e:
            return f"Error: API request failed - {str(e)}"
