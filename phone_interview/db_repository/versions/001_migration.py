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
    Column('difficulty', Integer),
    Column('timestamp', DateTime),
    Column('next_question', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].columns['difficulty'].create()
    post_meta.tables['questions'].columns['hint'].create()
    post_meta.tables['questions'].columns['next_question'].create()
    post_meta.tables['questions'].columns['text'].create()
    post_meta.tables['questions'].columns['timestamp'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['questions'].columns['difficulty'].drop()
    post_meta.tables['questions'].columns['hint'].drop()
    post_meta.tables['questions'].columns['next_question'].drop()
    post_meta.tables['questions'].columns['text'].drop()
    post_meta.tables['questions'].columns['timestamp'].drop()
