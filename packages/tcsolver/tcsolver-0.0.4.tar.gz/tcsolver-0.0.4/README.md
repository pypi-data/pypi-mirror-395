# tcsolver

A minimal Tencent slider captcha helper built with Playwright (Python). The demo opens the Tencent Captcha page, intercepts background image responses, saves them locally, and exposes basic hooks for solving.

## Quick Start

- Install Playwright browsers:

```
uv run playwright install
```

- Run the demo:

```
uv run main.py
```

This launches Chrome in non-headless mode, navigates to the Tencent Captcha product page, and prints the iframe bounding box. When the captcha background image request is intercepted, the image is saved in the current directory.

## Usage (Library)

```
from tcsolver.silder import SliderOptions, solve_slider

# Assume you already created a Playwright page
options = SliderOptions(
    validateButtonSelector="#captcha_click",
    iframeSelector="#tcaptcha_iframe_dy",
)

solve_slider(page, options)
```

- `SliderOptions` groups selectors used to open the captcha and locate its iframe.
- `solve_slider` registers a route handler to capture the background image (`index=1`) and saves it as `<image_value>.png` or `bg.png`.

## Build

```
uv run python -m build
```

Artifacts are written to `dist/` as an sdist (`.tar.gz`) and wheel (`.whl`).

## Project Structure

- `src/tcsolver/silder.py` core interception and entry function
- `main.py` runnable demo
- `pyproject.toml` packaging configuration

## Notes

- If the page appears blocked by strict load conditions, the demo uses `wait_until="domcontentloaded"` with increased timeouts.
- To run behind a proxy, configure Playwright’s `launch(proxy=...)` or environment variables as needed.
