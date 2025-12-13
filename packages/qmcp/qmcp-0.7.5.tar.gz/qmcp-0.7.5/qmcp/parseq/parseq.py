from qmcp.qlib import connect_to_q
from typing import List as ListType, Union, Any, Tuple
from .disambiguate import disambiguate_step
# from callLLM import call_llm
import os

package_dir = os.path.dirname(__file__)
parseq_q_file = os.path.join(package_dir, 'parseq_ns.q')
with open(parseq_q_file, 'r') as f:
    parseq_q_code = f.read()

def quote(x):
    escaped = str(x).replace('\\', '\\\\').replace('"', '\\"')
    return f'"{escaped}"'

glyph_map = {
    '@': 'at', '!': 'bang', '::': 'colon_colon',
    '.': 'dot', '$': 'dollar', '#': 'hash', '?': 'query',
    '_': 'underscore', ',': 'comma', '/': 'slash',
    '\\': 'backslash'
    }


# AST Node classes
class ASTNode:
    def __init__(self, node_type, value=None, children=None, eager=False, is_inside_dict = False):
        self.node_type = node_type
        self.value = value
        self.children = children or []
        self.eager = eager
        self.is_inside_dict = is_inside_dict

# Helper functions
def print_node_tree(node, indent=0):
    """Print AST node tree with node_type and eager status"""
    prefix = "  " * indent
    eager_status = f" (eager={node.eager})" if hasattr(node, 'eager') else ""
    node_type_status = f" (node_type={node.node_type})" if hasattr(node, 'node_type') else " (NO NODE_TYPE)"
    
    if node.node_type == 'variable':
        print(f"{prefix}Variable: {node.value}{eager_status}{node_type_status}")
    elif node.node_type == 'symbol':
        print(f"{prefix}Symbol: `{node.value}{eager_status}{node_type_status}")
    elif node.node_type == 'integer':
        print(f"{prefix}Integer: {node.value}{eager_status}{node_type_status}")
    elif node.node_type == 'float':
        print(f"{prefix}Float: {node.value}{eager_status}{node_type_status}")
    elif node.node_type == 'boolean':
        print(f"{prefix}Boolean: {node.value}{eager_status}{node_type_status}")
    elif node.node_type == 'string':
        print(f"{prefix}String: {node.value}{eager_status}{node_type_status}")
    elif node.node_type == 'char':
        print(f"{prefix}Char: '{node.value}'{eager_status}{node_type_status}")
    elif node.node_type == 'sequence':
        print(f"{prefix}Sequence{eager_status}{node_type_status}:")
        for i, child in enumerate(node.children):
            print(f"{prefix}  Statement {i}:")
            print_node_tree(child, indent + 2)
    elif node.node_type == 'function':
        print(f"{prefix}Function: {node.value}{eager_status}{node_type_status}")
    elif node.node_type == 'symbol_list':
        print(f"{prefix}SymbolList{eager_status}{node_type_status}:")
        for i, child in enumerate(node.children):
            print_node_tree(child, indent + 1)
    elif node.node_type == 'lambda':
        param_names = getattr(node, 'param_names', [])
        print(f"{prefix}Lambda{eager_status}{node_type_status}:")
        print(f"{prefix}  Params: {param_names}")
        print(f"{prefix}  Body:")
        print_node_tree(node.children[0], indent + 2)
    elif node.node_type == 'list':
        print(f"{prefix}List{eager_status}{node_type_status}:")
        for i, child in enumerate(node.children):
            print(f"{prefix}  [{i}]:")
            print_node_tree(child, indent + 2)
    elif node.node_type == 'dict':
        print(f"{prefix}Dict{eager_status}{node_type_status}:")
        print(f"{prefix}  Keys:")
        print_node_tree(node.children[0], indent + 2)
        print(f"{prefix}  Values:")
        print_node_tree(node.children[1], indent + 2)
    else:
        print(f"{prefix}Unknown ({node.node_type}): {node.value}{eager_status}{node_type_status}")
        if hasattr(node, 'children') and node.children:
            print(f"{prefix}  Children:")
            for i, child in enumerate(node.children):
                print(f"{prefix}    [{i}]:")
                print_node_tree(child, indent + 3)

