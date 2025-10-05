# Source Code Directory

Place your ESP32 source files here:

## Main Application File
- **Recommended**: `main.cpp` for C++ projects
- **Alternative**: `main.ino` for Arduino-style projects

## Additional Files
- **Headers**: `.h` or `.hpp` files
- **Source**: `.cpp` or `.c` files
- **Arduino**: `.ino` files (if using Arduino-style)

## Example Structure
```
src/
├── main.cpp          # Your main application
├── config.h          # Configuration header
├── sensors.cpp       # Sensor handling
├── sensors.h         # Sensor header
└── utils.cpp         # Utility functions
```

## Getting Started
1. **Option 1**: Rename `main.example.cpp` to `main.cpp` and modify it
2. **Option 2**: Create your own `main.cpp` or `main.ino` file
3. Add your project code
4. Build with `.\build.ps1 build`
5. Upload with `.\build.ps1 upload`

## Example File
- `main.example.cpp` - Simple LED blink example (rename to `main.cpp` to use)

PlatformIO will automatically compile all source files in this directory.