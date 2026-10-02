"""Flat, synchronous research-controller lifecycle; effects remain in autoresearch."""
from dataclasses import dataclass, field

# Source, event, target, required guard value (None means unconditional).
TRANSITIONS = (
    ('idle', 'start', 'checking_lock', None),
    ('checking_lock', 'lock_valid', 'initializing', None),
    ('initializing', 'baseline_evaluated', 'ready', None),
    ('ready', 'candidate_started', 'evaluating', None),
    ('evaluating', 'keep', 'ready', 'accepted'),
    ('evaluating', 'reject', 'ready', 'rejected'),
    ('ready', 'trials_finished', 'canonical_evaluation', None),
    ('canonical_evaluation', 'canonical_evaluated', 'verified', None),
    ('verified', 'dry_run', 'complete', 'dry_run'),
    ('verified', 'write_requested', 'persisting', 'write_enabled'),
    ('persisting', 'receipts_written', 'promotion_decision', None),
    ('promotion_decision', 'promote', 'promoting', 'promotable'),
    ('promotion_decision', 'retain', 'complete', 'not_promotable'),
    ('promoting', 'champion_written', 'complete', None),
)
ACTIVE = frozenset(row[0] for row in TRANSITIONS) - {'idle'}


class InvalidTransition(RuntimeError):
    pass


@dataclass
class ResearchLifecycle:
    state: str = 'idle'
    trace: list = field(default_factory=list)

    def send(self, event: str, **guards: bool) -> None:
        for source, name, target, required in TRANSITIONS:
            if source == self.state and name == event and (not guards if required is None else set(guards) == {required} and guards[required] is True):
                self.trace.append({'source': source, 'event': event, 'target': target, 'guards': dict(guards)})
                self.state = target
                return
        raise InvalidTransition(f'{self.state}: invalid event/guard {event!r}/{guards!r}')

    def fail(self) -> None:
        if self.state in ACTIVE:
            self.trace.append({'source': self.state, 'event': 'infrastructure_error', 'target': 'failed', 'guards': {}})
            self.state = 'failed'


def diagram() -> str:
    lines = ['stateDiagram-v2', '    [*] --> idle']
    for source, event, target, guard in TRANSITIONS:
        label = event + (f' [{guard}]' if guard else '')
        lines.append(f'    {source} --> {target}: {label}')
    for source in sorted(ACTIVE):
        lines.append(f'    {source} --> failed: infrastructure_error')
    lines.extend(['    complete --> [*]', '    failed --> [*]'])
    return '\n'.join(lines) + '\n'
