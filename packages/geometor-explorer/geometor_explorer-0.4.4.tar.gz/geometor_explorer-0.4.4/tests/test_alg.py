import sympy as sp
import json
from sympy.core.function import Function

# --- Configuration ---

# ! SET THIS to the path of your JSON file
# I am setting it to 'constructions/pentagon.json' as you mentioned.
JSON_FILE_PATH = 'constructions/pentagon.json' 

# Add any other specific string expressions you want to test here.
# I've added the one likely causing the issue for point NN.
# This expression is related to the side length of a pentagon.
TEST_EXPRESSIONS = [
    "sqrt(5 - 2*sqrt(5))/2",  # Likely y-coord for NN
    "sqrt( (5 - sqrt(5)) / 8 )", # Another common pentagon value
    "1 + sqrt(5)", # Golden ratio, not nested
    "sqrt(1 + sqrt(5))", # Nested
]

# --- Simplification Functions ---

def clean_expr(expr):
    """
    Simplify and denest SymPy expressions iteratively to find a stable,
    canonical form. It avoids converting to float.
    """
    if not isinstance(expr, sp.Expr):
        return expr
        
    original_expr = expr
    try:
        # Iteratively apply simplifications until the expression stabilizes.
        # This helps in cases where one simplification enables another.
        last_expr = expr
        for _ in range(5):  # Limit to 5 iterations to prevent infinite loops
            # 1. Rationalize denominators and simplify radical expressions.
            expr = sp.radsimp(expr)
            # 2. Attempt to denest any square roots.
            expr = sp.sqrtdenest(expr)
            # 3. Apply general simplification routines.
            expr = sp.simplify(expr)
            # 4. Expand the expression to break down complex arguments.
            expr = sp.expand(expr)
            
            if expr == last_expr:
                # Expression has stabilized, no more changes.
                break
            last_expr = expr
            
        return expr
    except Exception as e:
        print(f"Warning: Could not simplify {original_expr}. Error: {e}")
        return original_expr


def has_nested_radicals(expr):
    """
    Checks if a SymPy expression contains nested radicals (e.g., sqrt(1 + sqrt(2))).
    """
    if not isinstance(expr, sp.Expr):
        return False

    # Find all radical functions (sp.sqrt or Pow(..., 1/2))
    # We use atoms() to find all sub-expressions of these types
    radicals = expr.atoms(sp.sqrt) | {p for p in expr.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)}

    for rad in radicals:
        # The base is the argument *inside* the radical
        # For sp.sqrt(base), args[0] is base
        # For Pow(base, 1/2), args[0] is base
        base = rad.args[0]
        
        # Now, check if this base *itself* contains any radicals
        base_radicals = base.atoms(sp.sqrt) | {p for p in base.atoms(sp.Pow) if p.exp == sp.Rational(1, 2)}
        
        if base_radicals:
            # If the base has any radicals, it's a nested radical
            return True
            
    return False

# --- Main Test Runner ---

def test_simplification():
    """
    Loads expressions from a JSON file and the TEST_EXPRESSIONS list,
    checks them for nested radicals, and attempts to simplify them.
    """
    
    all_expressions_to_test = set(TEST_EXPRESSIONS)

    # 1. Load expressions from the JSON file
    try:
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
        
        # Assuming a structure like {"points": {"A": {"x": "0", "y": "1"}, ...}}
        if 'points' in data and isinstance(data['points'], dict):
            for point_name, coords in data['points'].items():
                if isinstance(coords, dict):
                    if 'x' in coords and isinstance(coords['x'], str):
                        all_expressions_to_test.add(coords['x'])
                    if 'y' in coords and isinstance(coords['y'], str):
                        all_expressions_to_test.add(coords['y'])
            print(f"--- Successfully loaded expressions from {JSON_FILE_PATH} ---")
        else:
            print(f"Warning: Could not find 'points' dictionary in {JSON_FILE_PATH}.")

    except FileNotFoundError:
        print(f"Warning: {JSON_FILE_PATH} not found.")
        print("--- Running only with hardcoded TEST_EXPRESSIONS ---")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {JSON_FILE_PATH}.")
        return
    except Exception as e:
        print(f"An error occurred loading the JSON file: {e}")

    # 2. Process and test all expressions
    print("\n--- Starting Simplification Test ---")
    
    for i, s_expr in enumerate(sorted(list(all_expressions_to_test))):
        print(f"\n======== TEST {i+1} ========")
        print(f"Original String: {s_expr}")
        
        try:
            expr = sp.sympify(s_expr)
        except sp.SympifyError as e:
            print(f"Sympify Error: {e}")
            continue
            
        print(f"Original SymPy:  {expr}")
        
        # Check for nested radicals
        is_nested = has_nested_radicals(expr)
        print(f"Has Nested Radicals? -> {is_nested}")
        
        if not is_nested:
            print("Skipping denesting (not nested).")
            continue

        # Apply the enhanced simplification
        print("--- Applying clean_expr ---")
        simplified_expr = clean_expr(expr)
        
        print(f"Simplified SymPy:  {simplified_expr}")
        
        # Check again
        is_nested_after = has_nested_radicals(simplified_expr)
        print(f"Has Nested Radicals After? -> {is_nested_after}")
        
        if simplified_expr == expr:
            print("Result: No symbolic change.")
        elif is_nested_after:
            print("Result: Canonical form found, but it remains nested.")
            print("        (This is expected for certain mathematical expressions.)")
        else:
            print("Result: SUCCESS - Denested!")
            

if __name__ == "__main__":
    test_simplification()

