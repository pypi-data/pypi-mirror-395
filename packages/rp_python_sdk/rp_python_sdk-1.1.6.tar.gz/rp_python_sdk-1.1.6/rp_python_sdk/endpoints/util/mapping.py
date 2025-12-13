from typing import Type, TypeVar, Union, List, get_type_hints

T = TypeVar('T')


def snake_to_pascal(name: str) -> str:
    """
    Converts a snake_case string to PascalCase.
    Example: organisation_id -> OrganisationId
    """
    return ''.join(word.capitalize() for word in name.split('_'))


def from_dict(data_class: Type[T], data: Union[dict, list], pascal_case: bool = False) -> Union[T, List[T]]:
    """
    Recursively maps a dictionary or a list of dictionaries to a dataclass or a list of dataclasses.
    Handles key transformations from snake_case to PascalCase, and resolves forward references.
    """
    if isinstance(data, list):
        # Map each item in the list to the dataclass
        return [from_dict(data_class, item, pascal_case) for item in data]

    if not isinstance(data, dict):
        raise ValueError(
            f"Expected a dictionary to map to {data_class.__name__}, but got {type(data).__name__}: {data}")

    # Get the fields of the dataclass, resolving forward references
    fieldtypes = get_type_hints(data_class)

    # Prepare the arguments for the dataclass constructor
    data_class_kwargs = {}
    for field, field_type in fieldtypes.items():
        # Convert the snake_case field name to PascalCase to match the JSON key
        json_field = field
        if pascal_case:
            json_field = snake_to_pascal(field)

        # Fetch the corresponding value from the JSON data
        field_value = data.get(json_field)

        if isinstance(field_value, list):
            inner_type = field_type.__args__[0]
            data_class_kwargs[field] = [from_dict(inner_type, item, pascal_case) if isinstance(item, dict) else item for
                                        item in field_value]
        elif isinstance(field_value, dict):
            data_class_kwargs[field] = from_dict(field_type, field_value, pascal_case)
        else:
            # Handle authorisation_servers case
            if field == "authorisation_servers" and field_value is None:
                data_class_kwargs[field] = []
            else:
                data_class_kwargs[field] = field_value

    return data_class(**data_class_kwargs)
