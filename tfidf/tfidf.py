import sys

import numpy as np
from gensim import corpora, matutils
from peewee import prefetch

from models import init_db, StemArticle, Article, Stem, StemTfidf, PEWEE_DB

if __name__ == '__main__':
    stem_type = sys.argv[1]
    init_db()

    articles = prefetch(Article.select(), StemArticle.select(), Stem.select())

    # for each article, for each porter stem, add it times its count to the array
    docs, ids = zip(*[([s for stem in article.stems for s in [stem.stem.term]*stem.count if stem.stem.type == stem_type], article.id)
                      for article in articles])

    dictionary = corpora.Dictionary(docs)
    corpus = [dictionary.doc2bow(doc) for doc in docs]

    matrix = matutils.corpus2dense(corpus, len(dictionary)).T

    # Divide each row by its sum of counts
    tf = matrix / np.sum(matrix, 1)[:, None]

    # How many documents each word is contained in
    df = np.sum(matrix > 0, 0)
    idf = np.log(len(docs) / df)

    # Multiply each row by idf vector, element-wise
    tfidf = tf * idf[None, :]

    print('Saving TFIDF to the database..')
    with PEWEE_DB.atomic():
        for i, article in enumerate(articles):
            for stem_article in article.stems:
                if stem_article.stem.type != stem_type:
                    continue
                value = tfidf[i, dictionary.token2id[stem_article.stem.term]]
                StemTfidf.create(article=article, stem=stem_article.stem, value=value)
    print('Finished')
