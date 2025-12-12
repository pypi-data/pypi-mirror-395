from typing import Dict, Iterable

class SubjectsLabels:
    def __call__(self, ids: Iterable[str]) -> Dict[str, str]: ...
