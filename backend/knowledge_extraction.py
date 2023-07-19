import spacy

text = "the downside of single sample estimator is that it has high variance because it only uses one sample"

nlp = spacy.load("en_core_web_sm")

doc = nlp(text)

for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)
