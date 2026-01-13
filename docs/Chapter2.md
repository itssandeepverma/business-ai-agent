# Chapter 2: End-to-End Agent Flow

## Core components
- `config.py`: loads `ANTHROPIC_API_KEY`/`CLAUDE_API_KEY`, chooses Anthropic model via `ANTHROPIC_MODEL` or defaults to a preference list, and exposes `PROMPTS_DIR`.
- `prompts/system_prompt.txt` & `prompts/business_prompt.txt`: system/user instructions stitched together for the LLM; the business prompt enforces a fixed JSON shape.
- `schemas/output_schema.py`: `BusinessOverview` Pydantic model (summary, primary_target_audience, core_pain_point, unique_value_proposition, not_a_priority) used for structured output validation.
- `chains/business_chain.py`: builds the LangChain pipeline, loads prompts, configures the Anthropic chat model, and enforces structured JSON via `with_structured_output(BusinessOverview)`. Falls back through configured model candidates if one is unavailable.
- `agent/executor.py`: orchestrates a run, yielding streaming log events and the final structured result.

## Request/response flow
1) **UI → API**: `ui/index.html` collects `business_task`, `tone`, `depth` and posts `FormData` to `POST /run-agent` using `fetch` with streaming response handling.
2) **API endpoint**: `api/router.py` defines `/run-agent`, instantiates `AgentExecutor(tone, depth)`, and returns a `StreamingResponse` that emits server-sent events (SSE) as the executor yields data.
3) **Executor**: `AgentExecutor.run_extreme` (async generator) yields:
   - `log` events for START and EXECUTION steps.
   - After invoking the chain, a `result` event containing the structured business output.
4) **Chain**: `BusinessChain.run` assembles prompts, tries each candidate model in order, and invokes the Anthropic chat model with structured output bound to `BusinessOverview`. It appends the requested tone to the user task before calling the chain.
5) **LLM**: `langchain_anthropic.ChatAnthropic` handles the API call; `with_structured_output` coerces the response into the Pydantic model, raising if the shape is invalid.
6) **Response back to UI**: SSE chunks are parsed in `ui/index.html`; `log` events update the console, `result` events call `renderData` to populate the Strategy tab (summary/target/UVP/pain point/not-a-priority). Other tabs are currently placeholders until the backend returns matching fields.

## Data contracts
- Input (UI → API): form fields `business_task` (text), `tone` (e.g., professional/friendly/premium), `depth` (quick/normal/deep; presently unused in backend logic).
- Output (API → UI): `business_overview` object matching `BusinessOverview`. UI also expects `marketing_strategy`, `email_campaign`, and `task_breakdown`, but these are not yet produced by the chain, so they render placeholders.

## Execution quickstart (recap)
- Run the app: `uvicorn main:app --reload` (or `python main.py`).
- Ensure `.env` has `ANTHROPIC_API_KEY` (or `CLAUDE_API_KEY`); optionally set `ANTHROPIC_MODEL` to override the model choice.
- Open `http://localhost:8000/app`, submit a goal, and watch logs/results stream live.

## Extension notes
- To add more outputs (marketing strategy, emails, tasks), extend `schemas/output_schema.py` with new models, adjust `prompts/business_prompt.txt` to request those fields, and update `BusinessChain` to use a composite schema.
- If using a different Anthropic model, set `ANTHROPIC_MODEL`; the chain will try that first and fall back to the bundled defaults.
