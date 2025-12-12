# Probability-Guided Number Guessing Simulator

A production-grade CLI application for playing number guessing games with intelligent probability-based hints and comprehensive game tracking.

## 🎯 Features

- **Probability-Guided Hints**: Smart hints based on Bayesian probability analysis
- **Multiple Difficulty Levels**: Easy, Medium, Hard, and Expert profiles
- **Durable Storage**: JSON storage with robust file operations
- **Import/Export**: CSV support for data portability
- **Comprehensive Logging**: Detailed logs for debugging and tracking
- **Strict Validation**: Clear error messages for all inputs
- **Statistics Tracking**: Detailed game statistics and performance metrics
- **Simple & Clean Code**: Easy to understand for learning purposes
- **Maximum Compatibility**: Works with Python 2.7+ and all Python 3.x versions
- **Basic Dependencies Only**: Uses only core Python standard library modules

## 📦 Installation

### Prerequisites
- Python 2.7+ or Python 3.x (any version)
- No external dependencies (uses only basic Python standard library)
- **Maximum compatibility** - works on virtually any Python installation

### Install from Source

```bash
# Clone or download the project
cd Project_Source

# Install in development mode (editable install)
pip install -e .
# Or if pip is not available, use:
pip3 install -e .

# Or install normally
pip install .   # Use pip3 if pip is not available
```

After installation, the `guess-sim` command will be available globally.

## 🚀 Quick Start

```bash
# Play a game with default settings (medium difficulty)
python -m guess_simulator.cli play

# Or if installed:
guess-sim play

# Play with specific difficulty
guess-sim play -d hard

# Play with custom range
guess-sim play --min 1 --max 500 -a 15

# Play with verbose output
guess-sim play -v
```

## 📖 Usage

### Commands

#### Play a Game
```bash
guess-sim play [OPTIONS]

Options:
  -d, --difficulty {easy,medium,hard,expert}  Difficulty level
  --min INTEGER                               Minimum number
  --max INTEGER                               Maximum number
  -a, --attempts INTEGER                      Maximum attempts
  -s, --save                                  Save game after completion
  -v, --verbose                               Verbose output with probability info
```

**Example:**
```bash
guess-sim play -d expert -s -v
```

#### View Statistics
```bash
guess-sim stats [OPTIONS]

Options:
  -v, --verbose    Show detailed statistics and recent games
```

**Example:**
```bash
guess-sim stats -v
```

#### Export Data
```bash
guess-sim export [OPTIONS]

Options:
  -o, --output PATH    Output CSV file path (default: game_export.csv)
```

**Example:**
```bash
guess-sim export -o my_games.csv
```

#### Import Data
```bash
guess-sim import -i INPUT_PATH

Options:
  -i, --input PATH    Input CSV file path (required)
```

**Example:**
```bash
guess-sim import -i my_games.csv
```

#### Manage Configuration
```bash
guess-sim config [OPTIONS]

Options:
  --list           List all available profiles
  --show PROFILE   Show specific profile settings
```

**Example:**
```bash
guess-sim config --list
guess-sim config --show hard
```

## 🎮 Gameplay

When you start a game, you'll see:

```
============================================================
🎮 PROBABILITY-GUIDED NUMBER GUESSING SIMULATOR
============================================================
Difficulty: MEDIUM
Range: 1 - 100
Maximum Attempts: 10
Game ID: game-1701516845123-456789
============================================================

Enter your guess (1-100): 50
📉 Too high! Try a lower number.
📊 Attempts: 1/10

Enter your guess (1-100): 25
📈 Too low! Try a higher number.
💡 Hint: ♨️ Hot! The number is between 26 and 49.
📊 Attempts: 2/10
```

### Hint System

The game provides intelligent hints based on:

1. **Temperature Feedback**: 
   - 🔥 Very Hot (within 10% of range)
   - ♨️ Hot (within 25% of range)
   - 🌡️ Warm (within 50% of range)
   - ❄️ Cold (within 75% of range)
   - 🧊 Very Cold (beyond 75% of range)

2. **Probability-Based Range Narrowing**:
   - When possible numbers drop below threshold, shows exact range
   - Displays remaining possibilities in verbose mode

## ⚙️ Configuration

Configuration is hardcoded in `config.py` with the following profiles:

### Difficulty Profiles

| Profile | Range | Max Attempts | Hint Frequency |
|---------|-------|--------------|----------------|
| Easy    | 1-50  | 15           | Every 2 guesses |
| Medium  | 1-100 | 10           | Every 3 guesses |
| Hard    | 1-200 | 8            | Every 4 guesses |
| Expert  | 1-500 | 12           | Every 5 guesses |

### Storage Settings
- `format`: json (default for easy debugging)
- `data_dir`: Directory for storing game data (default: game_data)

## 📊 Game Statistics

The game tracks comprehensive statistics:

- Total games played
- Win/loss counts and percentages
- Average attempts per game
- Best and worst scores
- Guess history for each game

## 📂 Project Structure

```
guess_simulator/
├── __init__.py          # Package initialization
├── cli.py               # Command-line interface
├── config.py            # Configuration management
├── game.py              # Core game engine
├── logger.py            # Logging system
├── storage.py           # Data persistence
└── validator.py         # Input validation

tests/
├── __init__.py
├── test_game.py         # Game engine tests
├── test_storage.py      # Storage tests
├── test_validator.py    # Validation tests
└── test_integration.py  # Integration tests
```

