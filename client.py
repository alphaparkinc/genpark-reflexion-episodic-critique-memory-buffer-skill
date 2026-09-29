"""Reflexion Episodic Critique Memory Buffer.
100% Python Standard Library.
"""

class ReflexionBuffer:
    """Accumulates episodic failure reflections and self-correcting plans across trials."""
    def __init__(self, max_trials=5):
        self.max_trials = max_trials
        self.episodes = []

    def record_trial(self, trial_id: int, trajectory: list, outcome: bool, critique: str, corrective_plan: str):
        record = {
            "trial_id": trial_id,
            "trajectory": trajectory,
            "success": outcome,
            "critique": critique,
            "corrective_plan": corrective_plan
        }
        self.episodes.append(record)
        if len(self.episodes) > self.max_trials:
            self.episodes.pop(0)

    def get_context_memory(self) -> str:
        lines = []
        for ep in self.episodes:
            status = "PASS" if ep["success"] else "FAIL"
            lines.append(f"Trial {ep['trial_id']} [{status}]: Critique: {ep['critique']} -> Plan: {ep['corrective_plan']}")
        return "\n".join(lines)
