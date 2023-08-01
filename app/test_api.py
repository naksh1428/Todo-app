from fastapi.testclient import TestClient
from main import app
import random
import json

client = TestClient(app)

names = ('John', 'Andy', 'Joe', 'Tiger', 'Marty', 'Nick')
task_type = ("Development", "Testing", "Deployment")
task_status = ("To-Do", "In-Progress", "Cancelled", "Completed")
task_names = ("Refinement task", "New Feature developement", "KT task", "Technical Documentation")


def data_generate():

    params = {"task_name": f"{random.choice(task_names)}",
              "task_type": f"{random.choice(task_type)}",
              "task_status": f"{random.choice(task_status)}",
              "assignee": f"{random.choice(names)}",
              "comments": f"Created by Pytest",
              }
    return params


def test_root():
    response = client.get("/api/healthchecker")
    assert response.status_code == 200
    assert response.json() == {"API": "To do management is LIVE.. "}


def test_task_list():
    response = client.get("api/all-todo")
    assert response.status_code == 200


def test_create_task():
    params = data_generate()
    response = client.post("/api/create-todo", params=params)
    assert response.status_code == 201
    assert response.json().get("task_name") == params["task_name"]
    assert response.json().get("task_type") == params["task_type"]
    assert response.json().get("task_status") == params["task_status"]
    assert response.json().get("assignee") == params["assignee"]
    assert response.json().get("comments") == params["comments"]


def test_delete_task():
    params = data_generate()
    response = client.post("/api/create-todo", params=params)
    assert response.status_code == 201
    task_id = response.json().get("id")
    response = client.delete("/api/delete-todo", params={"task_id": task_id})
    assert response.status_code == 200
    assert response.json() == {"Message": f"ID: {task_id}, Record Deleted successfully"}


def test_get_task():
    task_status = ("To-Do", "In-Progress", "Cancelled", "Completed")
    for item in task_status:
        response = client.get("/api/get-todo-list", params={"task_status": item})
        assert response.status_code == 200


def test_get_deleted_task_list():
    response = client.get("/api/deleted-do-list")
    assert response.status_code == 200


# def test_update_task():
#     params = data_generate()
#     print("###########")
#     print(params)
#     response = client.post("/api/create-todo", params=params)
#     assert response.status_code == 201
#     print(response.json())
#     task_id = response.json().get("id")
#     updated_params = {
#         "id": task_id,
#         "task_name": f"Testing",
#         "task_type": f"{random.choice(task_type)}",
#         "assignee": f"{random.choice(names)}",
#         "task_status": f"{random.choice(task_status)}",
#         "comments": f"Updated Task comment in testing"
#     }
#     print(updated_params)
#     updated_task = client.patch("/api/update-task", json=json.dumps(updated_params))
#     assert updated_task.status_code == 200
#     assert updated_task.json().get("id") == updated_params["id"]