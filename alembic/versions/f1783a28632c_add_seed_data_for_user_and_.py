"""Add seed data for User and AttendanceRecord

Revision ID: f1783a28632c
Revises: b4cdd16dd084
Create Date: 2024-01-30 09:27:31.677536

"""
from typing import Sequence, Union
from datetime import datetime, timedelta

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f1783a28632c'
down_revision: Union[str, None] = 'b4cdd16dd084'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

users_table = sa.table('users',
    sa.column('id', sa.Integer),
    sa.column('name', sa.String),
    sa.column('account', sa.String),
    sa.column('password', sa.String),
    sa.column('email', sa.String),
    sa.column('role', sa.String),
    sa.column('phone', sa.String),
    sa.column('error_times', sa.Integer),
)

attendance_records_table = sa.table('attendance_records',
    sa.column('user_id', sa.Integer),
    sa.column('attendance_date', sa.DateTime),
    sa.column('time_in', sa.DateTime),
    sa.column('time_out', sa.DateTime),
    sa.column('attendance_type', sa.String),
)

def upgrade() -> None:
    user_data = [
        {'name': 'John Doe', 'account': 'john.doe', 'password': 'password123', 'email': 'john@example.com', 'role': 'Employee', 'phone': '1234567890', 'error_times': 0},
        {'name': 'Jane Smith', 'account': 'jane.smith', 'password': 'password123', 'email': 'jane@example.com', 'role': 'Manager', 'phone': '0987654321', 'error_times': 0},
    ]
    
    op.bulk_insert(users_table, user_data)

    attendance_data = [
        {'user_id': 1, 'attendance_date': datetime.now(), 'time_in': datetime.now() - timedelta(hours=8), 'time_out': datetime.now(), 'attendance_type': 'On Time'},
        {'user_id': 2, 'attendance_date': datetime.now() - timedelta(days=1), 'time_in': datetime.now() - timedelta(days=1, hours=9), 'time_out': datetime.now() - timedelta(days=1), 'attendance_type': 'Late'},
    ]
    op.bulk_insert(attendance_records_table, attendance_data)


def downgrade() -> None:
    pass
