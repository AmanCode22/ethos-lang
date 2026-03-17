# **📚 Ethos Language Documentation**

Welcome to the official documentation for Ethos\! This document is designed to help students, beginners, and contributors understand how Ethos works, its syntax, and the underlying architecture that powers it.

## **🎯 The Philosophy**

Programming can be intimidating. Ethos is made with one primary goal: **to create the easiest, most accessible programming language in the world.** By replacing rigid symbols ({}, (), ;) with natural English sentences ending in periods, Ethos removes the friction of learning syntax so students can focus purely on learning **logic**. Because it runs perfectly on Windows, macOS, Linux, and **Android via Termux**, you can learn to code absolutely anywhere.

## **🏗️ How It Works (Under the Hood)**

Ethos isn't a completely new compiler from scratch (yet\!). Right now, it acts as a very smart translator that converts English into Python logic in real-time. Here is how the pipeline works:

### **1\. The Lexer (lexer.py)**

When you type a sentence like run math.sqrt with 144., the Lexer breaks it apart.

* It splits your text by periods (.) to separate lines.  
* It uses POSIX shell-like splitting (shlex) to separate words safely, ensuring strings enclosed in quotes ("hello world") stay intact.

### **2\. The Parser (parser.py)**

This is the brain. It takes the tokenized words and maps them to Python constructs.

* bring in becomes import.  
* set x to 5 becomes x \= 5\.  
* how to function\_name with args becomes def function\_name(args):.  
* It handles indentation automatically by tracking end. statements.

### **3\. The Executer (executer.py)**

Once the Python code is generated, Ethos doesn't just run it blindly. It creates an **isolated memory box** (a Python dictionary).

* When you run code, variables are saved to this dictionary.  
* When you type the next line in the REPL, the Executer passes this dictionary back in. This ensures your variables and imports persist naturally across lines.  
* It also uses Python's ctypes library to load high-performance C/Rust code (Hard Traits).

## **📦 The Forge Package Manager**

Forge is the package manager for Ethos. Unlike pip (Python's default package manager), Forge is **zero-dependency**.

**How it works:**

1. You run ./forge/main.bin install requests.  
2. Forge queries the PyPI JSON API using standard urllib.  
3. It finds the .whl (Python wheel) that matches your OS and Python version.  
4. It downloads it and uses standard zipfile to extract the code directly into \~/.ethos/traits/.  
5. Ethos automatically checks this traits folder when you use the bring in command\!

## **🖥️ The Ethos IDE (Alpha)**

To make development even smoother, Ethos includes a simple Qt-based IDE. Currently in its **alpha stage**, this IDE provides a streamlined graphical interface equipped with both a built-in **runner** and **compiler**. This allows users to write, test, and compile their Ethos code into standalone executables directly from the editor without needing to use the command line.

## **📖 Syntax Reference**

Every statement in Ethos **must end with a period (.)**.

### **Variables**

note This is a comment.  
set name to "Aman".  
set age to 20\.

### **Math & Operations**

set score to 10\.  
add 5 to score.  
subtract 2 from score.

*Behind the scenes, Ethos translates is, is not, is above, is below into \==, \!=, \>, \<.*

### **Conditional Logic (If / Otherwise)**

set power to 100\.

if power is above 50\.  
    say "System is running optimal.".  
otherwise if power is 50\.  
    say "System is at half capacity.".  
otherwise.  
    say "System power is low\!".  
end.

### **Loops**

**Repeat a set amount of times:**

repeat 3\.  
    say "Hello\!".  
end.

**While loops:**

set battery to 5\.  
while battery is above 0\.  
    say battery.  
    subtract 1 from battery.  
end.

### **Functions**

You can define your own reusable code blocks using how to.

how to greet with user\_name.  
    say "Welcome back\!".  
    say user\_name.  
end.

run greet with "Aman".

### **Using Python Libraries**

You can import standard Python libraries or Traits installed via Forge.

bring in random.  
run random.randint with 1, 10\.

## **🚀 The Roadmap: C and Rust Rewrite**

Right now, Ethos leverages Python and Nuitka. It is excellent for rapid development and leveraging Python libraries.

However, as the language matures, **the ultimate goal is to rewrite the core Lexer, Parser, and Memory Executer entirely in C or Rust.** \* **Why?** Writing the core in a low-level language will allow Ethos to bypass the Python virtual machine overhead, drop memory usage significantly, and execute orders of magnitude faster.

* Until then, Ethos will continue to mature its syntax and build out its dual-trait ecosystem\!
