import requests


host = "http://127.0.0.1:8000"


def test_load_server():
    response = requests.get(f"{host}")
    assert response.ok, "сервер недоступен"


def test_order_add():
    method = "order/add"
    req = {"ордер": "OR12342134", "заказ": "NZKP124555"}
    res = {"ордер": "OR12342134", "заказ": "NZKP124555", "статус": "запланирован"}
    response = requests.post(f"{host}/{method}", json=req)
    assert response.ok, f"метод {method} недоступен"
    assert isinstance(response.json(), dict), "Не dict"
    assert response.json()["OR12342134"] == res, "не тот ответ"


def test_union_order_add():
    method = "order/add"
    orders = [
        {"ордер": "ордер1", "заказ": "заказ1"},
        {"ордер": "ордер2", "заказ": "заказ2"},
    ]
    orders_resp = {
        "ордер1": {"ордер": "ордер1", "заказ": "заказ1", "статус": "запланирован"},
        "ордер2": {"ордер": "ордер2", "заказ": "заказ2", "статус": "запланирован"},
    }
    [requests.post(f"{host}/{method}", json=order) for order in orders]

    req = {"ордер": "test_union_1", "ордера": ["ордер1", "ордер2"]}
    response = requests.post(f"{host}/{method}", json=req)
    assert response.ok, f"метод {method} недоступен"
    assert isinstance(response.json(), dict), "Не dict"
    print(response.json())
    assert response.json()["ордер1"] == orders_resp["ордер1"], "не тот ответ"
    assert response.json()["ордер2"] == orders_resp["ордер2"], "не тот ответ"


def test_union_order_add_bad():
    method = "order/add"
    orders = [
        {"ордер": "ордер3", "заказ": "заказ3"},
    ]
    orders_resp = {
        "ордер3": {"ордер": "ордер3", "заказ": "заказ3", "статус": "запланирован"},
    }
    [requests.post(f"{host}/{method}", json=order) for order in orders]

    req = {"ордер": "test_union_bad", "ордера": ["ордер3", "ордер4"]}
    response = requests.post(f"{host}/{method}", json=req)
    assert response.ok, f"метод {method} недоступен"
    assert isinstance(response.json(), dict), "Не dict"
    print(response.json())
    assert response.json()["ордер3"] == orders_resp["ордер3"], "не тот ответ"


def test_change_cancel_status():
    method = "order/cancel"
    id = "OR12342134"
    response = requests.get(f"{host}/{method}/{id}")
    assert response.ok, f"метод {method} недоступен"
    assert response.json()[id]["статус"] == "отменен"

def test_change_cancel_status_union():
    method = "order/cancel"
    id = "test_union_1"
    response = requests.get(f"{host}/{method}/{id}")
    assert response.ok, f"метод {method} недоступен"
    assert response.json()["ордер1"]["статус"] == "отменен"
    assert response.json()["ордер2"]["статус"] == "отменен"

def test_change_cancel_status_union_bad():
    method = "order/cancel"
    id = "test_union_bad"
    response = requests.get(f"{host}/{method}/{id}")
    assert response.ok, f"метод {method} недоступен"
    assert response.json()["ордер3"]["статус"] == "отменен"


def test_change_status():
    method = "order/status"
    id = "OR12342134"
    status = "отобран"
    response = requests.get(f"{host}/{method}/{id}?status={status}")
    assert response.ok, f"метод {method} недоступен"
    assert response.json()[id]["статус"] == status
