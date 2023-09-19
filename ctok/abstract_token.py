from abc import ABC, abstractmethod


class AbstractToken(ABC):
    def __init__(self, *tokens: 'AbstractToken', cancelled=False):
        self.tokens = tokens
        self._cancelled = cancelled

    def __repr__(self):
        other_tokens = ', '.join([repr(x) for x in self.tokens])
        if other_tokens:
            other_tokens += ', '
        return f'{type(self).__name__}({other_tokens}cancelled={self.cancelled})'

    def __str__(self):
        cancelled_flag = 'cancelled' if self.cancelled else 'not cancelled'
        return f'<{type(self).__name__} ({cancelled_flag})>'

    @property
    def cancelled(self) -> bool:
        return self.is_cancelled()

    def keep_on(self) -> bool:
        return not self.is_cancelled()

    def is_cancelled(self) -> bool:
        if self._cancelled:
            return True

        elif any(x.is_cancelled() for x in self.tokens):
            return True

        elif self.superpower():
            return True

        return False

    def cancel(self) -> 'AbstractToken':
        self._cancelled = True
        return self

    @abstractmethod
    def superpower(self) -> bool:  # pragma: no cover
        pass
