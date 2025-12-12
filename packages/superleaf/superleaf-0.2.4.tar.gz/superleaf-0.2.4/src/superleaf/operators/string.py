from dataclasses import asdict, dataclass
from typing import Callable, Iterable, Optional

from rapidfuzz import fuzz, utils

from superleaf.operators.base import bool_operator, BooleanOperator, operator, Operator


def str_op(method: str, *args, **kwargs) -> Operator:
    return operator(lambda s: getattr(s, method)(*args, **kwargs))


def str_bool_op(method: str, *args, **kwargs) -> BooleanOperator:
    return bool_operator(lambda s: getattr(s, method)(*args, **kwargs))


@dataclass
class FuzzyMatchResult:
    string: str
    target: str
    score: float
    string_raw: str | None = None
    target_raw: str | None = None

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(f'{k}={v!r}' for k, v in asdict(self).items() if v is not None)})"


@dataclass
class FuzzyMatchResults:
    results: list[FuzzyMatchResult]

    def best_match(self) -> FuzzyMatchResult | None:
        return max(self.results, key=lambda r: r.score)


class FuzzyMatcher(Operator):
    def __init__(
            self,
            targets: str | Iterable[str],
            normalizer: Optional[Callable[[str], str]] = utils.default_process,
            substring: bool = True,
    ):
        if isinstance(targets, str):
            targets = [targets]
        else:
            targets = list(targets)
        if len(targets) == 0:
            raise ValueError("At least one target string must be provided.")
        elif len(targets) == 1:
            self.single_target = True
        else:
            self.single_target = False
        self.targets = targets
        self.normalizer = normalizer
        if normalizer:
            self.targets_norm = [normalizer(t) for t in targets]
        else:
            self.targets_norm = targets
        self.substring = substring

    def __call__(self, s: str) -> FuzzyMatchResult | FuzzyMatchResults:
        if self.normalizer:
            s_norm = self.normalizer(s)
        else:
            s_norm = s

        results = []
        for t, t_norm in zip(self.targets, self.targets_norm):
            if self.substring:
                score = fuzz.partial_ratio(t, s_norm)
            else:
                score = fuzz.ratio(t, s_norm)
            result_kws = dict(string=s_norm, target=t_norm, score=score)
            if s_norm != s:
                result_kws['string_raw'] = s
            if t_norm != t:
                result_kws['target_raw'] = t
            results.append(FuzzyMatchResult(**result_kws))

        if self.single_target:
            results = results[0]
        else:
            results = FuzzyMatchResults(results=results)

        return results

    def to_bool_operator(self, threshold=80, raise_type_error=False, **kwargs) -> BooleanOperator:
        def f(s: str) -> bool:
            if not isinstance(s, str):
                if raise_type_error:
                    raise TypeError(f"Input must be a string, but got {type(s)}")
                return False
            result = self(s)
            if isinstance(result, FuzzyMatchResult):
                return result.score >= threshold
            else:
                best = result.best_match()
                return best.score >= threshold

        return bool_operator(f, **kwargs)
