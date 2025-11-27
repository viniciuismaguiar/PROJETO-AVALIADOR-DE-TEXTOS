"""Entry point at project root to run the evaluator easily.

Use either:
  python main.py
or
  python -m main

This will import `data.main` as a package and call its `main()` function.
"""
try:
    from data.main import main
except Exception:
    # Fallback: try importing directly if package imports are not working
    from data import main as main_module
    main = main_module.main

if __name__ == "__main__":
    main()
