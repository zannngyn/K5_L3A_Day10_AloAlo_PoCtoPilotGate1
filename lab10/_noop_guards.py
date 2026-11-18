"""Guards that allow everything = the system BEFORE your fix. LOCKED."""
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    return Verdict.allow()
