import pytest
from unittest.mock import patch


@pytest.fixture(scope="function")
def mock_crud():
    with patch.object.object('app.crud.create_post') as mock_create, \
            patch.object('app.crud.get_post_by_id') as mock_get_by_id, \
            patch.object('app.crud.get_posts_by_author_id') as mock_get_posts_by_author_id, \
            patch.object('app.crud.get_posts') as mock_get_posts, \
            patch.object('app.crud.update_post') as mock_update_post, \
            patch.object('app.crud.delete_post') as mock_delete_post, \
            patch.object('app.auth.get_post_author_or_admin') as mock_get_author_or_admin:
        # mock_get_by_id.return_value = {"id": "1", "title": "Test Post", "content": "This is a test."}
        yield {
            "create": mock_create,
            "get_by_id": mock_get_by_id,
            "get_by_author": mock_get_posts_by_author_id,
            "get_all": mock_get_posts,
            "update": mock_update_post,
            "delete": mock_delete_post,
            "get_author_or_admin": mock_get_author_or_admin,
        }
