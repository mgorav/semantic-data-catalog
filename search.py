import os
from typing import List, Tuple, Dict, Union
import numpy as np
from gensim.models.word2vec import Word2Vec
import re

import gensim
import owlready2
from typing import List,Dict,Tuple
import numpy as np

import faiss
from faiss.swigfaiss import IndexFlatIP
from itertools import chain


def parse_camel_plus(string: str) -> List[str]:
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', string)
    words = [m.group(0) for m in matches]
    return [word.lower() for word in words]

def embed_text(sentence:Union[str,List[str]], model:Word2Vec) -> np.ndarray:
    # make sure sentence is a list of words
    if isinstance(sentence, str):
        sentence = sentence.split()

    emb_sum = np.zeros(model.vector_size, dtype=np.float32)
    known_words = 0

    for word in sentence:
        if word in model.wv.index_to_key:
            emb_sum += model.wv.get_vector(word)
            known_words += 1

    if known_words:
        return emb_sum / known_words
    else:
        raise ValueError("no words recognized in the given sentence")


model = gensim.models.Word2Vec.load('~/Documents/MyGithub/OWL2Vec-Star/semantic_search/output/multi_word2vec/output/ontology.embeddings')

ontologies:List[owlready2.Ontology] = [owlready2.get_ontology('./ontologies/'+onto_path).load() for onto_path in os.listdir('./ontologies')]

onto_iri2embeds:Dict[str,List[Tuple[str,np.ndarray]]] = dict()
for onto in ontologies:
    onto_iri2embeds[onto.base_iri] = list()
    for cls in onto.classes():
        onto_iri2embeds[onto.base_iri].append((cls.iri, model.wv.get_vector(cls.iri)))
        try:
            cls_name = ' '.join(parse_camel_plus(cls.name))
            onto_iri2embeds[onto.base_iri].append((cls.iri, embed_text(cls_name, model)))
        except ValueError:
            pass

print("Vector based indexing done.....")
def create_index(embeddings: List[Tuple[str,np.ndarray]], model: Word2Vec) -> IndexFlatIP:
    # make 2D array of all embeddings
    embeddings = [embedding[1] for embedding in embeddings]
    embeddings_2d = np.stack(embeddings, axis=0)
    search_index = faiss.IndexFlatIP(model.vector_size)
    search_index.add(embeddings_2d)
    return search_index

print("Creating vector based indexes....")
name2faiss_index:Dict[str, IndexFlatIP] = dict()
all_embeddings = list(chain.from_iterable(onto_iri2embeds.values()))
name2faiss_index['All'] = create_index(all_embeddings, model)
for ontology_iri in onto_iri2embeds:
    name2faiss_index[ontology_iri] = create_index(onto_iri2embeds[ontology_iri], model)

# search over entire catalog
query  = 'onion'
# query = 'spicy'

print("Querying ",query)
query_emb = embed_text(query, model).reshape(1,-1)
scores, indexes = name2faiss_index['All'].search(query_emb, 5)
results = [all_embeddings[ind][0] for ind in indexes[0]]
for result in results:
    print(result)