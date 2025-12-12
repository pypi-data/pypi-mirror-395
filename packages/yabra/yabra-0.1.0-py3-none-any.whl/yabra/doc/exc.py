from yabra.doc import types


class InvalidDocumentError(Exception):
    result: types.PerformValidationErrorResult

    def __init__(self, result: types.PerformValidationErrorResult) -> None:
        self.result = result
        super().__init__(result["message"])
