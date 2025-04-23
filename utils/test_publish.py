import pandas as pd
from sheets.upload_to_sheets import publish_to_gsheets

# Crea un pequeño DataFrame de prueba
df_test = pd.DataFrame({
    'ticker': ['AAPL', 'MSFT', 'GOOG'],
    'return': [0.05, 0.03, -0.01]
})

# Nombre del tab donde vas a probar
test_tab = "test_tab"

# Llama a tu función de publicación
publish_to_gsheets(df_test, test_tab)

print("✅ Test publication completed.")