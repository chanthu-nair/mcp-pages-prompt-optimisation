
This project demonstrates an optimized prompt-based system for structured problem solving using a Math Agent that leverages step-by-step reasoning and function-based tool usage.
🔍 Objective

The goal of this project is to build and evaluate a structured prompt system that enables a language model to:

    Perform math and logic operations using external tools.

    Reason explicitly in natural language before invoking tools.

    Separate reasoning, computation, and final answer generation.

    Handle uncertainty and ambiguous inputs with safe fallbacks.

    Maintain traceability through internal self-checks and categorized reasoning types.


🧠 Prompt Structure

Each prompt must guide the agent to:

    Start with REASONING: Explain the logic behind each decision in plain English.

    Use FUNCTION_CALLS only after reasoning and only one at a time.

    Avoid duplicate tool calls with identical parameters.

    Return FINAL_ANSWER only after all reasoning and calculations are complete.

    Handle errors or ambiguities gracefully using ERROR.

📦 Response Format

{
  "reasoning": "Explain why this tool or step is necessary",
  "reasoning_type": "e.g. arithmetic, lookup, planning, error_handling",
  "action": "FUNCTION_CALL: tool_name|input_values",
  "self_check": "Verify that the tool is being used correctly and that the expected output makes sense"
}
