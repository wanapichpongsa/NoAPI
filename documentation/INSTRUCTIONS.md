# NoAPI Documentation (In Progress)

## AI Models

##### Deepseek-R1 RAM Usage
- deepseek-r1:1.5b ≈ 1.1GB
- deepseek-r1:7b ≈ 4.7GB
- deepseek-r1:8b ≈ 4.9GB
- deepseek-r1:14b ≈ 9.0GB
- deepseek-r1:32b ≈ 20.0GB
- deepseek-r1:70b ≈ 43.0GB
- deepseek-r1:678b ≈ 404GB

recommended to run models with cpu only flag:

```bash
ollama run --verbose (modelname) --cpu
```

### Debugging

If you have unwanted dependencies in your __pycache__ folder, you can delete it with:

```bash
find . -type d -name "__pycache__" -exec rm -r {} +
```

### Desired Export Format

See example_structure.xlsx for the desired export format.

### Deep Questions
1. What data manipulation function of PyPDF2 is inferior to pdfplumber?
2. Why are RAGs better for scraping websites into LLM-friendly formats? (Since there're confusing document structure to LLMs) 
3. I wonder why _B param models take up _GB of VRAM?
4. Pretraining on _T tokens outputs what _B param model?

**Answers**
1. None
2. RAGs are situational, not permanently learning content like retraining [Dave's Garage](https://www.youtube.com/watch?v=fFgyOucIFuk)

### Deep Thoughts
**The Truth About Contextual Window Bugs**
LLMs are just like us humans. They get confused when there's too much information!


**Are University Degrees worth it?**
Humans learn by Extracting, Transforming and Loading data.

At its rawest form, data can be observed from primitive entities within our environment (e.g., Things fall down, the sky is blue, etc.)

The curriculum that we learn in school (e.g., Newton's laws in physics) are examples of transformed data.

The tragic aspect of formal education is how excessive the content students are forced to learn as it is completely unrelated to the knowledge they actually need to use when assessed.

**Maybe Exclude**
I remember reading Alan Turing's "Can Machines Think?" paper and I could only extrapolate very basic ideas from the paper because of how verbose it was.

I then started to feel bad, thinking: "Maybe I'm just not smart enough"

Turing machines are "infinite deterministic machines"

Ex-Machina made more sense to me, and it was all the ideas I really needed to move forward.

**What is Intelligence?**
