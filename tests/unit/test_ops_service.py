from core.msg.services import OperationsService, ops_service
from core.msg.models import Operation
from uuid import uuid4


def test_get_operation_valid() -> None:
    op_id = uuid4()
    op = Operation(op_id)
    test_table = {
        "input": {
            "op_id": op_id,
            "operations": {op_id: op},
        },
        "result": {"operation": op},
    }
    service = OperationsService()
    service.operations = test_table["input"]["operations"]
    assert (
        service.get_operation(test_table["input"]["op_id"])
        == test_table["result"]["operation"]
    )


def test_get_operation_empty() -> None:
    op_id = uuid4()
    test_table = {
        "input": {
            "op_id": op_id,
            "operations": {},
        },
        "result": {"operation": None},
    }
    service = OperationsService()
    service.operations = test_table["input"]["operations"]
    assert (
        service.get_operation(test_table["input"]["op_id"])
        == test_table["result"]["operation"]
    )


def test_finish_operation_valid() -> None:
    op_id = uuid4()
    test_table = {
        "input": {
            "op_id": op_id,
            "result": True,
            "operations": {
                op_id: Operation(op_id),
            },
        },
        "result": {
            "bool": True,
            "operations": {
                op_id: Operation(op_id, True, True),
            },
        },
    }
    service = OperationsService()
    service.operations = test_table["input"]["operations"]
    assert (
        service.finish_operation(
            test_table["input"]["op_id"],
            test_table["input"]["result"],
        )
        == test_table["result"]["bool"]
        and service.operations == test_table["result"]["operations"]
    )


def test_finish_operation_empty() -> None:
    op_id = uuid4()
    test_table = {
        "input": {
            "op_id": op_id,
            "result": True,
            "operations": {},
        },
        "result": {
            "bool": False,
            "operations": {},
        },
    }
    service = OperationsService()
    service.operations = test_table["input"]["operations"]
    assert (
        service.finish_operation(
            test_table["input"]["op_id"],
            test_table["input"]["result"],
        )
        == test_table["result"]["bool"]
        and service.operations == test_table["result"]["operations"]
    )


def test_execute_operation_valid() -> None:
    op_id = uuid4()
    test_table = {
        "input": {
            "op_id": op_id,
            "result": True,
        },
        "result": {
            "operations": {},
        },
    }
    service = OperationsService()
    op_id = service.execute_operation(lambda x: x+1)
    assert ()
