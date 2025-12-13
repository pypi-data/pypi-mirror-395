from __future__ import annotations

import logging
from contextlib import contextmanager, nullcontext

logger = logging.getLogger("xmas_app")


@contextmanager
def repo_uow(repo):
    """
    Unit-of-work for DBRepository.
    Uses repo.Session() + session.begin().
    Falls back to no-op if neither is available (not atomic).
    """

    if hasattr(repo, "Session"):
        logger.debug("repo_uow: using repo.Session() + session.begin()")
        Session = getattr(repo, "Session")
        with Session() as session:
            # SQLAlchemy transactional block
            with session.begin():
                yield
        return

    logger.warning("repo_uow: no transaction support; proceeding without atomicity")
    with nullcontext():
        yield
