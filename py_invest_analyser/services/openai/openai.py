from openai import OpenAI

from config.settings import API_KEY_OPENAI


class OpenaiService:
    def __init__(self):
        client = OpenAI(
            api_key=API_KEY_OPENAI
        )

        self.client_openai = client

    def get_answer(self, link: str) -> str:
        try:
            prompt = (
                f""" 
                Analise o seguinte texto: {link}

                Você é um investidor que deseja investir em um fundo imobiliário 
                e precisa analisar este texto para decidir se irá investir ou não.
                Gere um resumo com as informações mais importantes do texto 
                """
            )

            chat_completion = self.client_openai.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=750,
                n=1,
                stop=None,
                temperature=0.17,
                frequency_penalty=0.2,
                presence_penalty=0.0
            )

            return chat_completion.choices[0].text.strip()

        except Exception as e:
            raise e