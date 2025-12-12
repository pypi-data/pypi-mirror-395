# interpreter.py

from . import core, combinatorics, genai, optimization, graph, vision
import ast

SAFE_FUNCTIONS = {
    "add": core.add,
    "sqrt": core.sqrt,
    "comb": combinatorics.comb,
    "perm": combinatorics.perm,
    "softmax": genai.softmax,
    "dijkstra": graph.dijkstra,
    "conv2d": vision.conv2d,
}


def run():
    print("AIMATHX Interactive Shell — type 'exit' to quit")

    while True:
        try:
            line = input("aimath> ").strip()
            if line in ("quit", "exit"):
                break

            if "(" in line and line.endswith(")"):
                func = line.split("(")[0]
                args_str = line[line.index("(") + 1 : -1]

                if func not in SAFE_FUNCTIONS:
                    print("❌ Function not allowed")
                    continue

                args = []
                if args_str.strip():
                    args = [ast.literal_eval(a.strip()) for a in args_str.split(",")]

                result = SAFE_FUNCTIONS[func](*args)
                print(result)
            else:
                print("Use format: function(arg1,arg2)")
        except Exception as e:
            print("Error:", e)
