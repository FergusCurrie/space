import spacy

# Read markdown file in data/facts


def read_markdown_file(filename):
    with open(filename, "r") as f:
        return [x for x in f.read().split("\n") if x != ""]


filename = "data/facts/apache_beam.md"

markdown = read_markdown_file(filename)

nlp = spacy.load("en_core_web_sm")


for m in markdown:
    doc = nlp(m)

    print([token.text for token in doc])

    for token in doc:
        print(
            token.text,
            token.lemma_,
            token.pos_,
            token.tag_,
            token.dep_,
            token.shape_,
            token.is_alpha,
            token.is_stop,
        )

    for entity in doc.ents:
        print(entity.text, entity.label_)
    print("\n\n\n")
