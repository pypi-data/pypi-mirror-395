from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(".env", override=True)

