import warnings
warnings.filterwarnings("ignore", message=".*found in sys.modules.*", category=RuntimeWarning)

import argparse
import sys
import shlex
import importlib
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from pygments.lexers.python import PythonLexer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

class safeargparser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)

def lazy(name):
    return importlib.import_module(f"brliant_calc.{name}")

def execute_command(arguments, user_vars=None):
    try:
        if arguments.command in ["basic", "b"]:
            mod = lazy("basic_ops")
            func = getattr(mod, arguments.operation)
            nums = arguments.numbers
            if arguments.operation == "mod" and len(nums) != 2:
                console.print("[bold red]Error: mod requires exactly two arguments[/bold red]")
                return
            result = func(*nums)
            output = f"{result:g}" if isinstance(result, (int, float)) else str(result)
            console.print(Panel(output, title="Result", expand=False, style="bold green"))

        elif arguments.command in ["adv", "a"]:
            mod = lazy("advanced_ops")
            func = getattr(mod, arguments.operation)
            try:
                result = func(*arguments.numbers)
            except TypeError as e:
                print(f"Error: {e}")
                return
            print(f"{result:g}" if isinstance(result, (int, float)) else result)

        elif arguments.command in ["curr", "cr"]:
            if arguments.update == "upd":
                from currency_converter.app import get_curr_json
                get_curr_json()
                print("Exchange rates updated successfully.")

        elif arguments.command in ["convert", "cv"]:
            mod = importlib.import_module("brliant_calc.convert_currency")
            result = mod.convert_currency(arguments.from_currency, arguments.to_currency, arguments.amount)
            print(f"{arguments.amount} {arguments.from_currency} = {result:.2f} {arguments.to_currency}")

        elif arguments.command in ["vector", "v"]:
            mod = lazy("vectors")
            func = getattr(mod, arguments.operation)
            comps = arguments.components
            if arguments.operation in ["dot_product", "cross_product", "angle_between"]:
                if len(comps) % 2 != 0:
                    print("Error: Vectors must have the same number of dimensions.")
                    return
                mid = len(comps) // 2
                result = func(comps[:mid], comps[mid:])
            else:
                result = func(comps)
            print(result)

        elif arguments.command in ["physics", "p"]:
            mod = lazy("physics_formulas")
            func = getattr(mod, arguments.operation)
            try:
                result = func(*arguments.args)
            except TypeError as e:
                print(f"Error: {e}")
                return
            print(result)

        elif arguments.command in ["units", "u"]:
            mod = lazy("units")
            func = getattr(mod, arguments.category)
            print(func(arguments.value, arguments.from_unit, arguments.to_unit))

        elif arguments.command in ["matrix", "m"]:
            mod = lazy("matrix_ops")
            func = getattr(mod, arguments.operation)
            if arguments.operation == "mul":
                print(func(arguments.m1, arguments.m2))
            else:
                print(func(arguments.m1))

        elif arguments.command in ["complex", "cx"]:
            mod = lazy("complex_ops")
            func = getattr(mod, arguments.operation)
            if arguments.operation in ["add", "sub", "mul", "div"]:
                print(func(arguments.c1, arguments.c2))
            elif arguments.operation == "rect":
                print(func(arguments.c1, arguments.c2))
            else:
                print(func(arguments.c1))

        elif arguments.command in ["symbolic", "s"]:
            mod = lazy("symbolic_ops")
            func = getattr(mod, arguments.operation)
            if arguments.operation in ["diff", "integrate", "solve"]:
                print(func(arguments.expression, arguments.variable))
            else:
                print(func(arguments.expression))

        elif arguments.command in ["plot", "pl"]:
            mod = lazy("plotting")
            func = getattr(mod, arguments.operation)
            print(func(arguments.function, arguments.range, user_vars))

        elif arguments.command in ["dim", "d"]:
            mod = lazy("dimensional_analysis")
            func = getattr(mod, arguments.operation)
            if arguments.operation == "evaluate_dim":
                print(func(arguments.expression))
            else:
                print(func(arguments.value, arguments.from_unit, arguments.to_unit))


        elif arguments.command in ["precise", "pr"]:
            mod = lazy("precision_ops")
            func = getattr(mod, arguments.operation)
            if "decimal" in arguments.operation:
                print(func(arguments.n1, arguments.n2, arguments.precision))
            else:
                print(func(arguments.n1, arguments.n2))

        elif arguments.command in ["convolve", "cnv"]:
            mod = lazy("advanced_ops")
            result = mod.convolve(arguments.signal, arguments.kernel)
            console.print(Panel(str(result), title="Convolution Result", expand=False, style="bold cyan"))

    except Exception as e:
        console.print(f"[bold red]An error has occurred: {e}[/bold red]")

