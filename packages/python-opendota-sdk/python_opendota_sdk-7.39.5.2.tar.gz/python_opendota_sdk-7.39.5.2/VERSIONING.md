# Versioning

Python OpenDota SDK follows a **4-part versioning scheme** that tracks the Dota 2 game patch:

```
v{major}.{minor}.{letter}.{sdk_release}
```

| Part | Meaning |
|------|---------|
| `major` | Dota 2 major version (e.g., 7) |
| `minor` | Dota 2 minor version (e.g., 39) |
| `letter` | Dota 2 patch letter: 0=none, 1=a, 2=b, 3=c, 4=d, 5=e, etc. |
| `sdk_release` | SDK release number for that Dota patch |

## Examples

| SDK Version | Dota 2 Patch | Notes |
|-------------|--------------|-------|
| `7.39.0.1` | 7.39 | First SDK release for 7.39 |
| `7.39.1.1` | 7.39a | First SDK release for 7.39a |
| `7.39.5.1` | 7.39e | First SDK release for 7.39e |
| `7.39.5.2` | 7.39e | Bug fix release, still 7.39e |
| `7.40.0.1` | 7.40 | First SDK release for 7.40 |

## Release Process

### Dev/Test Release (TestPyPI)

```bash
git tag v7.39.5.1-dev1
git push origin v7.39.5.1-dev1
```

Tags containing `-` (like `-dev1`, `-alpha1`, `-rc1`) publish to TestPyPI.

### Production Release (PyPI)

```bash
git tag v7.39.5.1
git push origin v7.39.5.1
```

Tags without `-` publish to PyPI.

## When to Bump Versions

- **New Dota patch**: Update `major.minor.letter`, reset `sdk_release` to 1
- **SDK bug fix**: Increment `sdk_release`
- **New SDK feature**: Increment `sdk_release`
