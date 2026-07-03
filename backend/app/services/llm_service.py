from openai import OpenAI

from app.core.config import settings


class LLMService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_response(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str,
    ) -> str:
        """
        Generate a response using the OpenAI Responses API.
        """

        try:
            response = self.client.responses.create(
                model=model,
                input=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "input_text",
                                "text": system_prompt,
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": user_prompt,
                            }
                        ],
                    },
                ],
            )

            return response.output_text

        except Exception as e:
            raise RuntimeError(f"OpenAI API Error: {e}")