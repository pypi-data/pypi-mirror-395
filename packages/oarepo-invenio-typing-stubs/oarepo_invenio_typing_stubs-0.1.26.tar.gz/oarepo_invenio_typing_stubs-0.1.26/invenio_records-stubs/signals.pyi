from blinker import Namespace, Signal

_signals: Namespace

before_record_insert: Signal
after_record_insert: Signal
before_record_update: Signal
after_record_update: Signal
before_record_delete: Signal
after_record_delete: Signal
before_record_revert: Signal
after_record_revert: Signal

__all__: tuple[str, ...]
