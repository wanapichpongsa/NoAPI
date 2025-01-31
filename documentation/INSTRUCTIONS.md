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
ollama run (modelname) --cpu
```


### Debugging

If you have unwanted dependencies in your __pycache__ folder, you can delete it with:

```bash
find . -type d -name "__pycache__" -exec rm -r {} +
```

### Desired Export Format

See example_structure.xlsx for the desired export format.

### Deep Questions
1. I wonder why _B param models take up _GB of VRAM?
2. Pretraining on _T tokens outputs what _B param model?
