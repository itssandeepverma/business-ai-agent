## Request Flow (Submit Button → Results)

```
User clicks "Analyze & Generate Plan"
        |
        v
ui/index.html (form submit handler)
  - builds FormData: business_task, tone, depth
  - calls streamAgent(fetch POST /run-agent)
        |
        v
POST /run-agent (api/router.py)
  - creates AgentExecutor(tone, depth)
  - returns StreamingResponse(executor.run_extreme)
        |
        v
AgentExecutor.run_extreme (agent/executor.py)
  -> forwards to run_stream
        |
        v
AgentExecutor.run_stream
  - create_log helper yields log events
  - planner = ExecutionPlanner(tone, depth)
  - plan = planner.generate_plan(business_task)  [thread offloaded]
  - steps = plan["steps"]
  - for each step:
      business_analysis -> BusinessChain.run(business_task)
      marketing_strategy -> MarketingChain.run(business_task)
  - validate FinalOutput(business_overview?, marketing_strategy?)
  - yield final result event
        |
        v
UI streamAgent reader
  - on log event -> addLog
  - on result event -> renderData (updates tabs)
```

## Function Inputs/Outputs

| Function | Location | Input | Output |
| --- | --- | --- | --- |
| `streamAgent` | `ui/index.html` | FormData: `business_task`, `tone`, `depth` | Processes SSE-style chunks; calls `addLog` / `renderData` |
| `run_agent` | `api/router.py` | Form fields `business_task`, `tone`, `depth` | `StreamingResponse` yielding `log` and final `result` events |
| `AgentExecutor.run_extreme` | `agent/executor.py` | `business_task` | Async generator proxy to `run_stream` |
| `AgentExecutor.run_stream` | `agent/executor.py` | `business_task` | Streams `log` events; executes planner/chains; final `result` dict |
| `ExecutionPlanner.generate_plan` | `agent/planner.py` | `business_task` (+ tone/depth context in prompt) | `{"steps": [ ... ]}` |
| `BusinessChain.run` | `chains/business_chain.py` | `business_task` (tone appended) | `BusinessOverview` dict |
| `MarketingChain.run` | `chains/marketing_chain.py` | `business_task` (tone/depth context) | `MarketingStrategy` dict |
| `renderData` | `ui/index.html` | Final `result` content | Updates Strategy/Marketing/Email/Tasks tabs |
