---
name: take-photo
description: Capture a single webcam photo with the webcam-cli CLI, including autofocus warmup and camera fallback. Use when the user asks to take a photo, snapshot, or webcam image.
---

# Take Photo

Capture one webcam frame quickly using this repository's CLI flow.

## Default command

Run from `/Users/lasaths/Documents/GitHub/webcam-cli`:

```bash
uv run webcam-cli --capture-photo /Users/lasaths/Documents/GitHub/Bahnblick/.verification/webcam_capture.jpg --autofocus-seconds 2.0 --camera-index 0
```

## Rules

1. Save captures to `/Users/lasaths/Documents/GitHub/Bahnblick/.verification/` unless the user asks for another path.
2. Use `--autofocus-seconds` (default `2.0`) so the camera can settle focus and exposure.
3. If camera index `0` fails, retry once with camera index `1`.
4. Keep it minimal: one terminal command per attempt, no new scripts.
5. Report the final output file path for immediate opening.
