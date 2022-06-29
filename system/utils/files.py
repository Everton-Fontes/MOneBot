import json
import logging


async def load_file(file, debug=True):
    try:

        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        if debug:
            logging.warning(
                "Por favor, crie o arquivo %s para podermos ler", file)
        else:
            pass


async def save_file(file, data: dict):
    try:
        with open(file, "w") as f:
            f.write(json.dumps(data))
    except Exception as e:
        logging.warning("Não foi possivel salvar o arquivo %s", e)
