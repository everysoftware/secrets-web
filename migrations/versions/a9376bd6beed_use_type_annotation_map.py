"""use type_annotation_map

Revision ID: a9376bd6beed
Revises: f4b3abdd6ac3
Create Date: 2023-10-23 23:35:17.281275

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a9376bd6beed'
down_revision: Union[str, None] = 'f4b3abdd6ac3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('comments', 'record_id',
    #                 existing_type=sa.BIGINT(),
    #                 type_=sa.String(),
    #                 existing_nullable=False)
    # op.alter_column('records', 'id',
    #                 existing_type=sa.BIGINT(),
    #                 type_=sa.String(),
    #                 existing_nullable=False,
    #                 existing_server_default=sa.Identity(always=False, start=1, increment=1, minvalue=1,
    #                                                     maxvalue=9223372036854775807, cycle=False, cache=1))
    # # ### end Alembic commands ###


def downgrade() -> None:
    pass
    # ### commands auto generated by Alembic - please adjust! ###
    # op.alter_column('records', 'id',
    #                 existing_type=sa.String(),
    #                 type_=sa.BIGINT(),
    #                 existing_nullable=False,
    #                 existing_server_default=sa.Identity(always=False, start=1, increment=1, minvalue=1,
    #                                                     maxvalue=9223372036854775807, cycle=False, cache=1))
    # op.alter_column('comments', 'record_id',
    #                 existing_type=sa.String(),
    #                 type_=sa.BIGINT(),
    #                 existing_nullable=False)
    # # ### end Alembic commands ###