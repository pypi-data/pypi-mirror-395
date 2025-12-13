# baqup-agent

SDK for building baqup backup agents in Python.

> ⚠️ **This is a placeholder package.** Full implementation coming soon.

## What is baqup?

[baqup](https://github.com/baqupio/baqup) is a container-native backup orchestration system. Agents are stateless containers that perform backup and restore operations on behalf of the controller.

This SDK provides everything needed to build a compliant baqup agent:

- **Contract types** - `ExitCode`, `AgentState`, `LogLevel`
- **Structured logging** - JSON logs with required fields
- **Redis communication** - Bus client with filesystem fallback
- **Heartbeat management** - Background thread with intent signalling
- **Staging utilities** - Atomic writes, checksums, path validation
- **Secret handling** - Wrapper preventing accidental exposure

## Installation

```bash
pip install baqup-agent
```

## Usage (Preview API)

```python
from baqup_agent import ExitCode, AgentState, LogLevel

# Exit codes are already available
print(ExitCode.SUCCESS)           # 0
print(ExitCode.USAGE_CONFIG_ERROR) # 64

# Agent states
print(AgentState.RUNNING)         # 'running'

# Secret wrapper (available now)
from baqup_agent import Secret
password = Secret("my-secret-password")
print(password)          # [REDACTED]
print(password.reveal()) # my-secret-password
```

## Contract Compliance

This SDK implements the [baqup Agent Contract Specification](https://github.com/baqupio/baqup/blob/main/AGENT-CONTRACT-SPEC.md):

| Section | Feature |
|---------|---------|
| §1 Lifecycle | State machine, signal handling |
| §2 Config | Environment variable loading |
| §3 Communication | Redis protocol, fallback |
| §4 Output | Atomic completion, manifests |
| §5 Errors | Exit code taxonomy |
| §6 Observability | Structured logging |
| §7 Security | Path validation, secrets |

## Related Packages

| Package | Description |
|---------|-------------|
| `baqup-schema` | Schema validation |
| `baqup-agent` | Agent SDK (this package) |

## Links

- [GitHub](https://github.com/baqupio/baqup)
- [Agent Contract Spec](https://github.com/baqupio/baqup/blob/main/AGENT-CONTRACT-SPEC.md)

## License

Fair Source License - see [LICENSE](./LICENSE) for details.
