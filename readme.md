Evaluate command for Clojure [Sublime Text 2]

This plugin evaluates current selections.
You need socket-repl from http://github.com/kondratovich/socket-repl/

Usage:
1. Run socket-repl
2. Drop 'clo_evaluate.py' in 'Packages/Default/' folder
3. Define command in your settings, for example:
    { "keys": ["ctrl+alt+x"], "command": "clo_evaluate" }