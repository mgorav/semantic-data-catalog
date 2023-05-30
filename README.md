

## Overview
Data is a fuel on which an organization depends on its operations/running, in other words, data is foundational to organisational operations. Data catalog are central to managing and utilizing data
assets. Data catalog provides an ability to search "for data", based on - name of the data assets,
its metadata plus related business terms. Hence, data catalog plays a critical role in "data discovery". However, most 
of the data catalog rely on "string matching" (using framework like Lucene or Elastic search). These type of search,
lacks in understanding meaning and relationships of _concepts_ in the catalogs. This leads to, missing
useful search hits on the data assets in data catalog. With the rise of _"Data Mesh"_, which proposes, data products (as _composition of data assets_) are organized in _"domains"_. 
This further adds to the search challenge in a data catalog.

_NOTE:_
The ontology can be see as 5-typle where its components are:
- **C**oncepts,
- **R**elationships,
- **F**unctions,
- **I**ndividuals or Instances and
- **A**xioms

**_Ontology_** = <C,R,F,I,A>
where:
- Concepts (classes): are the main formalied elements of the domain. Since the logic, the concepts can be described using specific properties which must be statisfied by them
- Relationships: are links between the concepts for representing the ontology structure (taxonomix or not traxonomic)
- Functions: are elements with the purpose of calculating infomration from the other elements
- Instances (objects): are the representation about the main objects within domain according to ontology structure
- Axions: are the restricitons, rules, logic correspondces definitions which must be accomplished in the relationship between the ontology elements. The axioms can be seen as
  smalest unit of knowledge within an ontology

So,how can we address this? Let's throw, the latest buzzwords - ChatGPT, LLM etc - potentially they can and will.

_However_ - I do believe, Data Catalog should be **_"Semantic Data Catalog"_**. In this blog, let's explore - **_"Semantic Data Catalog"_**.

## Semantic Data Catalog

A semantic data catalog is an intelligent catalog/inventory of data assets that automatizes sharing common meanings of data across data silos and provides a means to define 
hierarchies and relationships featuring semantic reasoning. It serves as a queryable, AI-enabled knowledge encyclopedia of the organization.

A semantic search engine is based on _**semantic context**_ of _search queries_ and context is more desirable, to understand 
the meaning/knowledge. Semantic _search engines also uses the relationships between entities for returning search results_. This type
of search is based on **_"Knowledge Graph"_**. The Knowledge Graph is a semantic database in which information is 
structured in such a way that knowledge is created from the information. Here, entities (nodes) are related to each other 
via edges, provided with attributes and other information and placed in semantic context or ontologies.Entities are the 
central organizational element in semantic databases, such as in Google’s Knowledge Graph.In addition to the relationships 
between the entities, Google uses data mining to collect attributes and other information about the entities and 
organizes them around the entities, as shown below:

![google knowledge graph](google_knowledge_graph.png)

_**How can we apply semantic search conctext to data catalog to provide semnatic search based on the contextual knowledge of the data.**_

The _**Semantic Data Catalog**_ solves the challenges of non contextual searches, **_by leveraging, the power of
ontologies, ontology embeddings and vector search to improve data discovery and management_**. As explained,  _**a Data Catalog is a
social graph**_; hence plain search dos not help, knowledge graph driven based on ontology addresses this challenge.
![Data catalog as social network](data_catalog_social_network.png)

**_The Semantic Data Catalog_** brings, following benefits: .
1. **Increase search accuracy and relevance**
    Build ontology based knowledge graph of data concepts, which helps in understanding the meanings of _data concepts_ and the _relationships_ 
    between them, a semantic data catalog provides  _accurate and relevant search results._ This can be measured using: _**Recall ,Precision**_
       ![recall & precession](recall_precession.png)
        

2. **Smarter data governance**
    With the power of ontology driven knowledge graph in one hand, clear understanding of the meanings of data asset graph as well as
    relationship of data concepts on the other hand, **_a semantic data catalog provides an organization a tool to better manage and utilize
    their data._**
