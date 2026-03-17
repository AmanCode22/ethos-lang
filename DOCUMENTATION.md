# **📚 Ethos Language Documentation**

Welcome to the documentation for Ethos\! I wrote this document to help students, beginners, and potential contributors understand exactly how I built Ethos, what the syntax looks like, and the underlying architecture powering the whole thing.

**⚠️ HEAVY ALPHA WARNING: Ethos is a solo project and is currently in a heavy alpha stage. The internals documented here are evolving rapidly\!**

## **🎯 The Philosophy**

Programming can be incredibly intimidating. I created Ethos with one primary goal in mind: **to build the easiest, most accessible programming language in the world.** By replacing rigid symbols ({}, (), ;) with natural English sentences ending in periods, I wanted to remove the friction of learning syntax so you can focus purely on learning **logic**.


## **🏗️ How It Works (Under the Hood)**

Right now, Ethos acts as a very smart translator that converts English into Python logic in real-time. Here is how my pipeline works:

### **1. The Lexer (lexer.py)**

When you type a sentence like run math.sqrt with 144., the Lexer breaks it apart.

* It splits your text by periods (.) to separate lines.  
* It uses POSIX shell-like splitting (shlex) to separate words safely, ensuring strings enclosed in quotes ("hello world") stay perfectly intact.  
* I also built a multi-word mapper to group phrases like is not, is above, bring in, and otherwise if into single logical tokens.

### **2\. The Parser (parser.py)**

This is the brain of the operation. It takes the tokenized words from the Lexer and maps them to Python constructs.

* bring in becomes import.  
* set x to 5 becomes x \= 5\.  
* how to function\_name with args becomes def function\_name(args):.  
* I also programmed it to handle indentation automatically by tracking your end. statements\!

### **3\. The Executer (executer.py)**

Once the Python code is generated, I built Ethos to create an **isolated memory box** (essentially a Python dictionary).

* When you run code, variables are saved to this dictionary.  
* When you type the next line in the REPL, the Executer passes this dictionary back in. This is the magic that ensures your variables and imports persist naturally across lines without wiping themselves out.  
* It also uses Python's ctypes library to load high-performance C/Rust code (Hard Traits).

## **📦 The Forge Package Manager CLI**

Forge is the package manager I built for Ethos. Unlike Python's pip, I designed Forge to be entirely **zero-dependency**. It is a massive, professional-grade CLI switchboard that handles both pure Python code and compiled native binaries.

### **🐍 Managing Soft Traits (Python Modules)**

These commands handle pure Python .whl and source files, bypassing pip entirely.

| Command | Action |
| :---- | :---- |
| forge pymodule get \<name\> | Fetches PyPI metadata, finds the best OS-specific Wheel, and installs it. |
| forge pymodule wheel get \<url\> | Downloads a specific .whl file from a direct URL and extracts it. |
| forge pymodule wheel local \<path\> | Extracts a .whl file already downloaded on your local hard drive. |
| forge pymodule sdist get \<url\> | Downloads a .tar.gz or .zip source distribution from a direct URL. |
| forge pymodule sdist local \<path\> | Extracts a local source distribution archive into the backpack. |

### **⚙️ Managing Hard Traits (Native Binaries)**

These commands handle the high-performance C, Rust, and Java (GraalVM) compiled binaries (.so, .dll, .dylib).

| Command | Action |
| :---- | :---- |
| forge get \<url\> | Downloads a pre-compiled native binary trait from a direct URL. |
| forge local \<path\> | Registers a locally compiled native binary into the backpack. |

### **📦 Inventory & Cleanup**

These commands allow you to see exactly what powers Ethos currently has loaded and clean up old traits.

| Command | Action |
| :---- | :---- |
| forge list | Shows a complete inventory of all installed traits (both Soft and Hard). |
| forge list pymodule | Filters the inventory to show only Python-based soft traits. |
| forge list native | Filters the inventory to show only compiled C-ABI hard traits. |
| forge remove \<name\> | Deletes a specific Hard Trait binary from the system. |
| forge remove pymodule \<name\> | Recursively deletes a specific Soft Trait folder from the system. |

## **🖥️ The Ethos IDE (Alpha)**

To make development even smoother, I'm currently building a simple Qt-based IDE for Ethos. Like the language itself, this is in **heavy alpha stage**. It provides a streamlined graphical interface equipped with both a built-in **runner** and **compiler**, allowing you to write, test, and compile code into standalone executables directly from the editor.

## **📖 Comprehensive Syntax Reference**

A golden rule in Ethos: **Every statement must end with a period (.)**.

### **Comments**
```
note This is a single line comment.

notes  
This is a multi-line comment.  
I can type whatever I want here.  
endnotes.
```

### **Output**

```
say "Hello World!".
```

### **Variables and Slicing**

```
set name to "Aman".  
delete variable name.

note This acts like python's text[0:4]  
set text from 0 to 4. 

```
### **Math & Operations**

```
set score to 10.

add 5 to score.  
subtract 2 from score.

note You can also use inline math words:  
set total to 5 plus 5.  
set difference to 10 minus 2.  
set product to 5 times 5.  
set fraction to 10 divided by 2.  
set power to 2 to the power of 3.

```

### **Logic & Comparisons**

* is (==), is not (\!=), is above (\>), is below (\<), is at least (\>=), is at most (\<=)

### **Conditional Logic (If / Otherwise If / Otherwise)**

```
set power to 100.

if power is at least 50.  
    say "System is running optimal.".  
otherwise if power is below 50 and power is above 10.  
    say "System is at half capacity.".  
otherwise.  
    say "System power is critically low!".  
end.
```

### **Loops**

```
note 1. Fixed count loop  
repeat 3.  
    say "Hello!".  
end.

note 2. Stepping loop (for i in range...)  
count variable i 1 to 10 stepping 2.  
    say i.  
end.

note 3. Conditional loop  
set battery to 5.  
while battery is above 0.  
    say battery.  
    subtract 1 from battery.  
end.
```

### **Functions & Traits**

```
how to greet with user_name.  
    say "Welcome back!".  
    say user_name.  
end.

run greet with "Aman".

bring in random.  
run random.randint with 1, 10.

```
## **🛠️ Developer & Debug Modes**

I built special commands directly into the parser to help debug the language.

* python. / pythonend. \-\> Turns ON/OFF Python translation mode (prints generated Python).  
* debug. / debugend. \-\> Turns ON/OFF Lexer debug mode (prints raw tokens).

## **🚀 The Roadmap: C and Rust Rewrite**

Right now, I am leaning on Python and Nuitka for rapid development.

However, as Ethos matures, **my ultimate goal is to rewrite the core Lexer, Parser, and Memory Executer entirely in C or Rust.** Writing the core in a low-level language will allow Ethos to bypass the Python virtual machine overhead, drop memory usage significantly, and execute insanely fast.

Until I get there, I'll be focusing on maturing the syntax and building out the dual-trait plugin ecosystem\!