## 🗂️ Data Storage

### File Structure
```
game_data/
├── games.json          # All game records
└── statistics.json     # Aggregated statistics

game.log                # Application logs
```

### Data Format

Games are stored in JSON format:
```json
{
  "game_id": "game-1701516845123-456789",
  "start_time": "2025-11-29T15:30:45",
  "end_time": "2025-11-29T15:32:10",
  "duration_seconds": 85.5,
  "min_number": 1,
  "max_number": 100,
  "target_number": 42,
  "max_attempts": 10,
  "attempts": 7,
  "guess_history": [50, 25, 37, 43, 40, 41, 42],
  "won": true,
  "finished": true
}
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test module
python -m unittest tests.test_game

# Run with verbose output
python -m unittest discover tests -v
```

**Test Suite**: 18 streamlined tests covering all core functionality

### Test Coverage
- **Unit Tests**: Game logic, validation, storage
- **Integration Tests**: Complete workflows and system integration
- All tests run in ~0.1 seconds

## 🔧 Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed troubleshooting guide.

### Common Issues

**Issue**: Command not found after installation
```bash
# Solution: Use Python module syntax
python -m guess_simulator.cli play
```

**Issue**: Permission denied when saving
```bash
# Solution: Check directory permissions
chmod 755 game_data/
```

**Issue**: Corrupted data file
```bash
# Solution: Delete the corrupted file to start fresh
# Data files are located in game_data/ directory
```

## 📝 Design Trade-offs

### Simplified Dependencies
- **Choice**: Basic Python standard library only (no pathlib, datetime, uuid, typing)
- **Rationale**: Maximum compatibility across Python versions (2.7+ and all 3.x)
- **Trade-off**: Slightly more verbose code (e.g., `os.path.join()` vs `Path() / file`)
- **Benefit**: Works on any Python installation without version constraints

### Storage Format
- **Choice**: JSON for primary storage
- **Rationale**: Human-readable, easy debugging, excellent for learning
- **Trade-off**: Slightly larger file size vs binary formats
- **Benefit**: Students can open and inspect data files directly

### Probability Algorithm
- **Choice**: Simple Bayesian range narrowing
- **Rationale**: Easy to understand for 1st-year students
- **Trade-off**: Not as sophisticated as ML models
- **Benefit**: Fast, deterministic, explainable

### Testing Approach
- **Choice**: Focused test suite (18 tests)
- **Rationale**: Covers core functionality without overwhelming complexity
- **Trade-off**: Fewer edge cases tested
- **Benefit**: Easy to understand and maintain for beginners

## 🚨 Limits and Edge Cases

### Input Limits
- **Number Range**: 1 to 2,147,483,647 (max int)
- **Max Attempts**: 1 to 1000
- **String Length**: 100 characters max

### Edge Cases Handled
- ✅ Corrupted data files (graceful error handling)
- ✅ Invalid user input (strict validation)
- ✅ Missing configuration (defaults provided)
- ✅ Disk full (graceful error handling)
- ✅ Large datasets (tested with 10,000+ games)

### Known Limitations
- Large ranges (>1M): Probability tracking uses significant memory
- Single-threaded: No async processing (keeps code simple)
- No static type checking (typing module not used for maximum compatibility)

## 📄 License

MIT License - Feel free to use for learning and projects!

## 👨‍💻 Author

Created as a 1st-year college project demonstrating:
- Production-grade Python development
- CLI application design
- Testing and documentation
- Software engineering best practices

## 🤝 Contributing

This is a learning project, but suggestions are welcome!

1. Test your changes thoroughly
2. Follow existing code style
3. Add tests for new features
4. Update documentation

## 📚 Learning Resources

This project demonstrates:
- **argparse**: CLI argument parsing
- **logging**: Professional logging practices  
- **json/csv**: Data serialization
- **os module**: File and directory operations
- **time module**: Timestamp handling and formatting
- **unittest**: Testing framework
- **OOP principles**: Classes, inheritance, encapsulation
- **Design patterns**: Singleton pattern in logger
- **Input validation**: Defensive programming
- **Compatibility**: Writing cross-version Python code

## 🔧 Technical Details

### Python Modules Used

The project uses **only** basic Python standard library modules for maximum compatibility:

**Core Modules:**
- `argparse` - Command-line interface
- `sys` - System operations
- `os` - File/directory operations
- `json` - Data persistence
- `csv` - Import/export functionality
- `logging` - Application logging
- `random` - Random number generation
- `time` - Timestamp management
- `unittest` - Test framework

**Modules NOT Used** (for compatibility):
- ❌ `pathlib` - Replaced with `os.path`
- ❌ `datetime` - Replaced with `time` module
- ❌ `uuid` - Custom ID generator using time + random
- ❌ `typing` - No type hints (works on Python 2.7+)
- ❌ `tempfile` - Fixed test directories
- ❌ `shutil` - Custom directory removal

This design choice ensures the project runs on **Python 2.7 through Python 3.13+** without any modifications!

---

**Happy Guessing! 🎯**
