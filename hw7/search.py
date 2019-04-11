import sys

import numpy as np
from gensim import corpora, models, matutils
from peewee import prefetch

from models import init_db, Article, StemArticle, Stem
from stemming import stem_porter

STEM_TYPE = 'porter'
init_db()

articles = prefetch(Article.select(), StemArticle.select(), Stem.select())

# for each article, for each porter stem, add it times its count to the array
docs, ids = zip(*[([s for stem in article.stems for s in [stem.stem.term]*stem.count if stem.stem.type == STEM_TYPE], article.id)
                  for article in articles])

dictionary = corpora.Dictionary(docs)
corpus = [dictionary.doc2bow(doc) for doc in docs]
tfidf_model = models.TfidfModel(corpus, smartirs='ntc')
idf_model = models.TfidfModel(corpus, smartirs='btc')  # TF is binary


def project(doc):
    return np.matmul(doc[None, :], v.T[:, :5])


def project_corpus(corpus):
    return np.matmul(corpus, v.T[:, :5])


def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def search_docs(query: str):
    bow = dictionary.doc2bow([stem_porter(w) for w in query.split(' ')])
    query_idf = matutils.sparse2full(idf_model[bow], len(dictionary))
    query_lsi = project(query_idf)

    similarities = [(articles[i], cosine_sim(query_lsi, doc)) for i, doc in enumerate(corpus_lsi)]
    return [
        (article.url, value, article)
        for article, value in sorted(similarities, key=lambda x: x[1], reverse=True)[:10]
        if value > 0
    ]


if __name__ == '__main__':
    corpus_tfidf = matutils.corpus2dense(tfidf_model[corpus], len(dictionary)).T

    u, s, v = np.linalg.svd(corpus_tfidf)
    corpus_lsi = project_corpus(corpus_tfidf)

    for url, value, article in search_docs(sys.argv[1]):
        print('%.4f\t%s\t%s' % (value, url, article.title))
