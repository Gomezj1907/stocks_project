# Navegar al directorio raíz del proyecto
cd "C:\Users\jorge_j24fcle\OneDrive\Documentos\3. coding\Python\stocks_project"

# Crear estructura de carpetas
New-Item -ItemType Directory -Path "scraping"
New-Item -ItemType Directory -Path "data"
New-Item -ItemType Directory -Path "analysis"
New-Item -ItemType Directory -Path "sheets"
New-Item -ItemType Directory -Path "config"

# Crear archivos base vacíos
New-Item -ItemType File -Path "main.py"
New-Item -ItemType File -Path "scraping\dow_jones.py"
New-Item -ItemType File -Path "scraping\sp500.py"
New-Item -ItemType File -Path "scraping\nikkei.py"
New-Item -ItemType File -Path "scraping\sti.py"
New-Item -ItemType File -Path "scraping\ftse.py"
New-Item -ItemType File -Path "analysis\performance.py"
New-Item -ItemType File -Path "sheets\upload_to_sheets.py"
New-Item -ItemType File -Path "data\tickers_por_pais.json"
New-Item -ItemType File -Path "config\credentials.json"