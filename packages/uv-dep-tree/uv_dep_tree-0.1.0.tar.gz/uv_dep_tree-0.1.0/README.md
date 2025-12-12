# uv-dep-tree

Visualize `uv.lock` dependency sizes as a nested tree with deduplication metrics.

## Installation

```bash
# Run directly without installing (recommended)
uvx uv-dep-tree

# Or install globally
pip install uv-dep-tree
```

## Usage

```bash
# Generate HTML from uv.lock in current or parent directory
uv-dep-tree

# Generate from specific file
uv-dep-tree /path/to/uv.lock

# Custom output path
uv-dep-tree /path/to/uv.lock -o deps.html

# Live server with auto-refresh on file changes
uv-dep-tree --serve

# Live server on custom port
uv-dep-tree --serve --port 3000
```

## Understanding the Output

**Background colors:**
- Blue = package's wheel size
- Green = dependencies' sizes

**Number colors:**
- Purple = virtual size (as if duplicated)
- Green = amortized size (actual, after deduplication)

**Columns:** Wheel | Deps | Tree — each showing Virtual / Amortized

**Occurrence badges** (e.g., `×3`): Package appears 3 times in tree; amortized size is divided by 3.

## Deduplication Math

When package appears N times: Amortized = Size ÷ N. The root's amortized total equals actual download size.
