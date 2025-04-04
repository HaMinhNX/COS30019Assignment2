"""
Backward Chaining (BC) algorithm for propositional logic inference engine.
"""

def parse_horn_clauses(kb_clauses):
    """
    Parse Horn clauses and organize them by conclusion symbol.
    
    Args:
        kb_clauses (list): List of clauses in the knowledge base
        
    Returns:
        dict: Dictionary mapping conclusion symbols to lists of premises
    """
    kb_rules = {}
    
    for clause in kb_clauses:
        if '=>' in clause:
            premise, conclusion = clause.split('=>')
            premise = premise.strip()
            conclusion = conclusion.strip()
            
            if '&' in premise:
                premises = [p.strip() for p in premise.split('&')]
            else:
                premises = [premise]
            
            if conclusion not in kb_rules:
                kb_rules[conclusion] = []
            kb_rules[conclusion].append(premises)
        else:
            fact = clause.strip()
            if fact not in kb_rules:
                kb_rules[fact] = []
            kb_rules[fact].append([])  
    
    return kb_rules

def bc_entails(kb_clauses, query):
    """
    Backward Chaining algorithm to determine if KB entails query.
    
    Args:
        kb_clauses (list): List of clauses in the knowledge base
        query (str): The query proposition symbol
        
    Returns:
        tuple: (bool, list) where bool is True if KB entails query and list is the
               list of entailed symbols used in the proof
    """
    kb_rules = parse_horn_clauses(kb_clauses)
    entailed = set()
    
    def bc_check(symbol, path=None):
        if path is None:
            path = set()
        
        if symbol in path:
            return False
        
        path.add(symbol)
        
        if symbol not in kb_rules:
            return False
        
        for premises in kb_rules[symbol]:
            if not premises:  
                entailed.add(symbol)
                return True
            
            if all(bc_check(premise, path.copy()) for premise in premises):
                entailed.add(symbol)
                return True
        
        return False
    
    result = bc_check(query)
    
    proof_symbols = []
    if result:
        proof_stack = [query]
        visited = set()
        
        while proof_stack:
            current = proof_stack.pop()
            
            if current in visited:
                continue
                
            visited.add(current)
            proof_symbols.append(current)
            
            if current in kb_rules:
                for premises in kb_rules[current]:
                    if all(premise in entailed for premise in premises):
                        proof_stack.extend(premises)
                        break
    
    return result, proof_symbols