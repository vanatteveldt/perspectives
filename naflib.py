from typing import Sequence, Iterable, List

from KafNafParserPy import KafNafParser, Cterm, Cwf


def sort_tokens(tokens: Iterable[Cwf]) -> List[Cwf]:
    """Sort tokens by natural order (sent, offset)"""
    return sorted(tokens,  key=lambda t: (t.get_sent(), int(t.get_offset())))


def sort_terms(naf: KafNafParser, terms: Iterable[Cterm]) -> List[Cterm]:
    """Sort terms by natural order (sent, offset)"""
    def get_offset(term: Cterm):
        tokens = [naf.get_token(tid) for tid in naf.get_dict_tokens_for_termid(term.get_id())]
        token = sort_tokens(tokens).pop()
        return token.get_sent(), int(token.get_offset())
    return sorted(terms, key=get_offset)


def get_word(naf: KafNafParser, term: Cterm) -> str:
    """Get the word(s) belonging to a term, joining them if there's more than one"""
    tokenids = naf.get_dict_tokens_for_termid(term.get_id())
    tokens = sort_tokens(naf.get_token(tid) for tid in tokenids)
    return " ".join(t.get_text() for t in tokens)


def find_terms(naf: KafNafParser, words: Sequence[str]) -> Iterable[Cterm]:
    """Find all terms whose lemma or word form is in the list of words"""
    for t in naf.get_terms():
        if t.get_lemma() in words or get_word(naf, t) in words:
            yield t


def get_sentence(naf: KafNafParser, term: Cterm) -> int:
    tokens = [naf.get_token(tid) for tid in naf.get_dict_tokens_for_termid(term.get_id())]
    sent = {t.get_sent() for t in tokens}
    if len(sent) != 1:
        raise Exception(f"Term {term.get_id}:{term.get_lemma()} did not map to single sentence: {sent}")
    return sent.pop()


def get_terms_in_sentence(naf: KafNafParser, sent: int) -> Iterable[Cterm]:
    tokens = sort_tokens(t for t in naf.get_tokens() if t.get_sent() == sent)
    tokenids = [t.get_id() for t in tokens]
    return sort_terms(naf, [naf.get_term(tid) for tid in naf.map_tokens_to_terms(tokenids)])