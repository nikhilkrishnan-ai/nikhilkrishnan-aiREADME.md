import pandas as pd
from azure.identity import DefaultAzureCredential

# 💡 നിന്റെ ആ പഴയ വൺലേക്ക് പാത്ത് ഇവിടെ തന്നെ വെക്കുക
onelake_path = "abfss://Your_Workspace_ID@onelake.dfs.fabric.microsoft.com/Your_Lakehouse_ID/Files/geosense_anomaly_report.csv"

print("⏳ മിനി പിസിയിലെ ലേക്ക്ഹൗസിൽ നിന്ന് ജിപിഎസ് ഫയൽ നേരിട്ട് എടുക്കുന്നു...")

try:
    # 1. ലാപ്ടോപ്പിൽ ഓട്ടോമാറ്റിക് ലോഗിൻ സെറ്റ് ചെയ്യുന്നു (Browser വഴി)
    credential = DefaultAzureCredential()
    
    # 2. വൺലേക്ക് ലോഗിൻ വിവരങ്ങൾ കൂടി പാണ്ഡാസിന് കൈമാറുന്നു
    storage_options = {"credential": credential}
    
    # 3. ഡാറ്റ വായിക്കുന്നു
    df = pd.read_csv(onelake_path, storage_options=storage_options)
    print("✅ ഡാറ്റ പക്കാ ആയിട്ട് ലോഡ് ചെയ്തു Nk ചക്കരേ!\n")
    
    print("--- ജിപിഎസ് ഡാറ്റാ ടേബിൾ ---")
    print(df.head().to_string())

except Exception as e:
    print("❌ കണക്ഷൻ ലോക്കാണ് മുത്തേ! എറർ ഇതാണ്:", e)