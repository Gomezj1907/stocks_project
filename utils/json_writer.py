import json
import os


def update_json(data_to_add: dict, json_path: str = "data/tickers_por_pais.json") -> None:
    """
    Actualiza o agrega nuevas claves al JSON existente sin borrar lo anterior.

    Args:
        data_to_add (dict): Diccionario parcial con datos nuevos.
        json_path (str): Ruta al archivo .json.
    """
    if not os.path.exists(json_path) or os.stat(json_path).st_size == 0:
        data = {}
    else:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    # Mezclar lo nuevo con lo existente
    for country, indices in data_to_add.items():
        if country not in data:
            data[country] = indices
        else:
            data[country].update(indices)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)