"""
Forward Chaining (FC) algorithm for propositional logic inference engine.
"""

def parse_horn_clause(clause):
    """
    Parse a Horn clause to extract premises and conclusion.
    
    Args:
        clause (str): A Horn clause
        
    Returns:
        tuple: (premises, conclusion) where premises is a list of premise symbols and 
               conclusion is the conclusion symbol
    """
    if '=>' in clause:
        premise, conclusion = clause.split('=>')
        premise = premise.strip()
        conclusion = conclusion.strip()
        
        if '&' in premise:
            premises = [p.strip() for p in premise.split('&')]
        else:
            premises = [premise]
            
        return premises, conclusion
    else:
        # Fact (no premises)
        return [], clause.strip()

def fc_entails(kb_clauses, query):
    """
    Forward Chaining algorithm to determine if KB entails query.
    
    Args:
        kb_clauses (list): List of clauses in the knowledge base
        query (str): The query proposition symbol
        
    Returns:
        tuple: (bool, list) where bool is True if KB entails query and list is the 
               list of entailed symbols
    """
    # Parse all clauses to get premises and conclusions
    horn_clauses = [parse_horn_clause(clause) for clause in kb_clauses]
    
    # Extract all symbols from the KB
    symbols = set()
    for premises, conclusion in horn_clauses:
        symbols.update(premises)
        symbols.add(conclusion)
    
    # Initialize the count of premises for each clause
    count = {}
    for i, (premises, _) in enumerate(horn_clauses):
        count[i] = len(premises)
    
    # Initialize inferred and agenda
    inferred = {symbol: False for symbol in symbols}
    agenda = []
    
    # Add facts to agenda
    for premises, conclusion in horn_clauses:
        if not premises:  # This is a fact
            agenda.append(conclusion)
            inferred[conclusion] = True
    
    # Track the order of entailed symbols
    entailed_symbols = []
    
    # Forward chaining
    while agenda:
        p = agenda.pop(0)
        entailed_symbols.append(p)
        
        if p == query:
            return True, entailed_symbols
        
        for i, (premises, conclusion) in enumerate(horn_clauses):
            if p in premises and not inferred[conclusion]:
                count[i] -= 1
                if count[i] == 0:
                    inferred[conclusion] = True
                    agenda.append(conclusion)
    
    return False, entailed_symbols