3. **Increased efficiency and productivity**
   Semantic data catalog makes **_"search for data"_** easier, there by providing contextual knowledge driven **_"search in data"_** (lakehouse). This not only
   increase productivity, as well as, efficiency

 NOTE: excessive metadata can have negative affect on search, as articulated by [Zipf Law](https://en.wikipedia.org/wiki/Zipf%27s_law)

## Semantic Data Catalog Architecture
1. **Step 1** The starting point is the **_ontology catalog_**, which stores ontology of each of the data assets.
2. **Step 2** Train an ontology embedding model on the catalog to generate numerical vectors, or embeddings, that 
              capture the knowledge/meanings and relationships of concept
3. **Step 3** Load embedding into a vector search engine, which allows users to search for data assets within the
              data catalog using textual queries.
4. **Step 4** A provided query, the model is used to embed query and use vector search engine to fetch the most
              relevant concepts
![architecture](architecture.png)

## Sample Ontology Graph
   For this blog, I will be using pizza owl (ontology) from [Protege Stanford](https://protege.stanford.edu/ontologies/pizza/pizza.owl)

![Pizza](pizza_ontology.png)

## Search 
In this blog, I will be using [Facebooks similarity based search package](https://faiss.ai). After the embedding have been
created, these embedding need to be loaded into vector search engine. It's worth noting that, full blown vector database like [Pinecode](https://www.pinecone.io)
or [Weaviate](https://weaviate.io), etc can also be used for searching.

### Vector Database
Allow you to store a representation of any object as **_a vector (text, images, audio, video, etc_**. That is, it _stores data as high-dimensional vectors,
which are mathematical representations of features or attributes._. **_A vector is, essentially, just a list of numbers._** The amount of numbers, referred
to as dimensions, directly correlates to how much data a vector can represent. In our case the vectors we are interested in storing is a representation 
of the contextual meaning behind each and every word in the ontology (data concepts which exists in a Data Catalog).  Each vector has a certain number of dimensions, which can range from tens to 
thousands, depending on the complexity and granularity of the data. _The vectors are usually generated by applying some kind of transformation or
embedding function to the raw data. The embedding function can be based on various methods, such as machine learning models, word embeddings,
feature extraction algorithms._
**_The main advantage of a vector database is that it allows for fast and accurate similarity search and retrieval of data based on their vector 
distance or similarity. This means that instead of using traditional methods of querying databases based on exact matches or predefined criteria,
you can use a vector database to find the most similar or relevant data based on their semantic or contextual meaning._**

To perform similarity search and retrieval in a vector database, you need to use a **_query vector_** that represents your desired information or criteria.
The query vector can be either derived from the same type of data as the stored vectors. Then, you need to use a similarity measure that calculates
how close or distant two vectors are in the vector space. The similarity measure can be based on various metrics, such as cosine similarity, euclidean 
distance, hamming distance, jaccard index.

The result of the similarity search and retrieval is usually a ranked list of vectors that have the highest similarity scores with the query vector.
You can then access the corresponding raw data associated with each vector from the original source or index.

In 2023, there is a rising number of “vector databases” which are specifically built to store and search vector embeddings - some of the more popular ones include:
- Weaviate
- Milvus
- Qdrant
- Vespa
- Pinecon

### Embedding
An embedding is a relatively low-dimensional space into which you can translate high-dimensional vectors. Embeddings make it easier to do machine learning on large 
inputs like sparse vectors representing words. Ideally, an embedding captures some of the semantics of the input by placing semantically similar inputs close together
in the embedding space. An embedding can be learned and reused across models.
Embeddings can assist us in learning the semantic meaning of a word by studying what other words it often appears next to. 
Then we can produce a list of embeddings, which can be treated as a task-specific dictionary

### What exactly are vector embeddings?

Vectors are numeric representations of data that capture certain features of the data. For example, in the case of text data, “dog” and “puppy" 
Vectors are numeric representations of data that capture certain features of the data. For example, in the case of text data, “dog” and “puppy” have 
similar meaning, even though the words “dog” and “puppy” are very different if compared letter by letter. For semantic search to work effectively, representations 
of “dog” and “puppy” must sufficiently capture their semantic similarity. This is where vector representations are used, and why their derivation is so important.

```
dog = [1.6, -0.3, 7.2, 19.6, 3.1, ..., 20.6]
puppy = [1.5, -0.4, 7.2, 19.5, 3.2, ..., 20.8]
```
These vectors are genearated by machine learning model. 

### What is vector search?

Vector databases index data, unlike other databases, based on data vectors (or vector embeddings). Vector embeddings capture the meaning and context of data, usually predicted by Machine Learning models.

At the time of entry/import (or any significant changes to data objects), for every new/updated data object, vector databases use Machine Learning models to predict and calculate vector embeddings, which 
then are stored together with the object.


In practice, vectors are arrays of real numbers, of a fixed length (typically from hundreds to thousands of elements), generated by machine learning models. The process of generating a vector for a data object is
called vectorization. Vector DB generates vector embeddings using modules (OpenAI, Cohere, Google PaLM etc.), and conveniently stores both objects and vectors in the same database. For example, 
vectorizing the two words above might result in:” have similar meaning, even though the words “cat” and “kitty” are very different if compared letter by letter. For semantic search to work effectively, 
representations of “cat” and “kitty” must sufficiently capture their semantic similarity. This is where vector representations are used, and why their derivation is so important.

In practice, vectors are arrays of real numbers, of a fixed length (typically from hundreds to thousands of elements), generated by machine learning models. The process of generating a vector 
for a data object is called vectorization. Weaviate generates vector embeddings using modules (OpenAI, Cohere, Google PaLM etc.), and conveniently stores both objects and vectors in the same database. 
For example, vectorizing the two words above might result in:

```
Every data object in a dataset gets a vector
```

In a nutshell, vector embeddings are an array of numbers, which can be used as coordinates in a high-dimensional space. Although it is hard to imagine coordinates in more than 3-dimensional
space (x, y, z), we can still use the vectors to compute the distance between vectors, which can be used to indicate similarity between objects. 

There are many different distance metrics, like cosine similarity and Euclidean distance (L2 distance).

In a similar fashion, whenever we run a query (like: "What is the tallest building in Berlin?"), a vector database can also convert it to a "query" vector. The task of a vector database is to 
identify and retrieve a list of vectors that are closest to the given vector of your query, using a distance metric and a search algorithm.

Following are some of examples for search algorithims:
- k-nearest neighbors (kNN)
- Approximate nearest neighbors (ANN)
    - Examples of ANN methods are:

        - trees – e.g. ANNOY
        - proximity graphs
        - clustering - e.g. FAISS,
        - hashing - e.g. LSH,
        - vector compression - e.g. PQ or SCANN.


#### Vector Database Summary

- Vector databases use Machine Learning models to calculate and attach Vector embeddings to all data objects
- Vector embeddings capture the meaning and context of data
- Vector databases offer super fast queries thanks to ANN algorithms
- ANN algorithms trade a small amount of accuracy for huge gains in performance


## Model & Embedding
In this blog, I will be using [OWL2Vec2 - embedding of OWL ontology](https://arxiv.org/abs/2009.14654). There is refernce 
implementaiton from Oxford university, which takes a catalog of ontologies and build a model that embed ontologies.

**NOTE**
1. The embedding produced is affected by the language model and ontology configurations (so it's recommended to expriment
    with embeddings)
2. Accuracy testing is not coverned. It's recommended to use - [MRR](https://en.wikipedia.org/wiki/Mean_reciprocal_rank),
   [Hit Rate](https://en.wikipedia.org/wiki/Hit_rate) (recall & precession)

## OUTPUT
The example provided following search examples as a demonstration:
NOTE: There is no limitation, please enter the query of your choice

```
query  = 'margherita and onion'
# query  = 'margherita'
# query  = 'mozzarella'
query  = 'onion'
# query = 'spicy'
# query  = 'onion'
# query  = 'spicy'
```
Below is the output:
![output](output.png)

## Summary
Semantic Data Catalog is the future and provide powerful capabilities to simplify data governance challleges of 
discoverability and increase efficiencies. Howeer, it is worth articulating challenges which need to be considered before 
taking it to production:
1. The outcome is dependent on the training of ontology model as well as maintaining its accuracy
2. The continuous evaluation of effectiveness of the embeddings and also updating the search indexes (vectors), as 
   the catalog is evolving

   




