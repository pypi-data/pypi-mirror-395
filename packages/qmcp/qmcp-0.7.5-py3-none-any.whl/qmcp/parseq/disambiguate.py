from .callLLM import call_llm
import os

# Read the q operators documentation from package directory
package_dir = os.path.dirname(__file__)
q_ops_file = os.path.join(package_dir, 'q_operators.md')
with open(q_ops_file, 'r') as f:
    q_ops_content = f.read()


def create_disambiguation_prompt(code_string: str, q_operators_content: str) -> str:
    """Create a prompt for LLM to disambiguate q operators in code"""
    prompt = f"""TASK: Disambiguate generic Q operator function names to specific semantic overloads based on argument patterns and usage context.

CRITICAL OUTPUT FORMAT: You must output ONLY the Python code with comments. Do NOT include any explanatory text, analysis, or reasoning outside the code. Start your response immediately with the first line of code.

DISAMBIGUATION REQUIREMENTS:
1. Replace all generic function names with specific overloads based on argument patterns
2. Detect and wrap partial applications with partial() where needed
3. Add brief explanatory comments starting with # for each disambiguated operation

MANDATORY FUNCTION DISAMBIGUATIONS:
- Every instance of slash() → converge(), do(), while(), or reduce() based on usage pattern
- Every instance of bang() → dict_create(), enkey(), unkey(), etc. based on argument types  
- Every instance of hash() → take(), set_attribute() based on argument patterns
- Every instance of query() → find(), roll(), select_exec(), etc. based on arity and types
- All generic function names must be replaced with specific semantic names

PARTIAL APPLICATION HANDLING:
- When function calls have insufficient arguments, wrap with partial()
- Comment format: "# Partial application: takes arity-N function, returns arity-M function"
- Focus on what the resulting partial function does, not what was "missing"

FUNCTIONAL PATTERN RULES:
- converge/do/while/reduce return functions that are called separately  
- Two-step pattern: temp1 = converge(f) creates function, then temp2 = temp1(x) calls it
- Document the semantic meaning of each step

SYNTAX PRESERVATION:
- Function calls have parentheses: `func()`, `func(arg)`, `func(a, b)`
- Variable assignments without parentheses assign function objects: `result = func1`
- Only apply partial() analysis to expressions WITH parentheses (actual function calls)
- Never modify bare function names in assignments (no parentheses = function object assignment)

COMMENT EXAMPLES:
- `temp4 = partial(func1, x)` → `# Partial application: takes arity-2 function, returns arity-1 function`
- `temp5 = converge(temp4)` → `# Converge: repeatedly applies function until result stabilizes`
- `temp2 = dict_create(keys, values)` → `# Dict creation: creates dictionary from key-value lists`

Input code to disambiguate:
```
{code_string}
```

Disambiguation guide:
{q_operators_content}"""
    return prompt

def disambiguate_step(code: str) -> str:
    
    # Create the disambiguation prompt
    prompt = create_disambiguation_prompt(code, q_ops_content)
    # Ask LLM to disambiguate
    disambiguated = call_llm(prompt)
    
    # Remove markdown code fences if present
    lines = disambiguated.strip().split('\n')
    if lines[0].startswith('```'):
        lines = lines[1:]
    if lines[-1].startswith('```'):
        lines = lines[:-1]
    
    return '\n'.join(lines)

