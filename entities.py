import csv
import sys
from KafNafParserPy import KafNafParser

from naflib import *
from naflib import sort_terms

woorden = [r['original'] for r in csv.DictReader(open("klimaatwoorden.csv"))]

o = csv.writer(sys.stdout)
o.writerow(["file", "sentence", "entity", "type", "dbpedia", "text"])
for fn in sys.argv[1:]:
    naf = KafNafParser(fn)
    for e in naf.get_entities():
        for ref in e.get_references():
            terms = sort_terms(naf, [naf.get_term(t.get_id()) for t in ref.get_span()])
            o.writerow([fn, get_sentence(naf, terms[0]), e.get_id(), e.get_type(), " ".join(t.get_lemma() for t in terms)])