def inspect_node(node):
    """Inspect a node to understand its structure"""
    print(f"Node type: {node.node_type}")
    print(f"Node value: {node.value}")
    print(f"Node children: {len(node.children) if node.children else 0}")
    if node.children:
        for i, child in enumerate(node.children):
            print(f"  Child {i}: {child.node_type} = {child.value}")
    print(f"Node attributes: {[attr for attr in dir(node) if not attr.startswith('_')]}")
    print(f"Node eager: {node.eager}")
    print()


# Tokenizer
def tokenize(text: str) -> ListType[str]:
    """Tokenize the LISP-like input into a list of tokens"""
    tokens = []
    i = 0
    while i < len(text):
        char = text[i]
        if char.isspace():
            i += 1
        elif char in '[](),{}':
            tokens.append(char)
            i += 1
        elif char == ':':
            # Handle dict syntax like LSymbol[s, t]:
            tokens.append(char)
            i += 1
        else:
            # Read a word/identifier
            start = i
            while i < len(text) and text[i] not in '[](){},:' and not text[i].isspace():
                i += 1
            tokens.append(text[start:i])
    return tokens

# Parser
class Parser:
    def __init__(self, tokens: ListType[str]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> str:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    
    def consume(self) -> str:
        token = self.current_token()
        self.pos += 1
        return token
    
    def parse(self) -> ASTNode:
        """Parse the tokens into an AST"""
        return self.parse_expression()
    
    def parse_expression(self, idx = 0, is_inside_dict=False) -> ASTNode:
        token = self.current_token()
        
        if token == '[':
            return self.parse_list(is_inside_dict)
        elif token == '{':
            return self.parse_dict()
        elif token and token[0].isupper():
            # Type constructor like Symbol[name], Int[5], etc.
            return self.parse_type_constructor()
        else:
            # Simple token - consume it and parse as simple token
            token = self.consume()
            return self.parse_simple_token(token)
    
    def parse_list(self, is_inside_dict) -> ASTNode:
        """Parse a bracketed list [...]"""
        self.consume()  # consume '['
        elements = []
        idx = 0
        while self.current_token() != ']':
            if idx == 1 and not is_inside_dict:
                elements[0].eager = True
            if self.current_token() == ',':
                self.consume()  # skip comma
                continue
            parsed_result = self.parse_expression(idx, is_inside_dict)
            # Handle case where parsing returns symbol_list (needs flattening)
            if parsed_result.node_type == 'symbol_list':
                elements.extend(parsed_result.children)
            else:
                elements.append(parsed_result)
            idx += 1
        
        self.consume()  # consume ']'
        return ASTNode('list', children=elements)
    
    def parse_dict(self) -> ASTNode:
        """Parse a dictionary {...}"""
        self.consume()  # consume '{'
        
        # Parse keys
        keys = self.parse_expression(0, is_inside_dict = True)
        
        if self.current_token() != ':':
            raise ValueError(f"Expected ':' in dict, got {self.current_token()}")
        self.consume()  # consume ':'
        
        # Parse values
        values = self.parse_expression(0, is_inside_dict = True)
        
        # Expect '}'
        if self.current_token() != '}':
            raise ValueError(f"Expected '}}' in dict, got {self.current_token()}")
        self.consume()  # consume '}'
        
        return ASTNode('dict', children=[keys, values])
    
    def parse_type_constructor(self) -> ASTNode:
        """Parse type constructors like Symbol[name], Int[5], Bool[0]"""
        type_name = self.consume()
        
        if self.current_token() != '[':
            # Just a plain identifier
            return ASTNode('string', value=type_name)
        
        self.consume()  # consume '['
        
        if type_name == 'Symbol':
            name = self.consume()
            self.consume()  # consume ']'
            return ASTNode('variable', value=name)
        elif type_name in ['Int', 'Long']:
            value = int(self.consume())
            self.consume()  # consume ']'
            return ASTNode('integer', value=value)
        elif type_name in ['Real', 'Float']:
            value = float(self.consume())
            self.consume()  # consume ']'
            return ASTNode('float', value=value)
        elif type_name == 'Bool':
            value = self.consume() == '1'
            self.consume()  # consume ']'
            return ASTNode('boolean', value=value)
        elif type_name == 'Char':
            char = self.consume()
            self.consume()  # consume ']'
            if char == ';':
                # Special case: semicolon indicates statement sequence
                return ASTNode('sequence', value=';')
            else:
                # Regular character
                return ASTNode('char', value=char)
        elif type_name == 'Builtin':
            func_name = self.consume()
            self.consume()  # consume ']'
            return ASTNode('variable', value=func_name)  # Functions are variables
        elif type_name == 'LSymbol':
            # Parse LSymbol[a, b, c] as a special node containing symbols to be flattened
            symbols = []
            while self.current_token() != ']':
                if self.current_token() == ',':
                    self.consume()  # skip comma
                    continue
                symbols.append(ASTNode('symbol', value=self.consume()))
            self.consume()  # consume ']'
            return ASTNode('symbol_list', children=symbols)
        elif type_name == 'Lambda':
            # Parse Lambda[params, body] - handle params specially
            # Expect '[' for parameter list
            if self.current_token() != '[':
                raise ValueError(f"Expected '[' for Lambda params, got {self.current_token()}")
            self.consume()  # consume '['
            
            # Parse parameter names directly (not as expressions)
            param_names = []
            while self.current_token() != ']':
                if self.current_token() == ',':
                    self.consume()  # skip comma
                    continue
                param_names.append(self.consume())  # Just take the parameter name as string
            self.consume()  # consume ']'
            
            if self.current_token() != ',':
                raise ValueError(f"Expected ',' in Lambda, got {self.current_token()}")
            self.consume()  # consume ','
            
            body = self.parse_expression()
            self.consume()  # consume ']'
            
            # Create lambda node with param_names as a property
            lambda_node = ASTNode('lambda', children=[body])
            lambda_node.param_names = param_names  # Store params as property
            return lambda_node
        elif type_name.startswith('L') and len(type_name) > 1:
            # Parse L{type} as a typed list (LSymbol, LLong, LChar, etc.)
            base_type = type_name[1:]  # Remove 'L' prefix
            elements = []
            while self.current_token() != ']':
                if self.current_token() == ',':
                    self.consume()  # skip comma
                    continue
                token = self.consume()
                
                # Convert based on base type
                if base_type == 'Symbol':
                    elements.append(ASTNode('symbol', value=token))
                elif base_type in ['Long', 'Int']:
                    elements.append(ASTNode('integer', value=int(token)))
                elif base_type in ['Real', 'Float']:
                    elements.append(ASTNode('float', value=float(token)))
                elif base_type == 'Bool':
                    elements.append(ASTNode('boolean', value=token == '1'))
                elif base_type == 'Char':
                    elements.append(ASTNode('string', value=token))
                else:
                    # Unknown base type, treat as string
                    elements.append(ASTNode('string', value=token))
            
            self.consume()  # consume ']'
            return ASTNode('list', children=elements)
        else:
            # Unknown type, parse contents as string
            content = self.consume()
            self.consume()  # consume ']'
            return ASTNode('string', value=f"{type_name}[{content}]")
    
    def parse_simple_token(self, token: str) -> ASTNode:
        """Parse simple tokens that aren't type constructors"""
        if token.isdigit():
            return ASTNode('integer', value=int(token))
        elif token.replace('.', '').isdigit() and '.' in token:
            return ASTNode('float', value=float(token))
        else:
            return ASTNode('string', value=token)

# AST Flattener - converts nested calls to step-by-step assignments
class Flattener:
    def flatten(self, node: ASTNode) -> tuple[ListType[str], str]:
        self.temp_counter = 0
        self.func_counter = 0
        return self.flatten_ast(node)
    def flatten_ast(self, node: ASTNode, **kwargs) -> tuple[ListType[str], str]:
        """
        Flatten nested function calls into step-by-step assignments.
        Returns (statements, final_expression)
        """
        statements = []
        
        if node.node_type == 'variable':
            # Replace glyphs with readable names (since functions are variables)
            var_name = glyph_map.get(node.value, node.value)
            return statements, var_name
        elif node.node_type == 'symbol':
            return statements, f"`{node.value}"  # Only symbols get backticks
        elif node.node_type == 'integer':
            return statements, str(node.value)
        elif node.node_type == 'float':
            value_str = str(node.value)
            if '.' not in value_str:
                value_str += '.0'
            return statements, value_str
        elif node.node_type == 'boolean':
            return statements, 'True' if node.value else 'False'
        elif node.node_type == 'string':
            return statements, node.value
        elif node.node_type == 'char':
            return statements, f"'{node.value}'"
        elif node.node_type == 'function':
            # Replace glyphs with readable names
            func_name = glyph_map.get(node.value, node.value)
            
            # Function nodes should just return their name - arguments are handled at the list level
            return statements, func_name
            
        elif node.node_type == 'list':
            if node.children and node.children[0].node_type == 'sequence':
                # First element is sequence marker: treat as statement sequence
                statements_list = node.children[1:]  # Skip the sequence marker
                for stmt in statements_list:
                    stmt_stmts, stmt_expr = self.flatten_ast(stmt)
                    statements.extend(stmt_stmts)
                # Return the last expression (Q semantics)
                return statements, stmt_expr
            elif node.children and node.children[0].eager:
                # First element is eager: treat as function call
                func_node = node.children[0]
                args = node.children[1:]
                
                # Flatten the function expression first
                func_stmts, func_expr = self.flatten_ast(func_node)
                statements.extend(func_stmts)
                
                # Apply glyph mapping if the function is a simple string
                if func_node.node_type == 'string':
                    func_expr = glyph_map.get(func_expr, func_expr)
                
                # Special handling for assignments: colon with arity 2 (check BEFORE flattening args)
                if func_expr == ':' and len(args) == 2:
                    var_node = args[0]    # Still an AST node
                    value_node = args[1]  # Still an AST node
                    
                    if value_node.node_type == 'lambda':
                        # Handle lambda assignment specially
                        # print(f"DEBUG: Found lambda assignment to {var_node.value}")
                        # print(f"DEBUG: Lambda node details:")
                        # inspect_node(value_node)
                        var_name = var_node.value
                        # Process lambda with custom function name
                        lambda_stmts, lambda_expr = self.flatten_ast(value_node, func_name=var_name)
                        statements.extend(lambda_stmts)
                        # No need for assignment since function is already defined with the right name
                        # Assignments always return None (Q semantics)
                        return statements, None
                    else:
                        # Regular assignment - flatten both sides
                        var_stmts, var_expr = self.flatten_ast(var_node)
                        val_stmts, val_expr = self.flatten_ast(value_node)
                        statements.extend(var_stmts)
                        statements.extend(val_stmts)
                        statements.append(f"{var_expr} = {val_expr}")
                        # Assignments always return None (Q semantics)
                        return statements, None
                
                # For non-assignment cases, flatten arguments normally
                arg_exprs = []
                for arg in args:
                    arg_stmts, arg_expr = self.flatten_ast(arg)
                    statements.extend(arg_stmts)
                    # Handle symbol_list flattening
                    if isinstance(arg_expr, list):
                        arg_exprs.extend(arg_expr)
                    else:
                        arg_exprs.append(arg_expr)
                
                args_str = ', '.join(arg_exprs)
                
                # Special handling for arithmetic operators - use infix notation
                arithmetic_ops = {'+': '+', '-': '-', '*': '*', '%': '/'}
                if func_expr in arithmetic_ops and len(arg_exprs) == 2:
                    infix_op = arithmetic_ops[func_expr]
                    expr = f"{arg_exprs[0]} {infix_op} {arg_exprs[1]}"
                else:
                    expr = f"{func_expr}({args_str})"
                
                # Always create temp variable for function calls (we need proper evaluation order)
                self.temp_counter += 1
                temp_name = f"temp{self.temp_counter}"
                statements.append(f"{temp_name} = {expr}")
                return statements, temp_name
            else:
                # First element is lazy or empty list: treat as regular list
                elem_exprs = []
                for elem in node.children:
                    elem_stmts, elem_expr = self.flatten_ast(elem)
                    statements.extend(elem_stmts)
                    # Handle symbol_list flattening
                    if isinstance(elem_expr, list):
                        elem_exprs.extend(elem_expr)
                    else:
                        elem_exprs.append(elem_expr)
                elements_str = ', '.join(elem_exprs)
                return statements, f"[{elements_str}]"
                
        elif node.node_type == 'symbol_list':
            # Flatten symbol list into individual symbols
            symbols = [f"`{child.value}" for child in node.children]
            return statements, f"[{', '.join(symbols)}]"
                
        elif node.node_type == 'lambda':
            # Generate def function for lambda since Python doesn't support multi-line lambdas
            body_node = node.children[0]  # Body is now the only child
            
            # Generate function name - use custom name if provided, otherwise auto-generate
            if 'func_name' in kwargs:
                func_name = kwargs['func_name']
            else:
                self.func_counter += 1
                func_name = f"func{self.func_counter}"
            
            # Get parameter names from the property (no flattening needed)
            param_names = getattr(node, 'param_names', [])
            param_str = ', '.join(param_names) if param_names else ''
            
            # Flatten body
            body_stmts, body_expr = self.flatten_ast(body_node)
            
            # Generate function definition
            statements.append(f"def {func_name}({param_str}):")
            if body_stmts:
                # Multi-line function body - optimize like lines 526-536
                last_temp_var = f'temp{self.temp_counter}'
                if body_expr == last_temp_var:
                    # Replace last temp assignment with return (similar to result optimization)
                    for stmt in body_stmts[:-1]:
                        statements.append(f"    {stmt}")
                    statements.append(f"    {body_stmts[-1].replace(f'{last_temp_var} = ', 'return ', 1)}")
                else:
                    # Handle case where body_expr might be a list or different expression
                    for stmt in body_stmts:
                        statements.append(f"    {stmt}")
                    if isinstance(body_expr, list):
                        body_expr = ', '.join(body_expr)
                    statements.append(f"    return {body_expr}")
            else:
                # Single-line function body
                if isinstance(body_expr, list):
                    body_expr = ', '.join(body_expr)
                statements.append(f"    return {body_expr}")
            
            return statements, func_name
                
        elif node.node_type == 'dict':
            # Flatten dictionary
            keys_node = node.children[0]
            values_node = node.children[1]
            k_stmts, k_expr = self.flatten_ast(keys_node)
            v_stmts, v_expr = self.flatten_ast(values_node)
            statements.extend(k_stmts)
            statements.extend(v_stmts)
            return statements, f"{{{k_expr}: {v_expr}}}"
        else:
            return statements, str(node)

# AST Transformer
def transform_ast(node: ASTNode) -> str:
    """Transform AST nodes to Python-like syntax"""
    if node.node_type == 'variable':
        return node.value  # Variables don't get backticks
    elif node.node_type == 'symbol':
        return f"`{node.value}"  # Only symbols get backticks
    elif node.node_type == 'symbol_list':
        # Flatten symbol list into individual symbols
        return [f"`{elem.value}" for elem in node.children]
    elif node.node_type == 'integer':
        return str(node.value)
    elif node.node_type == 'float':
        # Ensure float has decimal point
        value_str = str(node.value)
        if '.' not in value_str:
            value_str += '.0'
        return value_str
    elif node.node_type == 'boolean':
        return 'True' if node.value else 'False'
    elif node.node_type == 'string':
        return node.value
    elif node.node_type == 'function':
        # Convert function calls from LISP [Func[name], arg1, arg2] to name(arg1, arg2)
        # Replace glyphs with readable names
        func_name = glyph_map.get(node.value, node.value)
        
        # Transform arguments with flattening
        arg_strs = []
        for arg in node.children:
            arg_result = transform_ast(arg)
            if isinstance(arg_result, list):
                arg_strs.extend(arg_result)
            else:
                arg_strs.append(arg_result)
        
        args_str = ', '.join(arg_strs)
        return f"{func_name}({args_str})"
    elif node.node_type == 'list':
        # Check if this is a function call (first element is Function)
        if node.children and node.children[0].node_type == 'function':
            func = node.children[0]
            func.children = node.children[1:]  # Set the arguments
            return transform_ast(func)
        else:
            # Regular list
            elem_strs = []
            for elem in node.children:
                elem_result = transform_ast(elem)
                if isinstance(elem_result, list):
                    elem_strs.extend(elem_result)
                else:
                    elem_strs.append(elem_result)
            elements_str = ', '.join(elem_strs)
            return f"[{elements_str}]"
    elif node.node_type == 'dict':
        # Transform Dict to Python dict syntax
        keys_node = node.children[0]
        values_node = node.children[1]
        k_str = transform_ast(keys_node)
        v_str = transform_ast(values_node)
        return f"{{{k_str}: {v_str}}}"
    else:
        return str(node)

def convert_lisp_to_function_calls(parsed_str):
    """Convert LISP-like representation to function call syntax using AST"""
    # First decode bytes to string if needed
    if isinstance(parsed_str, bytes):
        parsed_str = parsed_str.decode('utf-8')
    
    # Tokenize and parse into AST
    tokens = tokenize(parsed_str)
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Transform AST to Python-like syntax
    return transform_ast(ast)

def convert_lisp_to_flat_statements(parsed_str):
    """Convert LISP-like representation to step-by-step Python statements"""
    # First decode bytes to string if needed
    if isinstance(parsed_str, bytes):
        parsed_str = parsed_str.decode('utf-8')
    
    # Tokenize and parse into AST
    tokens = tokenize(parsed_str)
    parser = Parser(tokens)
    ast = parser.parse()
    
    # Flatten AST to step-by-step assignments
    f = Flattener()
    statements, final_expr = f.flatten(ast)
    # Format output
    if statements:
        # Add the final expression without temp variable (unless it's None for assignments)
        if final_expr is not None:
            # Check if final_expr is a temp variable that we can replace with its expression
            if final_expr.startswith('temp') and final_expr[4:].isdigit():
                # Replace the last temp assignment with just the expression
                last_stmt = statements[-1]
                if last_stmt.startswith(f"{final_expr} = "):
                    # Remove the temp assignment and use the expression directly
                    statements[-1] = last_stmt[len(f"{final_expr} = "):]
                else:
                    statements.append(final_expr)
            else:
                statements.append(final_expr)
        return '\n'.join(statements)
    else:
        # No statements, just return the final expression
        return final_expr
    # if statements:
    #     if final_expr == last_temp_var:
    #         statements[-1] = statements[-1].replace(last_temp_var, 'result', 1)
    #     else: 
    #         # Handle case where final_expr might be a list
    #         if isinstance(final_expr, list):
    #             final_expr = ', '.join(final_expr)
    #         # Skip result assignment if it would just be "result = func{n}"
    #         if not (final_expr.startswith('func') and final_expr[4:].isdigit()):
    #             statements.append('result = ' + final_expr)
    # else:
    #     # Handle case where final_expr might be a list
    #     if isinstance(final_expr, list):
    #         final_expr = ', '.join(final_expr)
    #     # Skip result assignment if it would just be "result = func{n}"
    #     if final_expr.startswith('func') and final_expr[4:].isdigit():
    #         return final_expr
    #     else:
    #         return 'result = ' + final_expr

def translate(q_expression: str, q) -> str:
    """
    Take a q expression, convert to flattened Python-like code,
    then ask Claude to add disambiguating comments
    """
    # Convert q to flattened Python-like code
    if q._current_async_task and q._current_async_task.get("status") == "Running":
        return "Cannot use code q->qython code translation while another q query is running"
    flattened_code = convert_lisp_to_flat_statements(parseq0(q_expression, q))
    
    return disambiguate_step(flattened_code)


def parseq0(s, qcomms):
    assert len(qcomms._listener_thread.messages) == 0 , "Shouldn't happen: there are messages in the listener thread message stack upon calling parseq0 in parseq module"
    qcomms._q_connection.q.sendSyncDetached(parseq_q_code+'; .parseq.parseq', s)
    assert qcomms._listener_thread.wait_for_response(1) # wait for maximum 1 second though in practice should be instant
    return qcomms.parse_raw_bytes(qcomms._listener_thread.messages.pop().data).str

def parseq1(s, q):
    return convert_lisp_to_function_calls(parseq0(s, q))

def parseq(s, q):
    # return convert_lisp_to_function_calls(q('var2string parse "'+s+'"'))
    return convert_lisp_to_flat_statements(parseq0(s, q))
def pr(s, q):
    print(parseq(s, q),'\n')
# pr('f[min]')
# pr('a lj 2!select min s, maxs t from c')
# pr('min x')
# pr('f x')
# pr('var')
# pr('`var')
# pr('`a`s`d')
# pr('f[a;b;c]')
# pr('f[`a`b`c]')
# pr('2+3*4')
# pr('{x+1}')
# print(parseq0('{a:x;x+a}'))
# pr('{a:x;x+a}')
# print(parseq0('nmsq:{[x] ({(y+x%y)%2f}[x]/) x%2f}'),'\n')
# print(parseq1('nmsq:{[x] ({(y+x%y)%2f}[x]/) x%2f}'),'\n')
# print(parseq('nmsq:{[x] ({(y+x%y)%2f}[x]/) x%2f}'),'\n')
# pr('f1:{x+1};f2:{x+2}')
# pr('2+3')

