"""
End-to-end tests for folder nesting functionality.

These tests mirror the folder nesting tests in scripts/sanity_test.sh but use the SDK.
They require a running Morphik server on localhost:8000.

To run these tests:
    pytest morphik/tests/test_folder_nesting_e2e.py -v

To skip these tests (e.g., in CI without a server):
    SKIP_LIVE_TESTS=1 pytest morphik/tests/test_folder_nesting_e2e.py -v
"""

import os
import uuid

import pytest

from morphik.async_ import AsyncMorphik
from morphik.sync import Morphik

# Skip these tests if the SKIP_LIVE_TESTS environment variable is set
pytestmark = pytest.mark.skipif(
    os.environ.get("SKIP_LIVE_TESTS") == "1",
    reason="Skip tests that require a running Morphik server",
)


# =============================================================================
# Sync Client Tests
# =============================================================================


class TestFolderNestingSync:
    """
    E2E tests for folder nesting with the synchronous Morphik client.
    """

    @pytest.fixture
    def db(self):
        """Create a Morphik client for testing"""
        client = Morphik(timeout=120)
        yield client
        client.close()

    @pytest.fixture
    def test_id(self):
        """Generate a unique test ID for isolation"""
        return f"folder_e2e_{uuid.uuid4().hex[:8]}"

    @pytest.fixture
    def root_folder_path(self, test_id):
        """Generate a unique root folder path"""
        return f"/e2e_test_{test_id}"

    def test_create_nested_folder_with_auto_parents(self, db, root_folder_path):
        """Test creating a deeply nested folder auto-creates parent folders."""
        nested_path = f"{root_folder_path}/level1/level2/level3"

        try:
            # Create deeply nested folder
            folder = db.create_folder(name="level3", full_path=nested_path)

            # Verify the folder was created with correct properties
            assert folder.full_path == nested_path
            assert folder.depth == 4  # /root/level1/level2/level3 = 4 levels

            # Verify intermediate folders were auto-created
            level1 = db.get_folder(f"{root_folder_path}/level1")
            assert level1.full_path == f"{root_folder_path}/level1"
            assert level1.depth == 2

            level2 = db.get_folder(f"{root_folder_path}/level1/level2")
            assert level2.full_path == f"{root_folder_path}/level1/level2"
            assert level2.depth == 3

        finally:
            # Cleanup - delete recursively
            try:
                db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    def test_folder_full_path_property(self, db, root_folder_path):
        """Test that Folder.full_path returns the canonical path."""
        try:
            folder = db.create_folder(name="test_folder", full_path=root_folder_path)

            assert folder.full_path == root_folder_path
            assert folder.depth == 1
            assert folder.id is not None

        finally:
            try:
                db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    def test_folder_hierarchy_document_ingestion(self, db, root_folder_path, test_id):
        """Test ingesting documents into nested folders."""
        doc_ids = []

        try:
            # Create nested folder structure
            db.create_folder(name="level2", full_path=f"{root_folder_path}/level1/level2")
            db.create_folder(name="sibling", full_path=f"{root_folder_path}/sibling")

            # Ingest documents at different levels
            folders_content = [
                (root_folder_path, "Root level document content"),
                (f"{root_folder_path}/level1", "Level 1 document content"),
                (f"{root_folder_path}/level1/level2", "Level 2 document content"),
                (f"{root_folder_path}/sibling", "Sibling folder document content"),
            ]

            for folder_path, content in folders_content:
                folder = db.get_folder_by_name(folder_path)
                doc = folder.ingest_text(
                    content=content,
                    filename=f"test_{uuid.uuid4().hex[:8]}.txt",
                    metadata={"test_id": test_id, "folder": folder_path},
                )
                doc_ids.append(doc.external_id)

            # Wait for all documents to be processed
            for doc_id in doc_ids:
                db.wait_for_document_completion(doc_id, timeout_seconds=60)

            # Verify documents are in correct folders
            root_folder = db.get_folder_by_name(root_folder_path)
            root_docs = root_folder.list_documents(folder_depth=0).documents
            assert len(root_docs) == 1

        finally:
            # Cleanup
            for doc_id in doc_ids:
                try:
                    db.delete_document(doc_id)
                except Exception:
                    pass
            try:
                db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    def test_folder_depth_filtering(self, db, root_folder_path, test_id):
        """Test folder_depth parameter filters documents correctly."""
        doc_ids = []

        try:
            # Create hierarchy: root -> level1 -> level2 -> level3
            #                        -> sibling
            db.create_folder(name="level3", full_path=f"{root_folder_path}/level1/level2/level3")
            db.create_folder(name="sibling", full_path=f"{root_folder_path}/sibling")

            # Ingest one document at each level
            folder_paths = [
                root_folder_path,
                f"{root_folder_path}/level1",
                f"{root_folder_path}/level1/level2",
                f"{root_folder_path}/level1/level2/level3",
                f"{root_folder_path}/sibling",
            ]

            for folder_path in folder_paths:
                folder = db.get_folder_by_name(folder_path)
                doc = folder.ingest_text(
                    content=f"Document in {folder_path}",
                    filename=f"doc_{uuid.uuid4().hex[:8]}.txt",
                    metadata={"test_id": test_id},
                )
                doc_ids.append(doc.external_id)

            # Wait for processing
            for doc_id in doc_ids:
                db.wait_for_document_completion(doc_id, timeout_seconds=60)

            root_folder = db.get_folder_by_name(root_folder_path)

            # folder_depth=0: only exact folder match (1 doc)
            docs_exact = root_folder.list_documents(folder_depth=0).documents
            assert len(docs_exact) == 1, f"folder_depth=0 should return 1 doc, got {len(docs_exact)}"

            # folder_depth=1: root + direct children (root + level1 + sibling = 3 docs)
            docs_depth1 = root_folder.list_documents(folder_depth=1).documents
            assert len(docs_depth1) == 3, f"folder_depth=1 should return 3 docs, got {len(docs_depth1)}"

            # folder_depth=2: up to grandchildren (root + level1 + sibling + level2 = 4 docs)
            docs_depth2 = root_folder.list_documents(folder_depth=2).documents
            assert len(docs_depth2) == 4, f"folder_depth=2 should return 4 docs, got {len(docs_depth2)}"

            # folder_depth=-1: all descendants (all 5 docs)
            docs_all = root_folder.list_documents(folder_depth=-1).documents
            assert len(docs_all) == 5, f"folder_depth=-1 should return 5 docs, got {len(docs_all)}"

        finally:
            for doc_id in doc_ids:
                try:
                    db.delete_document(doc_id)
                except Exception:
                    pass
            try:
                db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    def test_retrieve_chunks_with_folder_depth(self, db, root_folder_path, test_id):
        """Test retrieve_chunks respects folder_depth parameter."""
        doc_ids = []

        try:
            # Create nested structure
            db.create_folder(name="child", full_path=f"{root_folder_path}/child")

            # Ingest documents
            root_folder = db.get_folder_by_name(root_folder_path)
            child_folder = db.get_folder_by_name(f"{root_folder_path}/child")

            doc1 = root_folder.ingest_text(
                content="Root folder document about machine learning and AI",
                filename=f"root_{uuid.uuid4().hex[:8]}.txt",
                metadata={"test_id": test_id},
            )
            doc_ids.append(doc1.external_id)

            doc2 = child_folder.ingest_text(
                content="Child folder document about machine learning and AI",
                filename=f"child_{uuid.uuid4().hex[:8]}.txt",
                metadata={"test_id": test_id},
            )
            doc_ids.append(doc2.external_id)

            # Wait for processing
            for doc_id in doc_ids:
                db.wait_for_document_completion(doc_id, timeout_seconds=60)

            # Retrieve with folder_depth=0 (exact folder only)
            chunks_exact = root_folder.retrieve_chunks(
                query="machine learning",
                k=10,
                folder_depth=0,
                filters={"test_id": test_id},
            )

            # All chunks should be from root folder only
            root_doc_chunks = [c for c in chunks_exact if c.document_id == doc1.external_id]
            child_doc_chunks = [c for c in chunks_exact if c.document_id == doc2.external_id]
            assert len(root_doc_chunks) >= 1, "Should have chunks from root folder"
            assert len(child_doc_chunks) == 0, "Should not have chunks from child folder with depth=0"

            # Retrieve with folder_depth=-1 (all descendants)
            chunks_all = root_folder.retrieve_chunks(
                query="machine learning",
                k=10,
                folder_depth=-1,
                filters={"test_id": test_id},
            )

            # Should have chunks from both folders
            all_doc_ids = {c.document_id for c in chunks_all}
            assert doc1.external_id in all_doc_ids, "Should have chunks from root folder"
            assert doc2.external_id in all_doc_ids, "Should have chunks from child folder with depth=-1"

        finally:
            for doc_id in doc_ids:
                try:
                    db.delete_document(doc_id)
                except Exception:
                    pass
            try:
                db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    def test_folder_path_normalization(self, db, test_id):
        """Test that folder paths are normalized correctly."""
        base_path = f"/normalize_test_{test_id}"

        try:
            # Test trailing slash normalization
            folder1 = db.create_folder(name="trailing", full_path=f"{base_path}/trailing/")
            assert folder1.full_path == f"{base_path}/trailing", "Trailing slash should be normalized"

            # Test double slash normalization
            folder2 = db.create_folder(name="double", full_path=f"{base_path}//double")
            assert folder2.full_path == f"{base_path}/double", "Double slashes should be normalized"

        finally:
            try:
                db.delete_folder(f"{base_path}?recursive=true")
            except Exception:
                pass

    def test_folder_lookup_by_path(self, db, root_folder_path):
        """Test looking up folders by their path."""
        try:
            # Create nested structure
            db.create_folder(name="level2", full_path=f"{root_folder_path}/level1/level2")

            # Lookup by path
            level1 = db.get_folder(f"{root_folder_path}/level1")
            assert level1.full_path == f"{root_folder_path}/level1"
            assert level1.depth == 2

            level2 = db.get_folder(f"{root_folder_path}/level1/level2")
            assert level2.full_path == f"{root_folder_path}/level1/level2"
            assert level2.depth == 3

        finally:
            try:
                db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass


