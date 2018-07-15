# encoding: utf-8

from deepdiff import DeepDiff

from fact_extraction.run import extract_facts


DEFAULT_FACTS = {
    'places': [],
    'ipoteka': None,
    'price': None,
    'undefined_readable': '',
    'toilet': {'divided': None},
    'balcony': {'presence': None},
    'rooms': [],
    'size': {},
    'possible_places': []
}


def sort_dicts(jsn):
    if isinstance(jsn, dict):
        for k, v in jsn.items():
            sort_dicts(v)
    if isinstance(jsn, list):
        if jsn and all(isinstance(i, dict) for i in jsn):
            # Maybe to calculate common key and by it, not by hardcoded value?
            if all('id' in i for i in jsn):
                jsn.sort(key=lambda x: x['id'])
        for e in jsn:
            sort_dicts(e)


def have_json(tmpl, jsn, is_sort_dicts=True):
    if is_sort_dicts:
        sort_dicts(tmpl)
        sort_dicts(jsn)

    diff = DeepDiff(tmpl, jsn, ignore_order=True)
    if 'dictionary_item_added' in diff:
        del diff['dictionary_item_added']
    if 'iterable_item_added' in diff:
        del diff['iterable_item_added']
    return diff


def assert_have_json(tmpl, jsn, is_sort_dicts=True):
    print(tmpl)
    print(jsn)
    assert have_json(tmpl, jsn, is_sort_dicts=is_sort_dicts) == {}


def full_parse_message(message):
    facts = extract_facts(message)
    print(facts)
    return facts


def assert_parse_has(messsage, tmpl):
    jsn = full_parse_message(messsage)
    assert_have_json(tmpl, jsn)
