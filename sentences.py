import csv
import sys
from KafNafParserPy import KafNafParser

from naflib import *

woorden = [r['original'] for r in csv.DictReader(open("klimaatwoorden.csv"))]

o = csv.writer(sys.stdout)
o.writerow(["file", "sentence", "term", "text"])
for fn in sys.argv[1:]:
    naf = KafNafParser(fn)

    for klimaterm in find_terms(naf, woorden):
        sent = get_sentence(naf, klimaterm)
        text = " ".join([get_word(naf, t) for t in get_terms_in_sentence(naf, sent)])
        o.writerow([fn, sent, klimaterm.get_lemma(), text])