# =============================================================================
# Async Client Tests
# =============================================================================


class TestFolderNestingAsync:
    """
    E2E tests for folder nesting with the asynchronous Morphik client.
    """

    @pytest.fixture
    async def db(self):
        """Create an AsyncMorphik client for testing"""
        client = AsyncMorphik(timeout=120)
        yield client
        await client.close()

    @pytest.fixture
    def test_id(self):
        """Generate a unique test ID for isolation"""
        return f"folder_async_e2e_{uuid.uuid4().hex[:8]}"

    @pytest.fixture
    def root_folder_path(self, test_id):
        """Generate a unique root folder path"""
        return f"/async_e2e_{test_id}"

    @pytest.mark.asyncio
    async def test_create_nested_folder_with_auto_parents(self, db, root_folder_path):
        """Test creating a deeply nested folder auto-creates parent folders (async)."""
        nested_path = f"{root_folder_path}/level1/level2/level3"

        try:
            # Create deeply nested folder
            folder = await db.create_folder(name="level3", full_path=nested_path)

            # Verify the folder was created with correct properties
            assert folder.full_path == nested_path
            assert folder.depth == 4

            # Verify intermediate folders were auto-created
            level1 = await db.get_folder(f"{root_folder_path}/level1")
            assert level1.full_path == f"{root_folder_path}/level1"
            assert level1.depth == 2

            level2 = await db.get_folder(f"{root_folder_path}/level1/level2")
            assert level2.full_path == f"{root_folder_path}/level1/level2"
            assert level2.depth == 3

        finally:
            try:
                await db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_folder_full_path_property(self, db, root_folder_path):
        """Test that AsyncFolder.full_path returns the canonical path (async)."""
        try:
            folder = await db.create_folder(name="test_folder", full_path=root_folder_path)

            assert folder.full_path == root_folder_path
            assert folder.depth == 1
            assert folder.id is not None

        finally:
            try:
                await db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_folder_hierarchy_document_ingestion(self, db, root_folder_path, test_id):
        """Test ingesting documents into nested folders (async)."""
        doc_ids = []

        try:
            # Create nested folder structure
            await db.create_folder(name="level2", full_path=f"{root_folder_path}/level1/level2")
            await db.create_folder(name="sibling", full_path=f"{root_folder_path}/sibling")

            # Ingest documents at different levels
            folders_content = [
                (root_folder_path, "Root level document content async"),
                (f"{root_folder_path}/level1", "Level 1 document content async"),
                (f"{root_folder_path}/level1/level2", "Level 2 document content async"),
                (f"{root_folder_path}/sibling", "Sibling folder document content async"),
            ]

            for folder_path, content in folders_content:
                folder = db.get_folder_by_name(folder_path)
                doc = await folder.ingest_text(
                    content=content,
                    filename=f"test_{uuid.uuid4().hex[:8]}.txt",
                    metadata={"test_id": test_id, "folder": folder_path},
                )
                doc_ids.append(doc.external_id)

            # Wait for all documents to be processed
            for doc_id in doc_ids:
                await db.wait_for_document_completion(doc_id, timeout_seconds=60)

            # Verify documents are in correct folders
            root_folder = db.get_folder_by_name(root_folder_path)
            root_docs = (await root_folder.list_documents(folder_depth=0)).documents
            assert len(root_docs) == 1

        finally:
            for doc_id in doc_ids:
                try:
                    await db.delete_document(doc_id)
                except Exception:
                    pass
            try:
                await db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_folder_depth_filtering(self, db, root_folder_path, test_id):
        """Test folder_depth parameter filters documents correctly (async)."""
        doc_ids = []

        try:
            # Create hierarchy
            await db.create_folder(name="level3", full_path=f"{root_folder_path}/level1/level2/level3")
            await db.create_folder(name="sibling", full_path=f"{root_folder_path}/sibling")

            # Ingest one document at each level
            folder_paths = [
                root_folder_path,
                f"{root_folder_path}/level1",
                f"{root_folder_path}/level1/level2",
                f"{root_folder_path}/level1/level2/level3",
                f"{root_folder_path}/sibling",
            ]

            for folder_path in folder_paths:
                folder = db.get_folder_by_name(folder_path)
                doc = await folder.ingest_text(
                    content=f"Document in {folder_path}",
                    filename=f"doc_{uuid.uuid4().hex[:8]}.txt",
                    metadata={"test_id": test_id},
                )
                doc_ids.append(doc.external_id)

            # Wait for processing
            for doc_id in doc_ids:
                await db.wait_for_document_completion(doc_id, timeout_seconds=60)

            root_folder = db.get_folder_by_name(root_folder_path)

            # folder_depth=0: only exact folder match (1 doc)
            docs_exact = (await root_folder.list_documents(folder_depth=0)).documents
            assert len(docs_exact) == 1, f"folder_depth=0 should return 1 doc, got {len(docs_exact)}"

            # folder_depth=1: root + direct children (3 docs)
            docs_depth1 = (await root_folder.list_documents(folder_depth=1)).documents
            assert len(docs_depth1) == 3, f"folder_depth=1 should return 3 docs, got {len(docs_depth1)}"

            # folder_depth=2: up to grandchildren (4 docs)
            docs_depth2 = (await root_folder.list_documents(folder_depth=2)).documents
            assert len(docs_depth2) == 4, f"folder_depth=2 should return 4 docs, got {len(docs_depth2)}"

            # folder_depth=-1: all descendants (5 docs)
            docs_all = (await root_folder.list_documents(folder_depth=-1)).documents
            assert len(docs_all) == 5, f"folder_depth=-1 should return 5 docs, got {len(docs_all)}"

        finally:
            for doc_id in doc_ids:
                try:
                    await db.delete_document(doc_id)
                except Exception:
                    pass
            try:
                await db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_retrieve_chunks_with_folder_depth(self, db, root_folder_path, test_id):
        """Test retrieve_chunks respects folder_depth parameter (async)."""
        doc_ids = []

        try:
            # Create nested structure
            await db.create_folder(name="child", full_path=f"{root_folder_path}/child")

            # Ingest documents
            root_folder = db.get_folder_by_name(root_folder_path)
            child_folder = db.get_folder_by_name(f"{root_folder_path}/child")

            doc1 = await root_folder.ingest_text(
                content="Root folder document about machine learning and AI async",
                filename=f"root_{uuid.uuid4().hex[:8]}.txt",
                metadata={"test_id": test_id},
            )
            doc_ids.append(doc1.external_id)

            doc2 = await child_folder.ingest_text(
                content="Child folder document about machine learning and AI async",
                filename=f"child_{uuid.uuid4().hex[:8]}.txt",
                metadata={"test_id": test_id},
            )
            doc_ids.append(doc2.external_id)

            # Wait for processing
            for doc_id in doc_ids:
                await db.wait_for_document_completion(doc_id, timeout_seconds=60)

            # Retrieve with folder_depth=0 (exact folder only)
            chunks_exact = await root_folder.retrieve_chunks(
                query="machine learning",
                k=10,
                folder_depth=0,
                filters={"test_id": test_id},
            )

            # All chunks should be from root folder only
            root_doc_chunks = [c for c in chunks_exact if c.document_id == doc1.external_id]
            child_doc_chunks = [c for c in chunks_exact if c.document_id == doc2.external_id]
            assert len(root_doc_chunks) >= 1, "Should have chunks from root folder"
            assert len(child_doc_chunks) == 0, "Should not have chunks from child folder with depth=0"

            # Retrieve with folder_depth=-1 (all descendants)
            chunks_all = await root_folder.retrieve_chunks(
                query="machine learning",
                k=10,
                folder_depth=-1,
                filters={"test_id": test_id},
            )

            # Should have chunks from both folders
            all_doc_ids = {c.document_id for c in chunks_all}
            assert doc1.external_id in all_doc_ids, "Should have chunks from root folder"
            assert doc2.external_id in all_doc_ids, "Should have chunks from child folder with depth=-1"

        finally:
            for doc_id in doc_ids:
                try:
                    await db.delete_document(doc_id)
                except Exception:
                    pass
            try:
                await db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_folder_path_normalization(self, db, test_id):
        """Test that folder paths are normalized correctly (async)."""
        base_path = f"/async_normalize_{test_id}"

        try:
            # Test trailing slash normalization
            folder1 = await db.create_folder(name="trailing", full_path=f"{base_path}/trailing/")
            assert folder1.full_path == f"{base_path}/trailing", "Trailing slash should be normalized"

            # Test double slash normalization
            folder2 = await db.create_folder(name="double", full_path=f"{base_path}//double")
            assert folder2.full_path == f"{base_path}/double", "Double slashes should be normalized"

        finally:
            try:
                await db.delete_folder(f"{base_path}?recursive=true")
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_folder_lookup_by_path(self, db, root_folder_path):
        """Test looking up folders by their path (async)."""
        try:
            # Create nested structure
            await db.create_folder(name="level2", full_path=f"{root_folder_path}/level1/level2")

            # Lookup by path
            level1 = await db.get_folder(f"{root_folder_path}/level1")
            assert level1.full_path == f"{root_folder_path}/level1"
            assert level1.depth == 2

            level2 = await db.get_folder(f"{root_folder_path}/level1/level2")
            assert level2.full_path == f"{root_folder_path}/level1/level2"
            assert level2.depth == 3

        finally:
            try:
                await db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass

    @pytest.mark.asyncio
    async def test_user_scope_with_folder_depth(self, db, root_folder_path, test_id):
        """Test UserScope operations with folder_depth (async)."""
        user_id = f"user_{uuid.uuid4().hex[:8]}"
        doc_ids = []

        try:
            # Create nested structure
            await db.create_folder(name="child", full_path=f"{root_folder_path}/child")

            # Create user scope on root folder
            root_folder = db.get_folder_by_name(root_folder_path)
            user_scope = root_folder.signin(user_id)

            # Ingest documents as user
            doc1 = await user_scope.ingest_text(
                content="Root document for user",
                filename=f"user_root_{uuid.uuid4().hex[:8]}.txt",
                metadata={"test_id": test_id},
            )
            doc_ids.append(doc1.external_id)

            # Ingest in child folder (via direct folder access)
            child_folder = db.get_folder_by_name(f"{root_folder_path}/child")
            child_user_scope = child_folder.signin(user_id)
            doc2 = await child_user_scope.ingest_text(
                content="Child document for user",
                filename=f"user_child_{uuid.uuid4().hex[:8]}.txt",
                metadata={"test_id": test_id},
            )
            doc_ids.append(doc2.external_id)

            # Wait for processing
            for doc_id in doc_ids:
                await db.wait_for_document_completion(doc_id, timeout_seconds=60)

            # List with folder_depth=0 should only show root folder docs
            docs_exact = (await user_scope.list_documents(folder_depth=0)).documents
            assert len(docs_exact) == 1, f"folder_depth=0 should return 1 doc, got {len(docs_exact)}"

            # List with folder_depth=-1 should show all descendant docs
            docs_all = (await user_scope.list_documents(folder_depth=-1)).documents
            assert len(docs_all) == 2, f"folder_depth=-1 should return 2 docs, got {len(docs_all)}"

        finally:
            for doc_id in doc_ids:
                try:
                    await db.delete_document(doc_id)
                except Exception:
                    pass
            try:
                await db.delete_folder(f"{root_folder_path}?recursive=true")
            except Exception:
                pass
