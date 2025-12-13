#!/usr/bin/env python3
"""Generate math problems file(s) for repeat pattern testing.

Creates one or more text files with varied math problems (one per line) that can be used
to test the repeat pattern with math problem solver pipeline.

Problem types generated:
- Simple expression-based: "What is 15 + 27?"
- Word problems: "Sarah has 15 books. She buys 27 more. How many books does she have now?"
- Medium complexity: "What is 15 + 27 - 10?" (multiple operations)
- Complex expressions: "What is (15 + 27) * 3?" (with parentheses)

Usage:
    # Single file
    python scripts/generate_math_problems.py [--count <n>] [--output <path>]
    
    # Multiple files
    python scripts/generate_math_problems.py [--file-count <n>] [--problems-per-file <n>] [--output-dir <path>]
    
    uv run -m scripts.generate_math_problems --count 5 --output projects/ensemble/data/repeat/math_problems.txt
    uv run -m scripts.generate_math_problems --file-count 3 --problems-per-file 5 --output-dir projects/ensemble/data/repeat/
"""

import os
import sys
import argparse
import random
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def generate_simple_expression_problem(num1: int, num2: int, op_symbol: str) -> str:
    """Generate a simple expression-based problem."""
    return f"What is {num1} {op_symbol} {num2}?"


def generate_word_problem(num1: int, num2: int, op_symbol: str) -> str:
    """Generate a word-based problem."""
    word_problems = {
        "+": [
            f"Sarah has {num1} books. She buys {num2} more. How many books does she have now?",
            f"A store has {num1} items in stock. They receive {num2} more items. What is the total?",
            f"Tom collected {num1} stamps. His friend gave him {num2} more. How many stamps does Tom have?",
        ],
        "-": [
            f"Emma had {num1} cookies. She ate {num2} of them. How many cookies are left?",
            f"There were {num1} students in a class. {num2} students left. How many students remain?",
            f"Mike had ${num1}. He spent ${num2}. How much money does he have left?",
        ],
        "*": [
            f"Each box contains {num2} apples. If there are {num1} boxes, how many apples are there in total?",
            f"A car travels {num2} miles per hour. How far will it travel in {num1} hours?",
            f"Each pack has {num2} pencils. How many pencils are in {num1} packs?",
        ],
        "/": [
            f"{num1} apples are divided equally among {num2} baskets. How many apples are in each basket?",
            f"A {num1}-mile journey is divided into {num2} equal segments. How long is each segment?",
            f"{num1} students are split into {num2} equal groups. How many students are in each group?",
        ],
    }
    
    if op_symbol in word_problems:
        return random.choice(word_problems[op_symbol])
    return f"What is {num1} {op_symbol} {num2}?"


def generate_medium_expression_problem() -> str:
    """Generate a medium complexity expression (two operations)."""
    num1 = random.randint(10, 50)
    num2 = random.randint(5, 30)
    num3 = random.randint(5, 20)
    
    patterns = [
        f"What is {num1} + {num2} - {num3}?",
        f"What is {num1} - {num2} + {num3}?",
        f"What is {num1} * {num2} + {num3}?",
        f"What is {num1} + {num2} * {num3}?",
    ]
    
    return random.choice(patterns)


def generate_complex_expression_problem() -> str:
    """Generate a complex expression (multiple operations with parentheses)."""
    num1 = random.randint(10, 30)
    num2 = random.randint(5, 20)
    num3 = random.randint(5, 15)
    num4 = random.randint(2, 10)
    
    patterns = [
        f"What is ({num1} + {num2}) * {num3}?",
        f"What is {num1} * ({num2} + {num3})?",
        f"What is ({num1} - {num2}) * {num3} + {num4}?",
        f"What is {num1} + {num2} * {num3} - {num4}?",
    ]
    
    return random.choice(patterns)


