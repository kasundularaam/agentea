from src.application.agents.core.agent import Agent, AgentContext


class HelpfulAgent(Agent):
    NAME = "helpful_agent"

    def __init__(self, ctx: AgentContext,  # order_repo: OrderRepo
                 ):
        super().__init__(ctx)
        """     
        # Define function strictly for this instance
        # def get_order(order_id: int):
        #    return self.order_repo.get(order_id=order_id)

        # self.TOOLS = (get_order,)
        """
