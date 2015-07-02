from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
questions = Table('questions', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('author', VARCHAR(length=64)),
    Column('topic_id', INTEGER),
    Column('difficulty', INTEGER),
    Column('hint', TEXT(length=2000)),
    Column('next_question', INTEGER),
    Column('text', TEXT(length=2000)),
    Column('timestamp', DATETIME),
)

questions = Table('questions', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author', String(length=64)),
    Column('topic_id', Integer),
    Column('text', Text(length=2000)),
    Column('hint', Text(length=2000)),
    Column('timestamp', DateTime),
    Column('popularity', Integer),
    Column('answer', Text(length=2000)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['questions'].columns['difficulty'].drop()
    pre_meta.tables['questions'].columns['next_question'].drop()
    post_meta.tables['questions'].columns['answer'].create()
    post_meta.tables['questions'].columns['popularity'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['questions'].columns['difficulty'].create()
    pre_meta.tables['questions'].columns['next_question'].create()
    post_meta.tables['questions'].columns['answer'].drop()
    post_meta.tables['questions'].columns['popularity'].drop()
