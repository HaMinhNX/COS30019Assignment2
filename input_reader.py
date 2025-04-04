"""
Reader module for parsing input files containing knowledge bases and queries.
Supports both Horn-form and general knowledge bases.
"""

def read_file(filename):
    """
    Reads a file containing a knowledge base and query.
    
    Args:
        filename (str): Path to the input file
        
    Returns:
        tuple: (kb_string, query_string) where kb_string is the knowledge base string
        and query_string is the query string
    """
    try:
        with open(filename, 'r') as file:
            content = file.read()
            
            # locatate TEll and Ask
            tell_pos = content.find('TELL')
            ask_pos = content.find('ASK')
            
            if tell_pos == -1 or ask_pos == -1:
                raise ValueError("File must contain both TELL and ASK sections")
            
            kb_string = content[tell_pos+4:ask_pos].strip()
            query_string = content[ask_pos+3:].strip()
            
            return kb_string, query_string
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")

def is_horn_form(kb_string):
    """
    Determine if a knowledge base is in Horn form.
    
    Args:
        kb_string (str): Knowledge base string
        
    Returns:
        bool: True if the knowledge base is in Horn form, False otherwise
    """
    # whether if it is Hornform
    if '||' in kb_string or '<=' in kb_string or '<=>' in kb_string:
        return False
    
    clauses = [clause.strip() for clause in kb_string.split(';') if clause.strip()]
    
    for clause in clauses:
        if '=>' in clause:
            premise, conclusion = clause.split('=>')
            if '~' in conclusion.strip():
                return False
        elif '~' in clause:
            return False
            
    return True

def parse_kb(kb_string):
    """
    Parses a knowledge base string into a list of clauses.
    
    Args:
        kb_string (str): Knowledge base string
        
    Returns:
        list: List of clauses
    """
    # delete space, semicolon
    clauses = [clause.strip() for clause in kb_string.split(';') if clause.strip()]
    
    return clauses

def parse_query(query_string):
    """
    Parses a query string.
    
    Args:
        query_string (str): Query string
        
    Returns:
        str: The query proposition symbol or expression
    """
    return query_string.strip()