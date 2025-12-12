import json
from functools import wraps


def AuditLogMobile():
    """
    Decorador que:
    - Lee el JSON del request GraphQL
    - Intenta limpiar y parsear el campo 'data' si viene como string
    - Deja los datos limpios en info.context["data_clean"]
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print("AuditLog decorator invoked")

            # Obtener "info" del resolver
            try:
                _, info = args[:2]
            except:
                return await func(*args, **kwargs)

            request = info.context.get("request")

            graphql_json = {
                "operationName": None,
                "query": None,
                "variables": None,
                "raw": None,
            }

            raw_data = None

            # Leer request json si existe
            if request:
                try:
                    body_bytes = await request.body()
                    body_str = body_bytes.decode("utf-8")
                    parsed = json.loads(body_str)

                    graphql_json["operationName"] = parsed.get("operationName")
                    graphql_json["query"] = parsed.get("query")
                    graphql_json["variables"] = parsed.get("variables")
                    graphql_json["raw"] = parsed

                    # Extraer "data" si viene dentro de variables
                    raw_data = parsed.get("variables", {}).get("data")

                except Exception:
                    pass

            # Procesar campo data si viene como string
            cleaned_data = raw_data

            if isinstance(raw_data, str):
                clean = raw_data.strip()

                # 1) Quitar comillas externas
                if (clean.startswith('"') and clean.endswith('"')) or (
                    clean.startswith("'") and clean.endswith("'")
                ):
                    clean = clean[1:-1]

                # 2) Reemplazar escapes de comillas
                clean = clean.replace('\\"', '"')

                # 3) Intentar convertir a JSON
                try:
                    cleaned_data = json.loads(clean)
                except Exception as e:
                    print("Error parsing:", e)
                    print("Cleaned data:", clean)
                    raise Exception("Invalid JSON format in 'data'")

            # Guardar el data limpio
            info.context["data_clean"] = cleaned_data

            return await func(*args, **kwargs)

        return wrapper

    return decorator
