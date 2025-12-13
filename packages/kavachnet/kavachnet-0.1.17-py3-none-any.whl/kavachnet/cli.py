import sys
from streamlit.web import cli as st_cli
from pathlib import Path

def main():
    app_path = Path(__file__).parent / "app.py"
    # We need to set the arguments for streamlit
    # The first argument is the script name (streamlit), the second is the command (run), the third is the file
    sys.argv = ["streamlit", "run", str(app_path)] + sys.argv[1:]
    sys.exit(st_cli.main())

if __name__ == "__main__":
    main()
