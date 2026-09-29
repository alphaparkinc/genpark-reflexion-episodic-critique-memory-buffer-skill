import sys
import json
from client import ReflexionBuffer

buf = ReflexionBuffer()

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-reflexion-episodic-critique-memory-buffer-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "record_trial_critique",
                        "description": "Records trial trajectory outcome and self-critique in Reflexion buffer",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "trial_id": {"type": "integer"},
                                "trajectory": {"type": "array", "items": {"type": "string"}},
                                "outcome": {"type": "boolean"},
                                "critique": {"type": "string"},
                                "corrective_plan": {"type": "string"}
                            },
                            "required": ["trial_id", "outcome", "critique", "corrective_plan"]
                        }
                    },
                    {
                        "name": "get_reflexion_context",
                        "description": "Returns synthesized past failure reflections for prompt conditioning",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "record_trial_critique":
            buf.record_trial(
                args.get("trial_id", 1),
                args.get("trajectory", []),
                args.get("outcome", False),
                args.get("critique", ""),
                args.get("corrective_plan", "")
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": "Recorded"}]}}
        elif name == "get_reflexion_context":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": buf.get_context_memory()}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()
