from langchain_anthropic import ChatAnthropic
from langchain_core.prompts.chat import ChatPromptTemplate

from config import CLAUDE_API_KEY, MODEL_FALLBACKS, MODEL_NAME, PROMPTS_DIR
from schemas.output_schema import BusinessOverview


class BusinessChain:
    def __init__(self, tone: str = "professional"):
        self.tone = tone
        # Always try the configured model first, then fall back to older ones if unavailable.
        self.model_candidates = [MODEL_NAME] + [
            model for model in MODEL_FALLBACKS if model != MODEL_NAME
        ]

    @staticmethod
    def _is_model_not_found_error(exc: Exception) -> bool:
        message = str(exc).lower()
        return "not_found_error" in message or ("model:" in message and "not found" in message)

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

        last_error = None
        for model in self.model_candidates:
            print("Model Name", model)
            try:
                chain = self._build_chain(system_prompt_text, user_prompt_text, model)
                print(f"[CHAIN] Running business chain with Tone: {self.tone} using model: {model}")
                result = chain.invoke({"business_task": enhanced_task})
                print(f"result : {result}")
                return result.model_dump()
            except Exception as exc:
                last_error = exc
                if self._is_model_not_found_error(exc):
                    print(f"[CHAIN] Model {model} unavailable ({exc}); trying fallback.")
                    continue
                raise

        raise RuntimeError(f"All configured Anthropic models failed ({', '.join(self.model_candidates)}). Last error: {last_error}")
