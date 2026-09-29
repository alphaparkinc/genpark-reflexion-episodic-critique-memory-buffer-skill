from client import ReflexionBuffer

buf = ReflexionBuffer()
buf.record_trial(1, ["parse", "eval"], False, "Forgot edge cases", "Add zero-check")
print("Reflexion Prompt Context:\n", buf.get_context_memory())
