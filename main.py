"""
Inference engine for propositional logic.
Supports both Horn-form and general knowledge bases.
"""

import sys
from input_reader import read_file, parse_kb, parse_query, is_horn_form
from truth_table import tt_entails
from forward_chaining import fc_entails
from backward_chaining import bc_entails

def main():
    """
    Main function that processes command line arguments and runs the requested inference method.
    """
    if len(sys.argv) != 3:
        print("Usage: python iengine.py <filename> <method>")
        print("where method is one of: TT, FC, BC")
        sys.exit(1)
    
    filename = sys.argv[1]
    method = sys.argv[2].upper()
    
    if method not in ["TT", "FC", "BC"]:
        print("Invalid method. Use one of: TT, FC, BC")
        sys.exit(1)
    if 
    else
    
    try:
        kb_string, query_string = read_file(filename)
        kb_clauses = parse_kb(kb_string)
        query = parse_query(query_string)
        
        # Check if knowledge base is in Horn form for FC and BC
        is_horn = is_horn_form(kb_string)
        
        if method in ["FC", "BC"] and not is_horn:
            print("Error: Forward Chaining and Backward Chaining algorithms require a Horn-form knowledge base.")
            sys.exit(1)
        
        if method == "TT":
            result, models_count = tt_entails(kb_clauses, query)
            if result:
                print(f"YES: {models_count}")
            else:
                print("NO")
                
        elif method == "FC":
            result, entailed_symbols = fc_entails(kb_clauses, query)
            if result:
                print(f"YES: {', '.join(entailed_symbols)}")
            else:
                print("NO")
                
        elif method == "BC":
            result, proof_symbols = bc_entails(kb_clauses, query)
            if result:
                print(f"YES: {', '.join(proof_symbols)}")
            else:
                print("NO")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()