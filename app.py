from fastapi import FastAPI, Body, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.models import Selections, Selection, Union_selection, Union_selections



templates = Jinja2Templates(directory="templates")

selections = Selections()
selections.load()
union_selections = Union_selections()
union_selections.load() 

print(selections, union_selections)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    delete_status = {"отменен", "отгружен"}
    usk = list(union_selections.api().keys())
    for number in usk:
        if union_selections.union_selection(number).status() in delete_status:
            union_selections.remove(number)

    sk = list(selections.api().keys())
    for number in sk:
        if selections.selection(number).status() in delete_status:
            selections.remove(number)
    selections.save()
    union_selections.save()
    return templates.TemplateResponse(
        request=request, name="orders.html", context={"orders": selections.view()}
    )


@app.post("/order/add")
def order_add(data=Body()):
    keys = data.keys()
    if "заказ" in keys:
        selection = Selection(number=data["ордер"], order=data["заказ"])
        selections.add(selection)
    elif "ордера" in keys:
        union_selection = Union_selection(
            number=data["ордер"], numbers_selection=tuple(data["ордера"])
        )
        union_selection.change_status(selections, union_selection.status())
        union_selections.add(union_selection)
    return selections.view()


@app.get("/order/cancel/{id}")
def order_cancel(id: str):
    status = "отменен"
    if selections.selection(id):
        selections.selection(id).change_status(status)
    elif union_selections.union_selection(id):
        union_selections.union_selection(id).change_status(selections, status)
    return selections.view()


@app.get("/order/status/{id}")
def order_status(id: str, status: str):
    if selections.selection(id):
        selections.selection(id).change_status(status)
    elif union_selections.union_selection(id):
        union_selections.union_selection(id).change_status(status)
    return selections.view()


@app.get("/orders")
def orders_list():
    return selections.view()


@app.get("/union_orders")
def union_selections_list():
    return union_selections.view()

