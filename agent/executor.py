import asyncio
import time

from agent.planner import ExecutionPlanner
from chains.business_chain import BusinessChain
from chains.marketing_chain import MarketingChain
from schemas.output_schema import FinalOutput


class AgentExecutor:
    def __init__(self, tone : str = "professional", depth : str = "high"):
        self.tone = tone
        self.depth = depth


    async def run_stream(self, business_task: str):

        def create_log(step, message):
            return {
                "type": "log",
                "content": {
                    "step": step,
                    "message": message,
                    "timestamp": time.time()
                }
            }

        # 1.Planning
        planner = ExecutionPlanner(tone=self.tone, depth=self.depth)

        plan = await asyncio.to_thread(planner.generate_plan, business_task)

        steps = plan.get("steps", [])

        yield create_log("PLANNING", f"Decided steps: {steps}")

        # 2. Execution
        final_output_data = {}

        # Business Chain
        if "business_analysis" in steps:
            yield create_log("EXECUTION", "Starting Business Chain...")

            chain = BusinessChain(tone=self.tone)
            final_output_data["business_overview"] = await asyncio.to_thread(chain.run, business_task)
        
        # Marketing Chain
        if "marketing_strategy" in steps:
            yield create_log("EXECUTION", "Starting Marketing Chain...")

            chain = MarketingChain(tone=self.tone)
            final_output_data["marketing_strategy"] = await asyncio.to_thread(chain.run, business_task)


        # Review - TODO

        # 4. Validation
        try:
            final_output_obj = FinalOutput(**final_output_data)

            validated_data = final_output_obj.model_dump()

            yield create_log("SUCCESS", "Final output validated successfully.")

            yield {
                "type": "result",
                "content": validated_data
            }

        except Exception as e:
            yield create_log("ERROR", f"Validation failed: {str(e)}")
            raise e

    async def run_extreme(self, business_task: str):
        """Compatibility wrapper for legacy callers."""
        async for event in self.run_stream(business_task):
            yield event
