from peewee import fn

from models import Article, Stem, StemArticle, init_db
from stemming import tokenize, stem_porter


def find(query):
    tokens = [stem_porter(token) for token in tokenize(query)]

    count = fn.SUM(StemArticle.count).alias('rank')
    count_distinct = fn.COUNT(StemArticle.stem.distinct())

    articles = (Article.select(Article, count, count_distinct)
                .join(StemArticle)
                .join(Stem)
                .where(Stem.term.in_(tokens) & (Stem.type == 'porter'))
                .group_by(Article.id)
                .having(count_distinct == len(tokens))
                .order_by(count.desc())
                )

    return articles


if __name__ == '__main__':
    init_db()
    query = input('Enter search query: ').strip()
    for article in find(query):
        print('%3d; %s' % (article.rank, article.title))