from robotransform.concepts import Variable, VectorDef, MatrixDef, TypeRef


def flatten_function_type(function_type):
    current = function_type
    linear = []

    while current is not None:
        linear.append(current.source)
        current = current.target

    function_type.source_chain = linear[:-1]
    function_type.final_target = linear[-1]
    return function_type


def flatten_product_type(obj):
    flat = [obj.types[0]] if obj.types else []
    for t in obj.types[1:]:
        flat.append(t)
    obj.flat_types = flat
    return obj


def flatten_variable_list(var_list_obj):
    flat_vars = []
    for variable in var_list_obj.variables:
        variable.modifier = var_list_obj.modifier
        flat_vars.append(variable)
    assert (len(flat_vars) == 1)  # TODO Is this always the case?
    return flat_vars[0]


def flatten_vector_type(obj):
    if isinstance(obj.source, VectorDef):
        obj.flattened = [obj.source.base]
    elif isinstance(obj.source, MatrixDef):
        obj.flattened = [obj.source.base]
    elif isinstance(obj.source, TypeRef):
        obj.flattened = [obj.source.type]
    return obj


def convert_variable_no_init(variable_no_init):
    return Variable(
        name=variable_no_init.name,
        type=variable_no_init.type,
        initial=None,
        parent=variable_no_init.parent
    )


processors = {
    "ProductType": flatten_product_type,
    "FunctionType": flatten_function_type,
    "VariableList": flatten_variable_list,
    "VariableNoInit": convert_variable_no_init,
    "VectorType": flatten_vector_type,
}
