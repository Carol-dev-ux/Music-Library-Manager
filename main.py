from cli import cli, prompt_user
from database import init_db

if __name__ == "__main__":
    init_db()
    prompt_user()
    cli()
   
