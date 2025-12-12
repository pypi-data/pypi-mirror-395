"""
Milvus vector database utilities.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

from bizstats_vector_store.milvus.client import MilvusClient
from bizstats_vector_store.milvus.collections import CollectionManager

__all__ = ["MilvusClient", "CollectionManager"]
