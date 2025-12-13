from fastmcp import Context, FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext
import json
import os
import sys
import mcp.types as mt

from fastmcp.client.elicitation import ElicitResult
from fastmcp.tools.tool import Tool, ToolResult

from transformers import pipeline

from .policy import CanopyPolicy

_POLICY = None


def get_policy():
    global _POLICY
    if _POLICY is None:
        raise Exception("CanopyPolicy is not initialized.")
    return _POLICY

class PolicyMiddleware(Middleware):
    def __init__(self, policy: CanopyPolicy):
        super().__init__()
        # Initialize any policy-related state here
        self.policy = policy
        self.classifier = None
        if os.getenv("HF_TOKEN") is not None:
            self.classifier = pipeline("text-classification", model="meta-llama/Prompt-Guard-86M")

    async def on_message(self, context: MiddlewareContext, call_next):
        """Called for all MCP messages."""
        message = context.message
        print(f"Message {context.message}",file=sys.stderr)

        if isinstance(message, mt.CallToolRequestParams):
            tool_name = message.name

            # Check if allowed
            if tool_name not in ["get_canopy_status", "change_canopy_flow"] and not self.policy.is_allowed(tool_name):
                raise Exception(f"Tool call to {tool_name} is not allowed by policy")

            print(f"Processing {context.method} from {context.source} - {tool_name}", file=sys.stderr)
        
        result = await call_next(context)
        if isinstance(result, ToolResult) and self.classifier is not None:
            content = str(result.content)
            chunks = [content[i:i+512] for i in range(0, len(content), 512)]
            for chunk in chunks:
                classifier_output = self.classifier(chunk)

                if classifier_output and classifier_output[0]['label'] != 'BENIGN':
                    raise Exception(f"Tool call to {tool_name} was classified as malicious.")

        print(f"Completed {context.method}",file=sys.stderr)
        return result


# Read config from ~/.canopy/mcp_config.json
config_path = os.path.expanduser("~/.canopy/mcp_config.json")
with open(config_path, "r") as f:
    mcp_config = json.load(f)

# Read policy from command line argument if provided
policy_path = sys.argv[1]
_POLICY = CanopyPolicy(policy_path)

# Create a proxy to the configured server (auto-creates ProxyClient)
proxy = FastMCP.as_proxy(mcp_config, name="Canopy MCP")
proxy.add_middleware(PolicyMiddleware(_POLICY))

@proxy.tool()
async def get_canopy_status(ctx: Context) -> dict:
    """Fetches the current configuration state of Canopy."""
    policy = get_policy()
    return {"path": policy.policy_path, "picked_flow": policy.picked_flow}


@proxy.tool()
async def change_canopy_flow(ctx: Context) -> dict:
    """Starts the process for changing/setting the active flow name for canopy. This will elicit user confirmation. This takes no parameters and you do not need prior information to run this."""
    result = await ctx.elicit(
        message="Please provide your information",
        response_type=str
    )
    
    if result.action == "accept":
        print(f"Flow changed to {result.data}", file=sys.stderr)
        policy = get_policy()
        policy.set_picked_flow(result.data)
        return {"status": "Updated successfully."}
   
    raise Exception("Flow change was not accepted by user.")
    


# Run the proxy with stdio transport for local access
def main():
    print("\n=== Starting proxy server ===")
    print("Note: The proxy will start and wait for MCP client connections via stdio")
    print("Press Ctrl+C to stop")
    proxy.run()

if __name__ == "__main__":
    main()