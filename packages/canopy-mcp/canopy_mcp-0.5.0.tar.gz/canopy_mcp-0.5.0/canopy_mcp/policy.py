
import re
import sys
import tomllib


class CanopyPolicy():
    def __init__(self, policy_path: str):
        self.policy_path = policy_path
        self.policy = self.load_policy(policy_path)
        self.picked_flow = None
        self.seen_allowed_flows = set()

    def set_picked_flow(self, flow_name: str):
        self.picked_flow = flow_name

    def load_policy(self, path: str) -> dict:
        with open(path, "rb") as f:
            return tomllib.load(f)

    def is_allowed(self, tool_call: str) -> bool:
        self.policy = self.load_policy(self.policy_path)
        picked_flow = self.picked_flow or "default"

        flows = self.policy.get("flows", {})
        for _flow_name, flow in flows.items():
            if picked_flow and picked_flow != _flow_name:
                continue

            allowed_calls = flow.get("allowed_calls", [])
            allowed_flows = flow.get("allowed_flows", [])
            no_more_than_count = flow.get("no_more_than_count", 0)

            if len(allowed_flows) > 0:
                return self._is_in_allowed_flow_policy(allowed_flows, tool_call, no_more_than_count)
            else:
                if not flow.get("disabled", False):
                    allowed = False
                    for allowed_call in allowed_calls:
                        try:
                            regex_call = re.compile(allowed_call)
                            if regex_call.fullmatch(tool_call):
                                allowed = True
                                break
                        except re.error as e:
                            raise ValueError(f"Invalid regex in policy for allowed_call: {allowed_call}") from e
                    
                    if allowed:
                        return True
                
        return False
    

    def _is_in_allowed_flow_policy(self, allowed_flows: list, tool_call: str, no_more_than_count: int) -> bool:
        # First, we need to figure out which of the allowed flows this tool_call belongs in.
        # (Which could be several)
        flows = self.policy.get("flows", {})
        found_at_least_one = False
        for flow_name, flow in flows.items():
            if flow_name in allowed_flows:
                allowed_calls = flow.get("allowed_calls", [])
                for allowed_call in allowed_calls:
                    regex_call = re.compile(allowed_call)
                    if regex_call.fullmatch(tool_call):
                        self.seen_allowed_flows.add(flow_name)
                        print(f"Tool call {tool_call} matched allowed flow {flow_name}", file=sys.stderr)
                        found_at_least_one = True

        if not found_at_least_one:
            return False

        # Now check how many allowed flows have been seen, if specified.
        if no_more_than_count > 0:
            if len(self.seen_allowed_flows) > no_more_than_count:
                return False

        return True
