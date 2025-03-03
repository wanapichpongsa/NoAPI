
### RAG Iteration 1

1. Not accessing attachment properly (maybe make attachment seperate user message)
2. Feel like longer, uncleaned conversations makes the agent hallucinate more -> Have user clean, then instantiate new 'expert'
3. Many edge cases e.g., 1 float = balance, 2 floats = in/out && balance, no date = previous date confuse the agent.

**Solution**
1. Once attachment properly filtered, cache the filtered result and only use that as the clean context.
2. Recursively do so for every edge case until done!