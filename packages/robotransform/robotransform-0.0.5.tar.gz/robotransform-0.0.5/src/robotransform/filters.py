def type_to_port(_type) -> str:
    # TODO this is wrong
    if str(_type) in {"event", }:
        return "event"
    return "data"

def type_to_aadl_type(_type) -> str:
    typename = str(_type)
    # Boolean,
    # Character,
    # Float, Float_32, Float_64,
    # Integer, Integer_8, Integer_16, Integer_32, Integer_64,
    # Natural,
    # String,
    # Unsigned_8, Unsigned_16, Unsigned_32, Unsigned_64
    mapping = {
        "boolean": "Base_Types::Boolean",
        "nat"    : "Base_Types::Natural",
        "real"   : "Base_Types::Float",
    }
    # TODO Seq -> Array[...]
    # TODO Matrix to Array[Array[...]]
    # REASON: AADL does not support variable length arrays
    # TODO Very hacky, not correct
    if typename.startswith("[") and typename.endswith("]"):
        typename = typename[1:-1]
    elif "*" in typename:
        typename = typename.split("*")[0]
    return mapping.get(typename, f"messages::{typename}")