def generate_math_problems(count: int = 3) -> list:
    """Generate math problems with varying complexity and formats.
    
    Args:
        count: Number of problems to generate
        
    Returns:
        List of problem strings in format "Problem N: <problem text>"
    """
    problems = []
    operations = [
        ("+", lambda a, b: a + b),
        ("-", lambda a, b: a - b),
        ("*", lambda a, b: a * b),
        ("/", lambda a, b: a // b if b != 0 else a),
    ]
    
    # Define problem types with weights for variety
    problem_types = [
        ("simple_expression", 0.3),  # 30% simple expression-based
        ("word", 0.3),                # 30% word problems
        ("medium_expression", 0.25),   # 25% medium complexity
        ("complex_expression", 0.15), # 15% complex expressions
    ]
    
    for i in range(count):
        # Choose problem type based on weights
        rand = random.random()
        cumulative = 0
        problem_type = "simple_expression"  # default
        
        for ptype, weight in problem_types:
            cumulative += weight
            if rand <= cumulative:
                problem_type = ptype
                break
        
        if problem_type == "simple_expression":
            # Simple expression-based problem
            num1 = random.randint(10, 99)
            num2 = random.randint(1, 50)
            op_symbol, _ = random.choice(operations)
            
            if op_symbol == "/":
                num1 = num2 * random.randint(2, 10)
            
            problem_text = generate_simple_expression_problem(num1, num2, op_symbol)
            
        elif problem_type == "word":
            # Word-based problem
            num1 = random.randint(10, 99)
            num2 = random.randint(1, 50)
            op_symbol, _ = random.choice(operations)
            
            if op_symbol == "/":
                num1 = num2 * random.randint(2, 10)
            elif op_symbol == "*":
                # For multiplication word problems, keep numbers smaller
                num1 = random.randint(2, 20)
                num2 = random.randint(2, 15)
            
            problem_text = generate_word_problem(num1, num2, op_symbol)
            
        elif problem_type == "medium_expression":
            # Medium complexity expression
            problem_text = generate_medium_expression_problem()
            
        else:  # complex_expression
            # Complex expression with parentheses
            problem_text = generate_complex_expression_problem()
        
        problems.append(f"Problem {i + 1}: {problem_text}")
    
    return problems


def main():
    parser = argparse.ArgumentParser(description="Generate math problems file(s) for repeat pattern testing")
    parser.add_argument(
        "--count",
        type=int,
        default=None,
        help="Number of math problems to generate for single file mode (default: 3)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path for single file mode (default: projects/ensemble/data/repeat/math_problems.txt)"
    )
    parser.add_argument(
        "--file-count",
        type=int,
        default=None,
        help="Number of files to generate (for multi-file mode)"
    )
    parser.add_argument(
        "--problems-per-file",
        type=int,
        default=3,
        help="Number of problems per file (for multi-file mode, default: 3)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="projects/ensemble/data/repeat",
        help="Output directory for multi-file mode (default: projects/ensemble/data/repeat)"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["single", "multi"],
        default=None,
        help="Mode: 'single' for single file, 'multi' for multiple files (default: interactive prompt)"
    )
    
    args = parser.parse_args()
    
    # Determine mode: single file or multi-file
    # Priority: 1. --mode flag, 2. --file-count presence, 3. interactive prompt
    if args.mode:
        multi_file_mode = (args.mode == "multi")
    elif args.file_count is not None:
        multi_file_mode = True
    elif sys.stdin.isatty():
        # Interactive mode selection
        print("\n" + "=" * 70)
        print("Math Problem Generator")
        print("=" * 70)
        print("\nSelect mode:")
        print("  1. Multi-file mode (generate multiple files) [default]")
        print("  2. Single file mode (generate one file)")
        print("\nPress Enter for multi-file mode, or type '1' or '2':")
        try:
            user_choice = input("> ").strip().lower()
            if user_choice in ['', '1', 'multi']:
                multi_file_mode = True
            elif user_choice in ['2', 'single']:
                multi_file_mode = False
            else:
                print("⚠ Invalid choice. Using default: multi-file mode")
                multi_file_mode = True
        except (EOFError, KeyboardInterrupt):
            print("\n⚠ Using default: multi-file mode")
            multi_file_mode = True
    else:
        # Non-interactive: default to multi-file mode
        multi_file_mode = True
    
    if multi_file_mode:
        # Multi-file mode
        file_count = args.file_count if args.file_count is not None else 3
        problems_per_file = args.problems_per_file
        output_dir = Path(args.output_dir)
        
        if sys.stdin.isatty():  # Only prompt if running interactively
            if not args.mode and args.file_count is None:
                # Already showed header above, just show mode-specific header
                print("\n" + "-" * 70)
                print("Multi-File Mode")
                print("-" * 70)
            else:
                print("\n" + "=" * 70)
                print("Math Problem Generator - Multi-File Mode")
                print("=" * 70)
            print(f"\nNumber of files to generate: {file_count}")
            print("Press Enter to use this count, or type a different number:")
            try:
                user_count = input("> ").strip()
                if user_count:
                    try:
                        file_count = int(user_count)
                        if file_count < 1:
                            print("⚠ Invalid count (must be >= 1). Using default: 3")
                            file_count = 3
                    except ValueError:
                        print("⚠ Invalid number. Using default: 3")
                        file_count = 3
            except (EOFError, KeyboardInterrupt):
                print("\n⚠ Using provided file count")
            
            print(f"\nProblems per file: {problems_per_file}")
            print("Press Enter to use this count, or type a different number:")
            try:
                user_count = input("> ").strip()
                if user_count:
                    try:
                        problems_per_file = int(user_count)
                        if problems_per_file < 1:
                            print("⚠ Invalid count (must be >= 1). Using default: 3")
                            problems_per_file = 3
                    except ValueError:
                        print("⚠ Invalid number. Using default: 3")
                        problems_per_file = 3
            except (EOFError, KeyboardInterrupt):
                print("\n⚠ Using provided problems per file")
        else:
            print(f"\nFile count: {file_count} (non-interactive mode)")
            print(f"Problems per file: {problems_per_file} (non-interactive mode)")
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if files exist and warn
        existing_files = []
        for i in range(file_count):
            file_path = output_dir / f"file_{i}.txt"
            if file_path.exists():
                existing_files.append(file_path)
        
        if existing_files and sys.stdin.isatty():
            print(f"\n⚠ {len(existing_files)} file(s) already exist:")
            for f in existing_files[:5]:  # Show first 5
                print(f"  - {f}")
            if len(existing_files) > 5:
                print(f"  ... and {len(existing_files) - 5} more")
            print("This will overwrite existing files.")
            try:
                confirm = input("Continue? (y/N): ").strip().lower()
                if confirm != 'y':
                    print("Cancelled.")
                    return 0
            except (EOFError, KeyboardInterrupt):
                print("\n⚠ Cancelled.")
                return 0
        
        # Generate files
        print(f"\nGenerating {file_count} files with {problems_per_file} problems each...")
        generated_files = []
        
        for i in range(file_count):
            file_path = output_dir / f"file_{i}.txt"
            problems = generate_math_problems(problems_per_file)
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for problem in problems:
                        f.write(problem + "\n")
                
                generated_files.append(file_path)
                print(f"✓ Generated {len(problems)} problems in {file_path.name}")
            except Exception as e:
                print(f"✗ Failed to write {file_path}: {e}")
                return 1
        
        print(f"\n✓ Generated {len(generated_files)} files in: {output_dir}")
        print("\nFiles generated:")
        for file_path in generated_files:
            print(f"  - {file_path}")
        
        return 0
    else:
        # Single file mode (backward compatible)
        problem_count = args.count if args.count is not None else 3
        output_path = Path(args.output) if args.output else Path("projects/ensemble/data/repeat/math_problems.txt")
        
        if sys.stdin.isatty():  # Only prompt if running interactively
            if not args.mode and args.count is None:
                # Already showed header above, just show mode-specific header
                print("\n" + "-" * 70)
                print("Single File Mode")
                print("-" * 70)
            else:
                print("\n" + "=" * 70)
                print("Math Problem Generator - Single File Mode")
                print("=" * 70)
            print(f"\nNumber of problems to generate: {problem_count}")
            print("Press Enter to use this count, or type a different number:")
            try:
                user_count = input("> ").strip()
                if user_count:
                    try:
                        problem_count = int(user_count)
                        if problem_count < 1:
                            print("⚠ Invalid count (must be >= 1). Using default: 3")
                            problem_count = 3
                    except ValueError:
                        print("⚠ Invalid number. Using default: 3")
                        problem_count = 3
            except (EOFError, KeyboardInterrupt):
                print("\n⚠ Using default problem count")
        else:
            print(f"\nProblem count: {problem_count} (non-interactive mode)")
        
        # Confirm output file
        if sys.stdin.isatty():  # Only prompt if running interactively
            print(f"\nOutput file: {output_path}")
            print("Press Enter to use this file, or type a different path:")
            try:
                user_path = input("> ").strip()
                if user_path:
                    output_path = Path(user_path)
            except (EOFError, KeyboardInterrupt):
                print("\n⚠ Using default output path")
        else:
            print(f"\nOutput file: {output_path} (non-interactive mode)")
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists and warn
        if output_path.exists() and sys.stdin.isatty():
            print(f"\n⚠ File already exists: {output_path}")
            print("This will overwrite the existing file.")
            try:
                confirm = input("Continue? (y/N): ").strip().lower()
                if confirm != 'y':
                    print("Cancelled.")
                    return 0
            except (EOFError, KeyboardInterrupt):
                print("\n⚠ Cancelled.")
                return 0
        
        # Generate problems
        print(f"\nGenerating {problem_count} math problems...")
        problems = generate_math_problems(problem_count)
        
        # Write to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for problem in problems:
                    f.write(problem + "\n")
            
            print(f"✓ Generated {len(problems)} math problems")
            print(f"✓ Saved to: {output_path}")
            print("\nProblems generated:")
            for problem in problems:
                print(f"  - {problem}")
            
            return 0
        except Exception as e:
            print(f"✗ Failed to write file: {e}")
            return 1


if __name__ == "__main__":
    sys.exit(main())

