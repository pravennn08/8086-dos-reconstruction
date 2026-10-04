# Test cases

## Setup smoke check

Run `scripts/dev.ps1 -Action verify`, or the VS Code **DOS: Verify setup** task.

| ID | Check | Expected |
| --- | --- | --- |
| S-001 | Assemble and link src/rebuild.asm | TASM/TLINK succeed; build/REBUILD.COM exists |
| S-002 | Execute the starter program | Two exact banner lines from README |
| S-003 | Program termination | DOS process exit code 0 |

This check is specific to the initial scaffold. Replace it with target-based
comparisons when the reconstruction behavior is implemented.

## Original vs reconstruction (pending)

First record expected behavior by running the original, then compare the
reconstruction with identical inputs and environment.

| ID | Input/condition | Original result | Reconstruction result | Status |
| --- | --- | --- | --- | --- |
| R-001 | Empty input | Pending | Pending | Not run |
| R-002 | One character | Pending | Pending | Not run |
| R-003 | Mixed text | Pending | Pending | Not run |
| R-004 | Spaces/punctuation | Pending | Pending | Not run |
| R-005 | Observed maximum input length | Pending | Pending | Not run |
| R-006 | Input beyond that limit | Pending | Pending | Not run |

Include output bytes, prompts, line endings, and exit behavior where relevant.
Tests must reflect the selected target's actual interface.
