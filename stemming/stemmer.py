import re
from collections import defaultdict

from nltk import SnowballStemmer
from pymystem3 import Mystem

from models import Article, init_db, StemArticle, Stem, PEWEE_DB


def tokenize(text: str):
    return re.split(r'[\s!@#$%^&*()/.,?><\\|;:\'\"\-]+', text)


snowball = SnowballStemmer('russian')
mystem = Mystem()


def stem_porter(token: str) -> str:
    return snowball.stem(token)


def stem_mystem(token: str) -> [str]:
    return mystem.lemmatize(token)[:-1]


if __name__ == '__main__':
    init_db()

    porter_articles = defaultdict(lambda: defaultdict(int))
    mystem_articles = defaultdict(lambda: defaultdict(int))

    print('Processing articles...')

    for article in Article.select():
        tokens = tokenize(article.text)
        for token in tokens:
            porter_articles[stem_porter(token)][article] += 1
            for lemma in stem_mystem(token):
                mystem_articles[lemma][article] += 1

    print('Saving stems...')
    with PEWEE_DB.atomic():
        for term, articles in porter_articles.items():
            stem = Stem(type='porter', term=term)
            stem.save()
            for article, count in articles.items():
                stem_article = StemArticle(article=article, stem=stem, count=count)
                stem_article.save(force_insert=True)

        for term, articles in mystem_articles.items():
            stem = Stem(type='pymystem', term=term)
            stem.save()
            for article, count in articles.items():
                stem_article = StemArticle(article=article, stem=stem, count=count)
                stem_article.save(force_insert=True)
