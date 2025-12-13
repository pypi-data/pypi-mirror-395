import sys
import ast

def detect_version(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    py2_score = 0
    py3_score = 0
    reasons = []

    # Try parsing with Python 3 syntax
    try:
        tree = ast.parse(source)
        py3_score += 1
        reasons.append("Parsed successfully with Python 3 syntax.")
    except SyntaxError:
        print("2\nConfidence: High\nReason: Syntax error when parsed with Python 3.")
        return

    # Check for print statement (Python 2)
    if 'print ' in source and not 'print(' in source:
        py2_score += 2
        reasons.append("Uses print statement without parentheses (Python 2 style).")

    # Check for future import
    if '__future__' in source and 'print_function' in source:
        py3_score += 2
        reasons.append("Uses 'from __future__ import print_function' (Python 3 compatibility).")

    # Check for Python 3-only features
    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef) or isinstance(node, ast.Await):
            py3_score += 3
            reasons.append("Uses async/await syntax (Python 3 only).")
        if isinstance(node, ast.Try) and hasattr(node, 'finalbody'):
            py3_score += 1
            reasons.append("Uses try/finally block (Python 3 syntax).")
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if hasattr(arg, 'annotation') and arg.annotation is not None:
                    py3_score += 2
                    reasons.append("Uses function argument annotations (Python 3 feature).")

    # Final decision
    if py2_score > py3_score:
        version = "2"
        confidence = "High" if py2_score - py3_score > 2 else "Medium"
    elif py3_score > py2_score:
        version = "3"
        confidence = "High" if py3_score - py2_score > 2 else "Medium"
    else:
        version = "3"
        confidence = "Low"
        reasons.append("No strong indicators found; defaulting to Python 3.")

    print(f"{version}\nConfidence: {confidence}\nReason(s):")
    for reason in reasons:
        print(f"- {reason}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python is_py2_or_py3.py <filename>")
    else:
        detect_version(sys.argv[1])