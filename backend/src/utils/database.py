"""Database utility functions for managing User entities."""

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


async def get_user_by_username(db: AsyncSession, username: str) -> User:
    """Retrieve a user from the database by their username.

    Args:
        db (AsyncSession): The active SQLAlchemy asynchronous session.
        username (str): The username to search for.

    Returns:
        User | None: The User object if found, otherwise None.
    """
    user = await db.execute(select(User).where(User.username == username))
    return user.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password_hash: str) -> User:
    """Create a new user in the database.

    Uses PostgreSQL's `INSERT ... ON CONFLICT DO NOTHING` to avoid inserting
    a duplicate user with the same username. If the user already exists,
    no new record is created and None is returned.

    Args:
        db (AsyncSession): The active SQLAlchemy asynchronous session.
        username (str): The username for the new user.
        password_hash (str): The hashed password for the new user.

    Returns:
        User | None: The newly created User object if successful,
        otherwise None (e.g., if the username already exists).
    """
    stmt = (
        insert(User)
        .values(username=username, password=password_hash)
        .on_conflict_do_nothing(index_elements=[User.username])
        .returning(User)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()
