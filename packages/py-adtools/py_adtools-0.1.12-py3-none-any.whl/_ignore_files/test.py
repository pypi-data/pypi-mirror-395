import concurrent
from typing import Dict, Any, Callable, List

from adtools.evaluator import PyEvaluatorForBigReturnedObjectV2


class MyEvaluator(PyEvaluatorForBigReturnedObjectV2):
    def __init__(self):
        super().__init__(debug_mode=True)

    def evaluate_program(
            self,
            program_str: str,
            callable_functions_dict: Dict[str, Callable] | None,
            callable_functions_list: List[Callable] | None,
            callable_classes_dict: Dict[str, Callable] | None,
            callable_classes_list: List[Callable] | None,
            **kwargs
    ) -> Any:
        while True:
            pass
        import torch
        return torch.randn(100, 4096, 4096)



if __name__ == '__main__':
    eval = MyEvaluator()
    res = eval.secure_evaluate('',timeout_seconds=20)
    print(res.shape)
