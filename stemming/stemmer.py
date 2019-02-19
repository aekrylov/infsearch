import re
from collections import defaultdict

from nltk import SnowballStemmer
from pymystem3 import Mystem

from models import Article, init_db, StemArticle, Stem, PEWEE_DB


def tokenize(text: str):
    return re.split(r'[\s!@#$%^&*()/.,?><\\|;:\'\"\-]+', text)


snowball = SnowballStemmer('russian')
mystem = Mystem()


if __name__ == '__main__':
    init_db()

    porter_articles = defaultdict(set)
    mystem_articles = defaultdict(set)

    print('Processing articles...')

    for article in Article.select():
        tokens = tokenize(article.text)
        for token in tokens:
            porter_articles[snowball.stem(token)].add(article)
            for lemma in mystem.lemmatize(token)[:-1]:
                mystem_articles[lemma].add(article)

    print('Saving stems...')
    with PEWEE_DB.atomic():
        for term, articles in porter_articles.items():
            stem = Stem(type='porter', term=term)
            stem.save()
            for article in articles:
                stem_article = StemArticle(article=article, stem=stem)
                stem_article.save(force_insert=True)

        for term, articles in mystem_articles.items():
            stem = Stem(type='pymystem', term=term)
            stem.save()
            for article in articles:
                stem_article = StemArticle(article=article, stem=stem)
                stem_article.save(force_insert=True)
