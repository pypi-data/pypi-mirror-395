# 🔪 kport - Cross-Platform Port Inspector and Killer

A simple, powerful command-line tool to inspect and kill processes using specific ports on Windows, Linux, and macOS.

## ✨ Features

- 🔍 **Inspect ports** - Find which process is using a specific port
- 🔎 **Inspect by process name** - Find all processes matching a name and their ports
- 🔪 **Kill processes** - Terminate processes using specific ports
- 📋 **List all ports** - View all listening ports and their processes
- 🎯 **Kill by process name** - Kill all processes matching a name (e.g., "node", "python")
- 🔥 **Kill multiple ports** - Kill processes on multiple ports at once
- 🎨 **Colorized output** - Easy-to-read colored terminal output
- ✅ **Confirmation prompts** - Safety confirmation before killing processes
- 🌍 **Cross-platform** - Works on Windows, Linux, and macOS
- 🚀 **Easy to use** - Simple command-line interface

## 📦 Installation

### Quick Install (Once Published to PyPI)

```bash
pip install kport
```

### Install from GitHub

```bash
pip install git+https://github.com/farman20ali/port-killer.git
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/farman20ali/port-killer.git
cd port-killer

# Install
pip install .
```

### Install for Development

```bash
# Install in editable mode
pip install -e .
```

After installation, `kport` will be available globally in your terminal.

### Run Without Installing

```bash
# Run directly with Python
python kport.py -h
```

> 📖 For detailed installation instructions, see [INSTALL.md](INSTALL.md)
> 
> 🚀 For publishing instructions, see [PUBLISH.md](PUBLISH.md)

## 🚀 Usage

### Inspect a port

Find out which process is using a specific port:

```bash
kport -i 8080
```

Example output:
```
🔍 Inspecting port 8080...

✓ Port 8080 is being used by PID 12345

Process Information:
──────────────────────────────────────────────────
PID: 12345
Image Name: node.exe
Session Name: Console
Mem Usage: 45,678 K
```

### Inspect by process name

Find all processes matching a name and see what ports they're using:

```bash
kport -ip node
```

Example output:
```
🔍 Inspecting processes matching 'node'...

Found 3 connection(s) for processes matching 'node':

PID        Process                   Port       State          
──────────────────────────────────────────────────────────────────────
12345      node.exe                  3000       LISTENING      
                                     3001       LISTENING      
12346      node.exe                  8080       LISTENING      

✓ Total processes found: 2
✓ Total connections: 3
```

### Kill a process on a port

Terminate the process using a specific port:

```bash
kport -k 8080
```

Example output:
```
🔪 Attempting to kill process on port 8080...

Found PID 12345 using port 8080

Process to be terminated:
PID: 12345
Image Name: node.exe

Are you sure you want to kill this process? (y/N): y

✓ Successfully killed process 12345
Port 8080 is now free.
```

### List all listening ports

View all active listening ports and their associated processes:

```bash
kport -l
```

Example output:
```
📋 Listing all active ports...

Protocol   Local Address            State           PID       
──────────────────────────────────────────────────────────────────────
TCP        0.0.0.0:80               LISTENING       1234      
TCP        0.0.0.0:443              LISTENING       1234      
TCP        0.0.0.0:3000             LISTENING       5678      
TCP        0.0.0.0:8080             LISTENING       9012
```

### Kill by process name

Kill all processes matching a specific name:

```bash
kport -kp node
```

Example output:
```
🔪 Killing all processes matching 'node'...

Found 3 process(es) matching 'node':
──────────────────────────────────────────────────
  PID 12345: node.exe
  PID 12346: node.exe
  PID 12347: node.exe

Are you sure you want to kill 3 process(es)? (y/N): y

✓ Killed PID 12345
✓ Killed PID 12346
✓ Killed PID 12347

✓ Successfully killed 3/3 process(es)
```

### Kill multiple ports at once

Kill processes on multiple ports simultaneously:

```bash
kport -ka 3000 3001 3002
```

Example output:
```
🔪 Killing processes on 3 port(s)...

Found processes on 3 port(s):
──────────────────────────────────────────────────
  Port 3000: PID 12345 (node.exe)
  Port 3001: PID 12346 (node.exe)
  Port 3002: PID 12347 (python.exe)

Are you sure you want to kill 3 process(es)? (y/N): y

✓ Killed process on port 3000 (PID 12345)
✓ Killed process on port 3001 (PID 12346)
✓ Killed process on port 3002 (PID 12347)

✓ Successfully killed 3/3 process(es)
Ports freed: 3000, 3001, 3002
```

### Show help

```bash
kport -h
```

### Show version

```bash
kport -v
```

## 📚 Command-Line Options

| Option | Long Form | Description |
|--------|-----------|-------------|
| `-i PORT` | `--inspect PORT` | Inspect which process is using the specified port |
| `-ip NAME` | `--inspect-process NAME` | Inspect all processes matching the given name and their ports |
| `-k PORT` | `--kill PORT` | Kill the process using the specified port |
| `-kp NAME` | `--kill-process NAME` | Kill all processes matching the given name |
| `-ka PORT [PORT ...]` | `--kill-all PORT [PORT ...]` | Kill processes on multiple ports at once |
| `-l` | `--list` | List all listening ports and their processes |
| `-v` | `--version` | Show version information |
| `-h` | `--help` | Show help message |

## 🛠️ Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

### Platform-specific tools

The tool uses platform-native commands:

- **Windows**: `netstat`, `tasklist`, `taskkill`
- **Linux/macOS**: `lsof`, `ps`, `kill`

These tools are typically pre-installed on all platforms.

## 🔧 Development

### Clone and setup

```bash
git clone https://github.com/farman20ali/port-killer.git
cd port-killer

# Install in development mode
pip install -e .
```

### Run tests

```bash
# Test inspecting a port
kport -i 80

# Test listing ports
kport -l
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Important Notes

- **Administrator/sudo privileges**: Killing processes may require elevated privileges on some systems
- **Port validation**: Port numbers must be between 1 and 65535
- **Safety**: The tool asks for confirmation before killing any process
- **Multiple processes**: If multiple processes use the same port, the first one found will be shown/killed

## 🐛 Troubleshooting

### "Permission denied" errors

On Linux/macOS, you may need to run with sudo:
```bash
sudo kport -k 80
```

On Windows, run your terminal as Administrator.

### Port not found

Make sure the port number is correct and that a process is actually using it. Use `kport -l` to see all active ports.

### Color output not working on Windows

Colors should work on Windows 10 and later. If you're on an older version, colors may not display correctly.

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/port-killer](https://github.com/yourusername/port-killer)

---

Made with ❤️ for developers who are tired of hunting down processes
