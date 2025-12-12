import json
from functools import wraps


def AuditLogMobile():
    """
    Decorador que:
    - Lee el body del request (GraphQL)
    - Extrae y limpia el campo "data" si viene como string o escapado
    - Reemplaza automáticamente el argumento `data` del resolver
    - Guarda el data limpio en info.context["data_clean"]
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            # Obtener "info" (args[1] siempre es info en resolvers GraphQL)
            try:
                info = args[1]
            except Exception:
                # Si algo falla, ejecutar igual
                return await func(*args, **kwargs)

            request = info.context.get("request")
            raw_data_from_request = None

            # ===============================
            # 1. Leer JSON crudo del request
            # ===============================
            if request:
                try:
                    body_bytes = await request.body()
                    body_str = body_bytes.decode("utf-8")
                    parsed_body = json.loads(body_str)

                    # Si hay variables y dentro de ellas viene "data"
                    raw_data_from_request = parsed_body.get("variables", {}).get("data")

                except Exception:
                    pass

            # ===============================
            # 2. Obtener el data enviado al resolver
            # ===============================
            original_data = kwargs.get("data")
            cleaned_data = original_data

            # ===============================
            # 3. Decidir cuál "data" procesar
            # ===============================
            candidate = (
                raw_data_from_request
                if raw_data_from_request is not None
                else original_data
            )

            # ===============================
            # 4. Limpiar/parsear JSON si viene como str
            # ===============================
            if isinstance(candidate, str):
                temp = candidate.strip()

                # Quitar comillas externas
                if (temp.startswith('"') and temp.endswith('"')) or (
                    temp.startswith("'") and temp.endswith("'")
                ):
                    temp = temp[1:-1]

                # Reemplazar escapes
                temp = temp.replace('\\"', '"')

                try:
                    cleaned_data = json.loads(temp)
                except Exception as e:
                    print("Error al parsear JSON en data:", e)
                    print("Cadena que falló:", temp)
                    raise Exception("El campo 'data' tiene un JSON inválido.")

            else:
                cleaned_data = candidate

            # ===============================
            # 5. Guardar data limpio para auditoría
            # ===============================
            info.context["data_clean"] = cleaned_data

            # ===============================
            # 6. Reemplazar argumento `data`
            # ===============================
            kwargs["data"] = cleaned_data

            # ===============================
            # 7. Ejecutar función original
            # ===============================
            return await func(*args, **kwargs)

        return wrapper

    return decorator
