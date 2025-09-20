from functools import reduce
import operator
from typing import TYPE_CHECKING, Tuple, Union

import spacy

from django.db.models import QuerySet, Q

if TYPE_CHECKING:
    from things.models import Thing

# Load the English language model
nlp = spacy.load("en_core_web_sm")


def process_command(command: str) -> Tuple[Union[str, None], Union[str, None]]:
    doc = nlp(command)

    # Identify command type
    command_type = None
    for token in doc:
        if token.text.lower() in ["where", "how", "do", "what"]:
            if token.dep_ == "advmod" and token.head.text.lower() == "is":
                command_type = "location"
            elif token.text.lower() == "how" and token.head.text.lower() == "many":
                command_type = "quantity"
            elif token.text.lower() == "do" and token.head.text.lower() == "have":
                command_type = "existence"
            break

    # Extract target object
    target_object = None
    for chunk in doc.noun_chunks:
        if not target_object:
            target_object = chunk.text

    return command_type, target_object


def locate_items(nouns: str) -> QuerySet["Thing"]:
    names = reduce(operator.or_, (Q(name__icontains=word) for word in nouns.split()))
    decriptions = reduce(operator.or_, (Q(description__icontains=word) for word in nouns.split()))

    query = Thing.objects.filter(names | decriptions)
    print(query.sql)
    return query


def quantity_on_hand(command: str):
    pass


def check_existence(command: str):
    pass


def whats_in_here(command: str):
    pass


COMMAND_MAP = {"location": locate_items, "quantity": quantity_on_hand, "existence": check_existence}
