# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from pathlib import Path
from traitlets import Unicode
from .stores import SQLiteYStore

class CustomSQLiteYStore(SQLiteYStore):
    db_dir = ".guides"

    db_path = Unicode(
        ".guides/.jupyter_ystore.db",
        config=True,
        help="""The path to the YStore database. Defaults to '.guides/.jupyter_ystore.db' in the current
        directory.""",
    )

    def __init__(self, **kwargs):
        Path(self.db_dir).mkdir(parents=True, exist_ok=True)
        super().__init__(**kwargs)
