import google.generativeai as genai

class ScamDetectionAI:
    def __init__(self, api_key):
        """
        Initializes the Scam Detection AI with Gemini.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-pro")  # Define the Gemini model

    def detect_scam_with_gemini(self, text, retrieved_texts):
        """
        Uses Gemini AI to analyze text for scam detection.
        Handles safety filters gracefully.
        """
        prompt = f"""
        You are an AI scam detection assistant. Analyze the following conversation and detect whether it's a scam.

        **Conversation:** "{text}"

        **Reference Scam Conversations:** {retrieved_texts}

        If the conversation contains phishing attempts, urgent financial requests, or instructions to install software, classify it as "suspicious."
        Otherwise, classify it as "not suspicious."

        Provide an explanation for your classification.
        """

        try:
            response = self.model.generate_content(prompt)

            # Check if the response has valid content
            if response.candidates and response.candidates[0].content:
                return response.candidates[0].content.parts[0].text
            else:
                return "Gemini AI refused to generate a response due to content policies."

        except Exception as e:
            return f"Error: {str(e)}"
