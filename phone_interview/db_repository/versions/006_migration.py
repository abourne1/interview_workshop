from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
questions = Table('questions', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author', String(length=64)),
    Column('topic_id', Integer),
    Column('text', Text(length=2000)),
    Column('hint', Text(length=2000)),
    Column('timestamp', DateTime),
    Column('popularity', Integer),
    Column('answer', Text(length=2000)),
    Column('language', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].columns['language'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].columns['language'].drop()
