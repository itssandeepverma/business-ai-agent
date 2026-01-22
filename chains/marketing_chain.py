import os

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

from config import CLAUDE_API_KEY, MODEL_NAME, PROMPTS_DIR
from schemas.output_schema import MarketingStrategy


class MarketingChain:
    def __init__(self, tone: str = "professional", depth: str = "normal"):
        self.tone = tone
        self.depth = depth

        self.llm = ChatAnthropic(
            model=MODEL_NAME,
            temperature=0.3,
            api_key=CLAUDE_API_KEY
        )

    def generate_strategy(self, business_task: str) -> dict:

        prompt_path = os.path.join(PROMPTS_DIR, 'marketing_prompt.txt')
        system_prompt_path = os.path.join(PROMPTS_DIR, 'system_prompt.txt')

        with open(prompt_path, 'r') as f:
            user_prompt_text = f.read()

        with open(system_prompt_path, 'r') as f:
            system_prompt_text = f.read()

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            ("user", user_prompt_text)
        ])

        marketing_chain = prompt | self.llm.with_structured_output(MarketingStrategy)

        print(f"[MARKETING] Drafting strategy with {self.depth} depth...")

        context_enchanced_task = f"{business_task}\n\n[Context: Tone={self.tone}, Depth={self.depth}]."

        result = marketing_chain.invoke({"business_task": context_enchanced_task})

        return result.model_dump()

    def run(self, business_task: str) -> dict:
        """Compatibility alias matching other chain interfaces."""
        return self.generate_strategy(business_task)
