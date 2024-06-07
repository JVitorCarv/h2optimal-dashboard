import requests
import pandas as pd

DATABASE_URL = "https://kieza-da3c7-default-rtdb.firebaseio.com/"
DATABASE_SECRET = "jwBmBsvKeK0MzfzGk5Bi42PPgeAhDWALwQGQP71K"
COLLECTION = "log"


def get_data_from_firebase():
    url = f'{DATABASE_URL}/{COLLECTION}.json?auth={DATABASE_SECRET}&orderBy="$key"'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data is None:
            return pd.DataFrame()
        sorted_data = sorted(data.items(), key=lambda x: x[0])
        last_entries = sorted_data[-500:]
        processed_data = []
        for _, value in last_entries:
            parts = value.split()
            data_dict = {}
            if len(parts) > 0:
                data_dict["calc"] = parts[0]
            else:
                data_dict["calc"] = None
            if len(parts) > 1:
                data_dict["umidade"] = parts[1]
            else:
                data_dict["umidade"] = None
            if len(parts) > 2:
                data_dict["controle"] = parts[2]
            else:
                data_dict["controle"] = None
            processed_data.append(data_dict)
        df = pd.DataFrame(processed_data)
        df["calc"] = pd.to_numeric(df["calc"], errors="coerce")
        df["umidade"] = pd.to_numeric(df["umidade"], errors="coerce")
        df["controle"] = pd.to_numeric(df["controle"], errors="coerce")
        df.ffill(inplace=True)
        return df
    else:
        return pd.DataFrame()
