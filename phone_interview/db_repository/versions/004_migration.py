from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
recordings = Table('recordings', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String(length=200)),
    Column('call_sid', String(length=300)),
    Column('recording_sid', String(length=300)),
    Column('sent', Boolean),
    Column('question_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['recordings'].columns['recording_sid'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['recordings'].columns['recording_sid'].drop()
