from collections.abc import Sequence
from typing import TypeVar

# NOTE: T - переменная типа, которая гарантирует, что все элементы в последовательности одного типа.
T = TypeVar('T')


class UniqueSequence:
    """Валидатор для проверки, что все элементы последовательности уникальны.

    Используется как вызываемый объект в AfterValidator.

    Example:
        items: Annotated[
            Optional[Sequence[int]],
            AfterValidator(UniqueSequence()),
        ]
    """

    def __call__(self, seq: Sequence[T] | None) -> Sequence[T] | None:
        """Проверяет, что все элементы в последовательности уникальны.

        Args:
            seq: Последовательность значений или None.

        Returns:
            Исходную последовательность, если все элементы уникальны.

        Raises:
            ValueError: Если в последовательности есть дубликаты.
        """
        if seq is None or not seq:
            return None

        if len(seq) != len(set(seq)):
            raise ValueError('Элементы последовательности должны быть уникальными.')

        return seq


class WithinRange:
    """Валидатор для проверки, что все элементы последовательности находятся в диапазоне.

    Используется как вызываемый объект в AfterValidator без необходимости partial.

    Example:
        age: Annotated[
            Optional[tuple[int, int]],
            AfterValidator(WithinRange(4, 99)),
        ]
    """

    def __init__(self, min_value: int, max_value: int) -> None:
        """Инициализирует валидатор с границами диапазона.

        Args:
            min_value: Минимальное допустимое значение.
            max_value: Максимальное допустимое значение.
        """
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, seq: Sequence[int | float] | None) -> Sequence[int | float] | None:
        """Проверяет, что все элементы в последовательности находятся в диапазоне.

        Args:
            seq: Последовательность числовых значений или None.

        Returns:
            Исходную последовательность, если все элементы в диапазоне.

        Raises:
            ValueError: Если элемент выходит за пределы диапазона.
        """
        if seq is None:
            return seq

        for item in seq:
            if item < self.min_value or item > self.max_value:
                raise ValueError(f'Элемент последовательности {item} вне диапазона {self.min_value}-{self.max_value}.')

        return seq
