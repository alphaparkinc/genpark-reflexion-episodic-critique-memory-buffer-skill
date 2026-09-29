# genpark-reflexion-episodic-critique-memory-buffer-skill

Reflexion episodic failure memory buffer accumulating self-critiques and trial corrective plans across autonomous trials.

## Architecture

```mermaid
flowchart TD
    Trial[Trial Execution Failure] --> Critique[Evaluator / Self-Critique]
    Critique --> Buffer[Reflexion Episodic Buffer]
    Buffer --> NextTrial[Condition Next Trial Prompt]
```

## Features
- **Episodic Retention**: Maintains sliding window of past trial reflections.
- **Zero Dependencies**: 100% Python Standard Library.
