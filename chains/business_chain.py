from langchain_anthropic import ChatAnthropic
from langchain_core.prompts.chat import ChatPromptTemplate

from config import CLAUDE_API_KEY, MODEL_NAME, PROMPTS_DIR
from schemas.output_schema import BusinessOverview


class BusinessChain:
    def __init__(self, tone: str = "professional"):
        self.tone = tone

    def _load_prompts(self) -> tuple[str, str]:
        prompt_path = f"{PROMPTS_DIR}/business_prompt.txt"
        system_prompt_path = f"{PROMPTS_DIR}/system_prompt.txt"

        print(prompt_path)

        with open(prompt_path, 'r') as file:
            user_prompt_text = file.read()

        with open(system_prompt_path, 'r') as file:
            system_prompt_text = file.read()

        return system_prompt_text, user_prompt_text

    def _build_chain(self, system_prompt_text: str, user_prompt_text: str, model: str):
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt_text),
            ("user", user_prompt_text)
        ])

        llm = ChatAnthropic(
            model=model,
            temperature=0.3,
            api_key=CLAUDE_API_KEY
        )

        return prompt | llm.with_structured_output(BusinessOverview)

    def run(self, business_task: str) -> dict:
        system_prompt_text, user_prompt_text = self._load_prompts()
        enhanced_task = f"{business_task}\n\nPlease write in a {self.tone} tone."

        try:
            chain = self._build_chain(system_prompt_text, user_prompt_text, MODEL_NAME)
            print(f"[CHAIN] Running business chain with Tone: {self.tone} using model: {MODEL_NAME}")
            result = chain.invoke({"business_task": enhanced_task})
            print(f"result : {result}")
            return result.model_dump()
        except Exception as exc:
            raise RuntimeError(f"Anthropic model {MODEL_NAME} failed") from exc
