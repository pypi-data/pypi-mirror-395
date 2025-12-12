from typing import Dict, Type, TypeVar, get_origin, get_args, Union
from dataclasses import fields, is_dataclass
from Osdental.Shared.Utils.CaseConverter import CaseConverter

T = TypeVar('T')

class Mapper:

    @staticmethod
    def map_data(data: Dict[str, any], model: Type[T]) -> T:
        if not is_dataclass(model):
            raise ValueError(f"Target model {model} is not a dataclass")

        mapped = {CaseConverter.case_to_snake(k): v for k, v in data.items()}
        instance_data = {}

        for field in fields(model):
            field_name = field.name
            field_type = field.type
            value = mapped.get(field_name)

            if value is None:
                continue  

            instance_data[field_name] = Mapper._map_value(value, field_type)

        return model(**instance_data)

    @staticmethod
    def _map_value(value: any, field_type: any):
        origin = get_origin(field_type)
        args = get_args(field_type)

        # Si es Optional[X]
        if origin is Union and type(None) in args:
            actual_type = next((arg for arg in args if arg is not type(None)), None)
            return Mapper._map_value(value, actual_type)

        # Si es List[X]
        if origin is list:
            item_type = args[0]
            if isinstance(value, list):
                return [
                    Mapper._map_value(item, item_type)
                    for item in value
                ]
            return value 

        # Si es dict y es un dataclass, lo procesamos
        if is_dataclass(field_type) and isinstance(value, dict):
            # Recursivo para dataclass anidados
            return Mapper.map_data(value, field_type)

        return value
