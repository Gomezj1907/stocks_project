# Navegar al directorio del proyecto
cd "C:\Users\jorge_j24fcle\OneDrive\Documentos\3. coding\Python\stocks_project"

# Crear entorno virtual llamado "stocks"
python -m venv stocks

# Activar entorno virtual
.\stocks\Scripts\Activate.ps1

# Crear requirements.txt con librerías necesarias
@"
yfinance
pandas
gspread
oauth2client
requests
beautifulsoup4
lxml
"@ | Out-File -Encoding UTF8 requirements.txt

# Instalar las dependencias
pip install -r requirements.txt
