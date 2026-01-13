import time

from chains.business_chain import BusinessChain


class AgentExecutor:
    def __init__(self, tone : str = "professional", depth : str = "high"):
        self.tone = tone
        self.depth = depth

    async def run_extreme(self, business_task: str) -> dict:
        
        print("here in executor")
        
        yield {
            "type": "log",
            "content": {
                "step": "START",
                "message": f"Agent started with tone: {self.tone} and depth: {self.depth}",
                "timestamp": time.time()
            }
        }

        yield {
            "type": "log",
            "content": {
                "step": "EXECUTION",
                "message": "Running Business Chain...",
                "timestamp": time.time()
            }
        }
        
        chain = BusinessChain(tone=self.tone)
        result = chain.run(business_task)
        
        yield {
            "type": "log",
            "content": {
                "step": "DONE",
                "message": "Task Completed.",
                "timestamp": time.time()
            }
        }
        
        
        yield {
            "type": "result",
            "content": {
                "business_overview" : result 
            }
        }