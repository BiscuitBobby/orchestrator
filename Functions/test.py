import json


def get_test_info(component_name: str):
    component_info = {
        "name": component_name,
        "price": "10.99",
    }
    return json.dumps(component_info)


test = {
    "name": "get_test_info",
    "description": "Get name and price of a computer component",
    "parameters": {
        "type": "object",
        "properties": {
            "component_name": {
                "type": "string",
                "description": "The name of the component, e.g. graphics card, tpm chip, processor",
            },
        },
        "required": ["component_name"],
    },
}
