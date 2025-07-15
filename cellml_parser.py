# cellml_parser.py

import libcellml

def load_cellml_model_from_file(file_path):
    """Load and parse a CellML model from a file using libcellml."""
    parser = libcellml.Parser()
    parser.setStrict(False)  # Disable strict mode to allow parsing with warnings
    with open(file_path, 'r', encoding='utf-8') as f:
        cellml_text = f.read()

    print("[Debug] First 200 chars of CellML file:\n", cellml_text[:200])  # Debugging line to check file content
    model = parser.parseModel(cellml_text)

    if parser.issueCount() > 0:
        print("[Warning] Issues found during parsing:")
        for i in range(parser.issueCount()):
            print(f"  - {parser.issue(i).description()}")

    #if model.isValid():
    #    return model
    #else:
    #    raise ValueError("Failed to parse valid CellML model.")
    return model  # Return the model even if it has issues for further processing

def get_model_name(model):
    return model.name()

def extract_variable_names(model):
    """Extract variables from all components in the model."""
    variables = []

    print(f"[Debug] Model has {model.componentCount()} components.")
    for i in range(model.componentCount()):
        component = model.component(i)
        component_name = component.name()

        for j in range(component.variableCount()):
            var = component.variable(j)
            units = var.units()
            if not isinstance(units, str):
                units = units.name()
            var_data = {
                "component": component_name,
                "name": var.name(),
                "units": units,
                "initial_value": var.initialValue(),
                "cmeta_id": var.id()
            }
            variables.append(var_data)

    return variables


def extract_equations(model):
    """
    Placeholder for extracting mathematical expressions.
    libcellml stores them in mathml strings — more advanced parsing needed.
    """
    equations = []

    for i in range(model.componentCount()):
        component = model.component(i)
        mathml = component.math()
        if mathml:
            equations.append({
                "component": component.name(),
                "mathml": mathml
            })

    return equations


def summarize_model(file_path):
    """High-level summary for debugging or inspection."""
    model = load_cellml_model_from_file(file_path)
    print(f"Model Name: {get_model_name(model)}")

    print("\n[Variables]")
    for v in extract_variable_names(model):
        print(f" - {v['component']}.{v['name']} (units: {v['units']}, init: {v['initial_value']}, cmeta_id: {v['cmeta_id']})")

    print("\n[MathML Equations Found]")
    for eq in extract_equations(model):
        print(f" - Component: {eq['component']}, MathML Length: {len(eq['mathml'])} characters")

    return model


# Optional CLI test
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cellml_parser.py path_to_model.cellml")
    else:
        summarize_model(sys.argv[1])
