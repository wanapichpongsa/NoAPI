
### Iteration 1

1. Not accessing attachment properly (maybe make attachment seperate user message)
2. Feel like longer, uncleaned conversations makes the agent hallucinate more -> Have user clean, then instantiate new 'expert'
3. Many edge cases e.g., 1 float = balance, 2 floats = in/out && balance, no date = previous date confuse the agent.

**Solution**
1. Once attachment properly filtered, cache the filtered result and only use that as the clean context.
2. Recursively do so for every edge case until done!

### Iteration 2
1. Recursive RAGs are cleaner
2. Still facing a lot of query misintrepretation from the agent.
3. LLM does not understand tabular logic from text:
e.g.,
From:
```
Date, paymenttype, details, outflow, inflow, balance
01 Jan 2024, STORENAME PAYMENTTYPE URL FLOAT FLOAT
```
```python
[{
  "date": "A",
  "payment type and details": "STORENAME PAYMENTTYPE URL FLOAT FLOAT"
}]
```
**Solution**
1. Have Cleaner, Extractor and Transform Agent.
e.g., Cleaner outputs `columns` and `rows` variables, fed into Extractor.