"""
Truth Table (TT) checking algorithm for propositional logic inference engine.
Supports general knowledge bases with all logical operators.
"""

def extract_symbols(kb_clauses):
    """
    Extract all proposition symbols from the knowledge base.
    
    Args:
        kb_clauses (list): List of clauses in the knowledge base
        
    Returns:
        set: Set of all proposition symbols in the knowledge base
    """
    symbols = set()
    
    for clause in kb_clauses:
        # Remove special characters and split into parts
        clean_clause = clause.replace('=>', ' ').replace('&', ' ').replace(';', ' ')
        clean_clause = clean_clause.replace('(', ' ').replace(')', ' ')
        clean_clause = clean_clause.replace('~', ' ').replace('||', ' ')
        clean_clause = clean_clause.replace('<=>', ' ')
        
        # Add each word as a symbol
        for word in clean_clause.split():
            if word.strip() and word.strip().isalnum():
                symbols.add(word.strip())
                
    return symbols

def evaluate_expression(expr, model):
    """
    Evaluate a propositional logic expression given a model.
    
    Args:
        expr (str): A propositional logic expression
        model (dict): A model assigning truth values to proposition symbols
        
    Returns:
        bool: The truth value of the expression under the model
    """
    # Remove all whitespace
    expr = expr.replace(" ", "")
    
    # Handle parentheses recursively
    if '(' in expr:
        # Find matching parentheses
        count = 0
        start = None
        for i, char in enumerate(expr):
            if char == '(':
                if start is None:
                    start = i
                count += 1
            elif char == ')':
                count -= 1
                if count == 0 and start is not None:
                    # Replace the parenthesized expression with its evaluation
                    inner_expr = expr[start+1:i]
                    inner_value = evaluate_expression(inner_expr, model)
                    expr = expr[:start] + str(inner_value) + expr[i+1:]
                    return evaluate_expression(expr, model)
    
    # Handle biconditional (<=>)
    if '<=>' in expr:
        left, right = expr.split('<=>', 1)
        left_value = evaluate_expression(left, model)
        right_value = evaluate_expression(right, model)
        return left_value == right_value
    
    # Handle implication (=>)
    if '=>' in expr:
        left, right = expr.split('=>', 1)
        left_value = evaluate_expression(left, model)
        right_value = evaluate_expression(right, model)
        return (not left_value) or right_value
    
    # Handle disjunction (||)
    if '||' in expr:
        parts = expr.split('||')
        return any(evaluate_expression(part, model) for part in parts)
    
    # Handle conjunction (&)
    if '&' in expr:
        parts = expr.split('&')
        return all(evaluate_expression(part, model) for part in parts)
    
    # Handle negation (~)
    if expr.startswith('~'):
        return not evaluate_expression(expr[1:], model)
    
    # Handle atomic propositions
    if expr.lower() == 'true':
        return True
    elif expr.lower() == 'false':
        return False
    else:
        return model.get(expr, False)

def evaluate_kb(kb_clauses, model):
    """
    Evaluate if a knowledge base is satisfied by a model.
    
    Args:
        kb_clauses (list): List of clauses in the knowledge base
        model (dict): A model assigning truth values to proposition symbols
        
    Returns:
        bool: True if the model satisfies the knowledge base, False otherwise
    """
    for clause in kb_clauses:
        if not evaluate_expression(clause, model):
            return False
    return True

def tt_check_all(kb_clauses, query, symbols, model):
    """
    Recursive helper function for TT-Check-All.
    
    Args:
        kb_clauses (list): List of clauses in the knowledge base
        query (str): The query expression
        symbols (list): List of proposition symbols
        model (dict): Current partial model
        
    Returns:
        tuple: (bool, int) where bool is True if KB entails query and int is the number of models of KB
    """
    if not symbols:
        if evaluate_kb(kb_clauses, model):
            return evaluate_expression(query, model), 1
        return True, 0  # KB is false, so KB |= query is true vacuously
    
    p, *rest = symbols
    
    # Try p = true
    model[p] = True
    true_result, true_count = tt_check_all(kb_clauses, query, rest, model)
    
    # Try p = false
    model[p] = False
    false_result, false_count = tt_check_all(kb_clauses, query, rest, model)
    
    return true_result and false_result, true_count + false_count

def tt_entails(kb_clauses, query):
    """
    Truth table enumeration to determine if KB entails query.
    
    Args:
        kb_clauses (list): List of clauses in the knowledge base
        query (str): The query expression
        
    Returns:
        tuple: (bool, int) where bool is True if KB entails query and int is the number of models of KB
    """
    # Extract symbols from both KB and query
    symbols = extract_symbols(kb_clauses)
    
    # Add symbols from query
    query_symbols = extract_symbols([query])
    symbols.update(query_symbols)
    
    return tt_check_all(kb_clauses, query, list(symbols), {})