import pytest
import spacy


@pytest.fixture(scope="session")
def nlp_ja():
    return spacy.load("ja_ginza")
