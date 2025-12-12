import requests

class AIAssistant:
    def __init__(self, api_key=None, provider="mock"):
        """
        Initialize the AI Assistant.
        :param api_key: Your API Key (e.g., OpenAI or Gemini).
        :param provider: 'mock' for testing, 'gemini' for Google, 'openai' for OpenAI.
        """
        self.api_key = api_key
        self.provider = provider

    def get_response(self, prompt):
        """
        Sends the prompt to the selected AI tool and returns the response.
        """
        if not prompt:
            return "Error: Prompt cannot be empty."

        if self.provider == "mock":
            return self._mock_response(prompt)
        
        elif self.provider == "gemini":
            # Example implementation for Google Gemini REST API
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
            headers = {'Content-Type': 'application/json'}
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                # Parse the complex JSON response from Gemini
                return response.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                return f"API Error: {str(e)}"

        return "Error: Provider not supported."

    def format_response(self, text):
        """
        Cleans up the AI response. 
        Removes markdown bolding (**text**) for cleaner raw display.
        """
        if not text:
            return ""
        # Remove markdown bold syntax for cleaner display
        clean_text = text.replace("**", "").replace("__", "")
        return clean_text.strip()

    def summarize_text(self, text):
        """
        Simulates a summary if the text is too long (Mock logic for demonstration).
        """
        if len(text) > 100:
            return text[:97] + "..."
        return text

    def _mock_response(self, prompt):
        """Internal method to generate fake responses for testing without an API key."""
        # Simple logic to make the mock response feel slightly dynamic
        responses = [
            f"That is an interesting question about '{prompt}'. Here is a mock AI response.",
            f"I am a student-built AI library. I received: {prompt}",
            "Processing your request... Analysis complete. Result: Positive."
        ]
        return responses[len(prompt) % 3]