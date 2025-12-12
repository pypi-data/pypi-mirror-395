# Copyright 2024 Sushanth (https://github.com/sushanthpy)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
ToonDB Python SDK

A Python client for ToonDB - the database optimized for LLM context retrieval.

Provides two modes of access:
- Embedded: Direct database access via FFI (single process)
- IPC: Client-server access via Unix sockets (multi-process)
"""

from .ipc_client import IpcClient
from .database import Database, Transaction
from .query import Query
from .errors import ToonDBError, ConnectionError, TransactionError, ProtocolError

__version__ = "0.1.0"
__all__ = [
    "Database",
    "Transaction", 
    "Query",
    "IpcClient",
    "ToonDBError",
    "ConnectionError",
    "TransactionError",
    "ProtocolError",
]
