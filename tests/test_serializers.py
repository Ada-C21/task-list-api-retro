from app.serializers.one_task import OneTask

def test_serialize_one_task(one_task):
    serializer = OneTask()
    result = serializer.serialize(one_task)
    assert result == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }

# Tests for other serializers would be similar to the one above
