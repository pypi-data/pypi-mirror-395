# z2js - Z-Machine to JavaScript Compiler

A Python compiler that converts Z-machine story files (.z1-.z8) to playable JavaScript that runs in browsers or Node.js.

## Features

- **Multi-version support**: Handles Z-machine versions 1-8
- **Browser and Node.js**: Generated code works in both environments
- **Save/Load**: Game state persistence using localStorage (browser) or files (Node.js)
- **Interactive HTML UI**: Automatically generates a styled HTML wrapper for browser play
- **Modular architecture**: Clean separation between parser, code generator, and runtime

## Installation

```bash
pip install z2js
```

For development or from source, see [INSTALL.md](INSTALL.md).

## Usage

### Basic compilation

```bash
# Compile a Z-machine file to JavaScript
z2js game.z3

# This generates:
# - game.js: The JavaScript runtime and game data
# - game.html: Interactive HTML player interface
```

### Command-line options

```bash
# Specify output file
z2js game.z3 -o mygame.js

# Skip HTML generation
z2js game.z3 --no-html

# Verbose output (shows version, serial, etc.)
z2js game.z3 -v

# Show help
z2js --help
```

## Project Structure

```
z2js/
├── z2js           # Main compiler executable
├── zparser.py     # Z-machine file parser
├── opcodes.py     # Opcode decoder and instruction set
├── jsgen.py       # JavaScript code generator
└── test-output/   # Test compilation outputs
```

## Architecture

### Components

1. **Parser (zparser.py)**
   - Reads Z-machine story files
   - Parses headers, objects, dictionary
   - Decodes Z-strings and packed addresses

2. **Opcode Decoder (opcodes.py)**
   - Decodes all instruction forms (short, long, variable, extended)
   - Handles version-specific opcodes
   - Tracks operands, store variables, and branch targets

3. **JavaScript Generator (jsgen.py)**
   - Generates optimized JavaScript runtime
   - Embeds story data as base64
   - Creates complete Z-machine interpreter in JavaScript

### Runtime Features

The generated JavaScript runtime includes:

- **Memory management**: Dynamic and static memory regions
- **Stack machine**: Call stack and evaluation stack
- **Object system**: Full object tree with attributes and properties
- **I/O system**: Text output, keyboard input, save/restore
- **Z-string decoder**: Handles abbreviations and special characters

## Supported Games

The compiler has been tested with:
- Zork I-III
- Planetfall
- Enchanter
- Mini-Zork
- Most Inform 6/7 compiled games

## Browser Play

Open the generated HTML file in any modern browser:

```bash
# After compilation
open game.html  # macOS
xdg-open game.html  # Linux
start game.html  # Windows
```

Features in the browser interface:
- Retro terminal styling with green-on-black text
- Command history (arrow keys)
- Save/Load buttons
- Restart functionality
- Responsive design

## Node.js Usage

### Simple - Just run it:
```bash
node game.js
```

The game will automatically start when you run the file directly!

### Advanced - Use as a module:
```javascript
// Load the generated module
const { createZMachine } = require('./game.js');

// Create and run the Z-machine
const zm = createZMachine();

// Set up I/O callbacks
zm.outputCallback = (text) => process.stdout.write(text);
zm.inputCallback = // ... handle input

// Start the game
zm.run();
```

## Technical Details

### Z-Machine Versions

| Version | Max Size | Features | Status |
|---------|----------|----------|--------|
| 1-2 | 128KB | Basic | ✓ Supported |
| 3 | 128KB | Standard | ✓ Supported |
| 4 | 256KB | Plus | ✓ Supported |
| 5 | 256KB | Advanced | ✓ Supported |
| 6 | 256KB | Graphics | Partial |
| 7 | 320KB | Extended | Partial |
| 8 | 512KB | Large | ✓ Supported |

### Opcode Coverage

Currently implements core opcodes for:
- Control flow (call, return, jump, branch)
- Memory access (load, store, loadw, loadb)
- Object manipulation (get/set attributes, insert, remove)
- Text I/O (print, read, output streams)
- Arithmetic and logic operations
- Stack operations (push, pop)
- Game state (save, restore, restart, quit)

## Limitations

- Graphics opcodes (V6) are not fully implemented
- Sound effects are stubbed
- Some extended opcodes may not work correctly
- Mouse input not supported

## Future Enhancements

- Complete V6 graphics support
- Blorb file support for resources
- Debugger interface
- Optimization passes for generated code
- TypeScript output option

## License

This project is for educational purposes. Please respect the copyrights of original game files.

## Acknowledgments

Based on the Z-Machine Standards Document v1.1 by Graham Nelson and the work of the Interactive Fiction community.