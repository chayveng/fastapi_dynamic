# Fastapi Dynamic
| Auto create router

## StartUp

- Creating a Virtual Environment and Activate 
```bash
# Create venv 
python -m venv .venv 

# Activate venv on Linux
source .venv/bin/activate

# Activate venv on Windows
.venv/Script/activate
```

- Install packages
```bash
pip install -r requirements.txt
```

- Start FastAPI
```bash
# After activate venv
uvicorn main:app --host 0.0.0.0 --port 5050 --reload

# Or run from run.sh: linux
sh run.sh 
```

## Install packages 
```bash
pip install <PACKAGE_NAME>

# Freeze after install new packages
pip freeze > requirements.txt
```
