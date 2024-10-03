from fastapi.testclient import TestClient
from main import app  # Adjust according to your app's entry point

client = TestClient(app)


def test_create_new_post(mock_crud):
    # Set up the mock return value for creating a post
    mock_crud["create"].return_value = "1"  # Mock post ID return value

    response = client.post("/posts/", json={"title": "Test Post", "content": "This is a test."})

    assert response.status_code == 200
    assert response.json() == {"post_id": "1"}


def test_get_single_post(mock_crud):
    # Mock return value for getting a single post
    mock_crud["get_by_id"].return_value = {"id": "1", "title": "Test Post", "content": "This is a test."}

    response = client.get("/posts/1")

    assert response.status_code == 200
    assert response.json() == {"id": "1", "title": "Test Post", "content": "This is a test."}


def test_get_posts_by_author(mock_crud):
    # Mock return value for getting posts by author
    mock_crud["get_by_author"].return_value = [{"id": "1", "title": "Author Post", "content": "Author content."}]

    response = client.get("/posts/author/test_author_id")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Author Post"


def test_get_all_posts(mock_crud):
    # Mock return value for getting all posts
    mock_crud["get_all"].return_value = [{"id": "1", "title": "Post 1"}, {"id": "2", "title": "Post 2"}]

    response = client.get("/posts/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_existing_post(mock_crud):
    # Mock return value for updating a post
    mock_crud["update"].return_value = 1  # 1 post updated

    response = client.put("/posts/1", json={"title": "Updated Title", "content": "Updated content."})

    assert response.status_code == 200
    assert response.json() == {"msg": "Post updated"}


def test_delete_existing_post(mock_crud):
    # Mock return value for deleting a post
    mock_crud["delete"].return_value = 1  # 1 post deleted

    response = client.delete("/posts/1")

    assert response.status_code == 200
    assert response.json() == {"msg": "Post deleted successfully"}


def test_get_posts_by_date_range(mock_crud):
    # Mock return value for getting posts by date range
    mock_crud["get_all"].return_value = [
        {"id": "1", "title": "Date Filtered Post", "content": "This is a date filtered test."}]

    response = client.get("/posts/date/?start_date=2024-10-01&end_date=2024-10-02")

    assert response.status_code == 200
    assert len(response.json()) == 1
