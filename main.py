# main.py

import argparse
from cellml_parser import extract_variable_names, load_cellml_model_from_file
from pdf_parser import extract_relevant_sentences


def main(cellml_file, pdf_file):
    print(f"🔍 Parsing CellML file: {cellml_file}")
    model = load_cellml_model_from_file(cellml_file)  # Parse the file to get the model
    variables = extract_variable_names(model)  # Pass the model, not the file path
    print(f"✅ Found {len(variables)} variables:")
    for v in variables:
        print(f"  - {v['component']}.{v['name']} (units: {v['units']}, init: {v['initial_value']}, cmeta_id: {v['cmeta_id']})")

    print(f"\n📖 Parsing PDF file: {pdf_file}")
    keywords = [v['name'] for v in variables]  # Use variable names as keywords
    sentences = extract_relevant_sentences(pdf_file, keywords=keywords)
    print(f"\n📑 Matched Sentences ({len(sentences)}):")
    for s in sentences:
        print(f"  - {s.strip()}")

    # 🔧 Placeholder for variable-sentence linking
    print("\n[🚧 Next Step] Match variables to most relevant sentence (NLP embedding model)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic Annotation Assistant")
    parser.add_argument("cellml", type=str, help="Path to CellML file")
    parser.add_argument("pdf", type=str, help="Path to research paper PDF")

    args = parser.parse_args()
    main(args.cellml, args.pdf)
