import functions_framework

@functions_framework.http
def analyze_jump_cloud(request):
    # ഇതാണ് പുതിയ കോഡ് - ഇതിൽ ടേബിൾ ഫോർമാറ്റ് ഇല്ല!
    d = request.get_json(silent=True) or {}
    
    # പവർഷെല്ലിൽ നിന്ന് വരുന്ന ഡാറ്റ എടുക്കുന്നു
    val1 = d.get('a', 'No Data')
    val2 = d.get('c', 'No Data')

    return {
        "message": "NK, we found the data!",
        "received_a": val1,
        "received_c": val2,
        "full_data": d
    }
