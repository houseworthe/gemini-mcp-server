# Maximizing Gemini Context Usage in Claude

## Best Practices for Large Context

### 1. **Use the `gemini_analyze_large` tool**
This is optimized for massive contexts (up to 1M tokens ~ 750k words):

```
"Claude, use gemini_analyze_large to analyze this entire codebase and find security vulnerabilities"
```

### 2. **Aggregate Multiple Files**
Claude can read multiple files and send them all to Gemini at once:

```
"Read all files in src/ and have Gemini review the architecture"
```

### 3. **Leverage Claude's Pre-Processing**
Claude can:
- Read and combine multiple files
- Filter relevant content
- Structure the data before sending to Gemini

Example workflow:
```
1. Claude reads 50 files from your project
2. Claude identifies the 30 most relevant ones
3. Claude sends all 30 files (200k tokens) to Gemini in one request
4. Gemini analyzes with full context
```

### 4. **Specific Use Cases**

#### Full Codebase Analysis
```
"Read all Python files in this project and ask Gemini to:
- Identify code smells
- Suggest architectural improvements
- Find security issues"
```

#### Large Document Analysis
```
"Read these 10 PDF files (converted to text) and have Gemini create a comprehensive summary"
```

#### Log Analysis
```
"Read the last 10,000 lines of logs and have Gemini identify patterns and anomalies"
```

### 5. **Context-Preserving Conversations**
When you need to maintain context across multiple Gemini calls:

```
"First, have Gemini analyze the database schema (file1.sql).
Then, based on that analysis, have Gemini review the API endpoints (api/*.py) for consistency"
```

### 6. **Optimal Chunk Sizes**
- **Small tasks**: Use `ask_gemini` (up to 50k tokens)
- **Code reviews**: Use `gemini_code_review` (up to 200k tokens)
- **Large analysis**: Use `gemini_analyze_large` (up to 1M tokens)

### 7. **Tips for Maximum Efficiency**

1. **Pre-filter with Claude**: Let Claude identify relevant files first
2. **Combine related content**: Send entire modules/packages together
3. **Use structured prompts**: Help Gemini understand the context structure
4. **Batch related questions**: Ask multiple questions in one request

### Example: Analyzing an Entire Project

```
"Claude, please:
1. Read all .py files in the project
2. Create a single string with all the code
3. Use gemini_analyze_large to:
   - Create a dependency graph
   - Identify dead code
   - Suggest refactoring opportunities
   - Find potential bugs
   - Review security practices"
```

This would send potentially 500k+ tokens to Gemini in a single request, maintaining full context.