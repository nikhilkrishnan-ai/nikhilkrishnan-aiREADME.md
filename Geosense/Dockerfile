FROM python:3.10-slim

# വർക്കിംഗ് ഡയറക്ടറി സെറ്റ് ചെയ്യുന്നു
WORKDIR /app

# ആവശ്യമായ പാക്കേജുകൾ ഇൻസ്റ്റാൾ ചെയ്യുന്നു
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# നമ്മുടെ കോഡ് മുഴുവൻ കോപ്പി ചെയ്യുന്നു
COPY . .

# വെബ്‌ഹൂക്ക് 8080 പോർട്ടിൽ റൺ ചെയ്യാൻ പറയുന്നു
CMD ["uvicorn", "webhook_main:app", "--host", "0.0.0.0", "--port", "8080"]
