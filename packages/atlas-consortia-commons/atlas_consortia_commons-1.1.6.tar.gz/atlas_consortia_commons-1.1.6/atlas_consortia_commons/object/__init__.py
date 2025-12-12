import enum
from typing import Union
from atlas_consortia_commons.string import to_snake_case_upper, equals


def build_enum_class(class_name: str, data: Union[list, dict], prop_key: str = None, val_key: str = None,
                     prop_callback=to_snake_case_upper, val_callback=None,
                     obj_type: str = 'class', data_as_val: bool = False):
    _props = {}

    if val_key is None:
        val_key = prop_key

    def _populate_props(_item):
        prop = _item.get(prop_key)
        val = _item if data_as_val is True else _item.get(val_key)
        prop = prop if prop_callback is None else prop_callback(prop)
        _props[prop] = val if val_callback is None else val_callback(val)

    try:
        if type(data) is list:
            for item in data:
                _populate_props(item)
        else:
            if prop_key is not None:
                _populate_props(data)
            else:
                _props = data

        if equals(obj_type, 'enum'):
            return enum.Enum(class_name, _props)
        elif equals(obj_type, 'dict'):
            return _props
        elif equals(obj_type, 'list'):
            return list(_props.keys())
        else:
            return type(class_name, (), _props)
    except Exception as e:
        print(e)


def includes(data, keyword, as_list=True, insensitive=True, single_index=False):
    results = []
    for i, val in enumerate(data):
        if equals(val, keyword, insensitive):
            if as_list is True:
                results.append(i)
            else:
                return True

    if as_list and single_index:
        return results[0] if len(results) > 0 else -1

    return results if as_list is True else False


def enum_val_lower(member):
    val = member.value
    return val if val is None else val.lower()


def enum_val(member):
    return member.value
