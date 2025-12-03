# Assets Directory

Place application icons here:

- `icon.png` - Main icon (512x512 PNG)
- `icon.icns` - Mac icon (for .dmg builds)
- `icon.ico` - Windows icon (for .exe builds)

## Creating Icons

### Mac (.icns)
```bash
# Using iconutil (Mac only)
iconutil -c icns icon.iconset
```

### Windows (.ico)
Use online converters or ImageMagick:
```bash
convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

For now, the app will use default Electron icons if these files are missing.