class CommandAutoSuggest(AutoSuggest):
    def __init__(self, commands, arg_map=None, example_map=None):
        self.commands = commands
        self.arg_map = arg_map or {}
        self.example_map = example_map or {}

    def get_suggestion(self, buffer, document):
        text = document.text_before_cursor
        
       
        if ' ' not in text:
            val = text.strip()
            if not val:
                return None
            for cmd in self.commands:
                if cmd.startswith(val):
                    return Suggestion(cmd[len(val):])
            return None
            
        
        parts = text.split()
        if not parts:
            return None
            
        cmd = parts[0]
        if cmd not in self.commands:
            return None
            
        
        if len(parts) == 1 and text.endswith(' '):
            example = self.example_map.get(cmd)
            if example:
                return Suggestion(example)
        
        
        suggestions = self.arg_map.get(cmd, [])
        is_new_arg = text.endswith(' ')
        current_typing = "" if is_new_arg else parts[-1]
        
        for sugg in suggestions:
            if is_new_arg:
                return Suggestion(sugg)
            if sugg.startswith(current_typing) and sugg != current_typing:
                 return Suggestion(sugg[len(current_typing):])
                 
        return None
                 
        return None

def run_shell(category, parser):
  

    
    category_map = {
        'b': 'basic', 'a': 'adv', 'cr': 'curr', 'cv': 'convert', 'v': 'vector', 
        'p': 'physics', 'u': 'units', 'm': 'matrix', 'cx': 'complex', 
        's': 'symbolic', 'pl': 'plot', 'd': 'dim', 'pr': 'precise', 'cnv': 'convolve', 'sh': 'sel'
    }
    canonical_category = category_map.get(category, category)

    full_completer_dict = {
        'basic': ['add', 'sub', 'mul', 'div', 'mod'],
        'b': ['add', 'sub', 'mul', 'div', 'mod'],
        'adv': ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh', 'log', 'log10', 'log2', 'exp', 'sqrt', 'abs', 'nth', 'pow', 'fact', 'floor', 'ceil', 'round', 'trunc', 'sign', 'mean', 'median', 'std', 'var', 'min', 'max', 'sum', 'prod'],
        'a': ['sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'sinh', 'cosh', 'tanh', 'arcsinh', 'arccosh', 'arctanh', 'log', 'log10', 'log2', 'exp', 'sqrt', 'abs', 'nth', 'pow', 'fact', 'floor', 'ceil', 'round', 'trunc', 'sign', 'mean', 'median', 'std', 'var', 'min', 'max', 'sum', 'prod'],
        'curr': ['upd'],
        'cr': ['upd'],
        'convert': [],
        'cv': [],
        'vector': ['dot_product', 'cross_product', 'magnitude', 'normalize', 'angle_between'],
        'v': ['dot_product', 'cross_product', 'magnitude', 'normalize', 'angle_between'],
        'physics': ['force', 'kinetic_energy', 'potential_energy', 'ohms_law', 'work', 'speed', 'acceleration'],
        'p': ['force', 'kinetic_energy', 'potential_energy', 'ohms_law', 'work', 'speed', 'acceleration'],
        'units': ['length', 'mass', 'temperature', 'time', 'speed'],
        'u': ['length', 'mass', 'temperature', 'time', 'speed'],
        'matrix': ['mul', 'det', 'inv', 'eig', 'transpose', 'rank'],
        'm': ['mul', 'det', 'inv', 'eig', 'transpose', 'rank'],
        'complex': ['add', 'sub', 'mul', 'div', 'mag', 'phase', 'polar', 'rect'],
        'cx': ['add', 'sub', 'mul', 'div', 'mag', 'phase', 'polar', 'rect'],
        'symbolic': ['simplify', 'diff', 'integrate', 'solve', 'expand', 'factor'],
        's': ['simplify', 'diff', 'integrate', 'solve', 'expand', 'factor'],
        'plot': ['plot'],
        'pl': ['plot'],
        'dim': ['evaluate_dim', 'convert_dim'],
        'd': ['evaluate_dim', 'convert_dim'],
        'precise': ['add_fraction', 'sub_fraction', 'mul_fraction', 'div_fraction', 'add_decimal', 'sub_decimal', 'mul_decimal', 'div_decimal'],
        'pr': ['add_fraction', 'sub_fraction', 'mul_fraction', 'div_fraction', 'add_decimal', 'sub_decimal', 'mul_decimal', 'div_decimal'],
        'convolve': ['--kernel'],
        'cnv': ['--kernel'],
    }
    
   
    CATEGORY_ARG_SUGGESTIONS = {
        'matrix': {
            'mul': ['"[["', '--m2'], 
            'det': ['"[["'],
            'inv': ['"[["'],
            'eig': ['"[["'],
            'transpose': ['"[["'],
            'rank': ['"[["'],
        },
        'plot': {
            'plot': ['--range'],
        },
        'convolve': {
            'convolve': ['--kernel'],
        },
        'complex': {
            'add': ['--c2'],
            'sub': ['--c2'],
            'mul': ['--c2'],
            'div': ['--c2'],
            'rect': ['--c2'],
        },
        'precise': {
             'div_decimal': ['--precision'],
        },
        'dim': {
             'convert_dim': ['--value', '--from_unit', '--to_unit'],
        },
        'symbolic': {
             'diff': ['--variable'],
             'integrate': ['--variable'],
        },
        
        'basic': {},
        'adv': {},
        'vector': {},
        'physics': {},
        'units': {},
        'curr': {},
    }
    
    arg_suggestions = CATEGORY_ARG_SUGGESTIONS.get(canonical_category, {})
 
    CATEGORY_EXAMPLES = {
        'basic': {
            'add': '10 5', 'sub': '10 5', 'mul': '2 3 4', 'div': '10 2', 'mod': '10 3'
        },
        'adv': {
            'sin': '1.57', 'cos': '0', 'tan': '0.785', 'arcsin': '0.5', 'arccos': '0.5', 'arctan': '1',
            'sinh': '1', 'cosh': '0', 'tanh': '0.5', 'arcsinh': '1', 'arccosh': '2', 'arctanh': '0.5',
            'log': '100', 'log10': '100', 'log2': '8', 'exp': '1', 'sqrt': '16', 'abs': '-5',
            'nth': '8 3', 'pow': '2 3', 'fact': '5',
            'floor': '3.7', 'ceil': '3.2', 'round': '3.14159 2', 'trunc': '3.9', 'sign': '-42',
            'mean': '1 2 3 4 5', 'median': '1 2 3 4 5', 'std': '1 2 3 4 5', 'var': '1 2 3',
            'min': '5 2 8 1 9', 'max': '5 2 8 1 9', 'sum': '1 2 3 4 5', 'prod': '2 3 4'
        },
        'vector': {
            'dot_product': '1 2 3 4 5 6', 'cross_product': '1 0 0 0 1 0', 
            'magnitude': '3 4', 'normalize': '3 4', 'angle_between': '1 0 0 1'
        },
        'physics': {
            'force': '10 9.8', 
            'kinetic_energy': '10 5', 
            'potential_energy': '10 5', 
            'ohms_law': '2 10', 
            'work': '10 5', 
            'speed': '100 9.8',
            'acceleration': '10 2 0' 
        },
        'units': {
            'length': '100 meter kilometer', 'mass': '1000 gram kilogram', 
            'temperature': '100 celsius fahrenheit', 'time': '60 minute second', 'speed': '100 km/h m/s'
        },
        'matrix': {
            'mul': '[[1,2],[3,4]] --m2 [[5,6],[7,8]]',
            'det': '[[1,2],[3,4]]',
            'inv': '[[1,2],[3,4]]',
            'eig': '[[1,0],[0,1]]',
            'transpose': '[[1,2],[3,4]]',
            'rank': '[[1,2],[3,4]]'
        },
        'complex': {
            'add': '1+2j --c2 3+4j', 'sub': '1+2j --c2 3+4j', 'mul': '1+2j --c2 3+4j', 
            'div': '1+2j --c2 3+4j', 'mag': '3+4j', 'phase': '1+1j', 
            'polar': '1+1j', 'rect': '1.414 0.785'
        },
        'symbolic': {
            'simplify': 'x**2 + 2*x + 1', 'diff': 'x**2+1 --variable x', 
            'integrate': 'sin(x) --variable x', 'solve': 'x**2-4', 
            'expand': '(x+1)**2', 'factor': 'x**2-1'
        },
        'plot': {
            'plot': 'sin(x) --range 0,10'
        },
        'dim': {
            'evaluate_dim': '5*meter + 30*centimeter',
            'convert_dim': '--value 100 --from_unit km/h --to_unit m/s'
        },
        'precise': {
            'add_fraction': '1/3 1/6', 'sub_fraction': '1/2 1/3', 'mul_fraction': '1/2 1/3', 'div_fraction': '1/2 1/3',
            'add_decimal': '1.1 2.2', 'sub_decimal': '2.2 1.1', 'mul_decimal': '1.1 2.2', 'div_decimal': '1 3 --precision 50'
        },
        'curr': {
            'upd': ''
        },
        'convert': {
        
        }, 
        'convolve': {
             
        }
    }
    
    
    command_examples = CATEGORY_EXAMPLES.get(canonical_category, {})
    
    
    valid_commands = full_completer_dict.get(category, [])
   
    valid_commands.extend(['exit', 'quit'])
    
    
    category_completer_dict = {cmd: None for cmd in valid_commands}
    
    completer = NestedCompleter.from_nested_dict(category_completer_dict)
    
    style = Style.from_dict({
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00aaaa #000000',
        'scrollbar.background': 'bg:#88aaaa',
        'scrollbar.button': 'bg:#222222',
        'prompt': '#00ffff bold',
    })
    
    session = PromptSession(
        completer=completer, 
        style=style, 
        lexer=PygmentsLexer(PythonLexer),
        auto_suggest=CommandAutoSuggest(valid_commands, arg_suggestions, command_examples),
        complete_while_typing=False
    )

    console.print(f"[bold cyan]Entering {canonical_category} mode. Type 'exit' to quit.[/bold cyan]")
    
    variables = {}

    while True:
        try:
            line = session.prompt(f"{canonical_category} > ")
            
            if line.strip().lower() in ["exit", "quit"]:
                break
            if not line.strip():
                continue
            
            if line.strip().lower() == "vars":
                if variables:
                    console.print("[bold cyan]Stored Variables:[/bold cyan]")
                    for var, val in variables.items():
                        console.print(f"  {var} = {val}")
                else:
                    console.print("[yellow]No variables stored[/yellow]")
                continue
            
            if '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
                parts = line.split('=', 1)
                var_name = parts[0].strip()
                var_value = parts[1].strip()
                
                try:
                    if var_value.replace('.','',1).replace('-','',1).isdigit():
                        variables[var_name] = float(var_value)
                    else:
                        variables[var_name] = var_value
                    console.print(f"[green]Variable '{var_name}' set to {variables[var_name]}[/green]")
                    continue
                except Exception as e:
                    console.print(f"[red]Error setting variable: {e}[/red]")
                    continue
            
            
            tokens = shlex.split(line)
            substituted_tokens = []
            for token in tokens:
                if token in variables:
                    substituted_tokens.append(str(variables[token]))
                else:
                    substituted_tokens.append(token)
            
            full = [category] + substituted_tokens
            args = parser.parse_args(full)
            execute_command(args, variables)
            
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            console.print(f"[bold red]An error has occurred: {e}[/bold red]")

def main():
    parser = safeargparser(description="A command-line advanced scientific calculator")
    sub = parser.add_subparsers(dest="command")

    basic = sub.add_parser("basic", aliases=["b"])
    basic.add_argument("operation", choices=["add", "sub", "div", "mul", "mod"])
    basic.add_argument("numbers", type=float, nargs="+")
    
    curr = sub.add_parser("curr", aliases=["cr"])
    curr.add_argument("update", choices=["upd"])

    cv = sub.add_parser("convert", aliases=["cv"])
    cv.add_argument("from_currency")
    cv.add_argument("to_currency")
    cv.add_argument("amount", type=float)

    adv = sub.add_parser("adv", aliases=["a"])
    adv.add_argument("operation", choices=[
        "sin", "cos", "tan", "arcsin", "arccos", "arctan",
        "sinh", "cosh", "tanh", "arcsinh", "arccosh", "arctanh",
        "log", "log10", "log2", "exp", "sqrt", "abs",
        "nth", "pow", "fact",
        "floor", "ceil", "round", "trunc", "sign",
        "mean", "median", "std", "var", "min", "max", "sum", "prod"
    ])
    adv.add_argument("numbers", type=float, nargs="+")

    vec = sub.add_parser("vector", aliases=["v"])
    vec.add_argument("operation", choices=["dot_product", "cross_product", "magnitude", "normalize", "angle_between"])
    vec.add_argument("components", type=float, nargs="+")

    phy = sub.add_parser("physics", aliases=["p"])
    phy.add_argument("operation", choices=["force", "kinetic_energy", "potential_energy", "ohms_law", "work", "speed", "acceleration"])
    phy.add_argument("args", type=float, nargs="+")

    units = sub.add_parser("units", aliases=["u"])
    units.add_argument("category", choices=["length", "mass", "temperature", "time", "speed"])
    units.add_argument("value", type=float)
    units.add_argument("from_unit")
    units.add_argument("to_unit")

    matrix = sub.add_parser("matrix", aliases=["m"])
    matrix.add_argument("operation", choices=["mul", "det", "inv", "eig", "transpose", "rank"])
    matrix.add_argument("m1")
    matrix.add_argument("--m2")

    comp = sub.add_parser("complex", aliases=["cx"])
    comp.add_argument("operation", choices=["add", "sub", "mul", "div", "mag", "phase", "polar", "rect"])
    comp.add_argument("c1")
    comp.add_argument("--c2")

    sym = sub.add_parser("symbolic", aliases=["s"])
    sym.add_argument("operation", choices=["simplify", "diff", "integrate", "solve", "expand", "factor"])
    sym.add_argument("expression")
    sym.add_argument("--variable", default="x")

    plot = sub.add_parser("plot", aliases=["pl"])
    plot.add_argument("operation", nargs='?', default="plot", choices=["plot"])
    plot.add_argument("function")
    plot.add_argument("--range", default="0,10")

    dim = sub.add_parser("dim", aliases=["d"])
    dim.add_argument("operation", choices=["evaluate_dim", "convert_dim"])
    dim.add_argument("expression", nargs="?")
    dim.add_argument("--value", type=float)
    dim.add_argument("--from_unit")
    dim.add_argument("--to_unit")

    pr = sub.add_parser("precise", aliases=["pr"])
    pr.add_argument("operation", choices=["add_fraction", "sub_fraction", "mul_fraction", "div_fraction", "add_decimal", "sub_decimal", "mul_decimal", "div_decimal"])
    pr.add_argument("n1")
    pr.add_argument("n2")
    pr.add_argument("--precision", type=int, default=28)

    cnv = sub.add_parser("convolve", aliases=["cnv"])
    cnv.add_argument("signal", type=float, nargs="+", help="Input signal values")
    cnv.add_argument("--kernel", "-k", type=float, nargs="+", required=True, help="Kernel values for convolution")

    sel = sub.add_parser("sel", aliases=["sh"])
    sel.add_argument("category", choices=[
        "basic", "b", 
        "adv", "a", 
        "curr", "cr", 
        "convert", "cv", 
        "vector", "v", 
        "physics", "p", 
        "units", "u",
        "matrix", "m",
        "complex", "cx",
        "symbolic", "s",
        "plot", "pl",
        "dim", "d",
        "precise", "pr",
        "convolve", "cnv"
    ])

    
    if len(sys.argv) > 1:
        if sys.argv[1] == "-changeCall" or sys.argv[1] == "--changeCall":
            if len(sys.argv) < 3:
                print("Usage: brliant_calc -changeCall <alias_name>")
                print("Example: brliant_calc -changeCall bcalc")
                sys.exit(1)
            
            from brliant_calc.alias_manager import create_alias
            alias_name = sys.argv[2]
            create_alias(alias_name)
            sys.exit(0)
        
        elif sys.argv[1] == "-removeAlias" or sys.argv[1] == "--removeAlias":
            if len(sys.argv) < 3:
                print("Usage: brliant_calc -removeAlias <alias_name>")
                sys.exit(1)
            
            from brliant_calc.alias_manager import remove_alias
            alias_name = sys.argv[2]
            remove_alias(alias_name)
            sys.exit(0)
        
        elif sys.argv[1] == "-listAliases" or sys.argv[1] == "--listAliases":
            from brliant_calc.alias_manager import list_aliases
            list_aliases()
            sys.exit(0)
        
        elif sys.argv[1] == "-runtests" or sys.argv[1] == "--runtests":
            import unittest
            import os
            tests_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
            if not os.path.exists(tests_dir):
                print("Error: tests directory not found")
                sys.exit(1)
            
            loader = unittest.TestLoader()
            suite = loader.discover(tests_dir, pattern='test_*.py')
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            sys.exit(0 if result.wasSuccessful() else 1)
        
        elif sys.argv[1] == "-version" or sys.argv[1] == "--version" or sys.argv[1] == "-v":
            try:
                from importlib.metadata import version
                print(f"brliant_calc version {version('brliant_calc')}")
            except Exception:
                print("brliant_calc version 2.1.2")
            sys.exit(0)
    
    try:
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(1)
        args = parser.parse_args()
        if args.command in ["sel", "sh"]:
            run_shell(args.category, parser)
        else:
            execute_command(args)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
