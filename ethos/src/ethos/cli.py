import sys
from .lexer import lex
from .executer import run,create_enviroment
from .parser import parse
from sys import exit

def main():
    if len(sys.argv)==1:
        start_repl()
        exit()
    elif len(sys.argv)!=2:
        print("Usage: ethosrun <filename.ethos>")
        exit()
    filename=sys.argv[1]
    if not filename.endswith(".ethos"):
        print("Filename must have extension .ethos")
        exit()
    with open(filename,encoding="utf-8") as f:
        data=f.read()
    tokens=lex(data)
    if not tokens or tokens==[]:
        exit()
    generated_python_code=parse(tokens)
    if not generated_python_code or generated_python_code=="" or generated_python_code==" ":
        exit()
    run(generated_python_code)

def start_repl():
    repl_memory=create_enviroment()
    buffer=""
    open_blocks=0
    while True:
        if open_blocks==0:
            command_input=input("ethos > ")
        else:
            command_input=input("... ")
        if command_input=="exit" or command_input=="quit":
            break
        if not command_input.endswith("."):
            command_input+="."
        tokens=lex(command_input)
        if not tokens or tokens==[]:
            continue
        if tokens[0][0] in ["repeat","while","if","how",'count']:
            open_blocks+=1
        elif tokens[0][0]=="end" and open_blocks!=0:
            buffer+="end."
            open_blocks-=1
            tokens=lex(buffer)
            if not tokens or tokens==[]:
                buffer=""
                continue
            python_code=parse(tokens)
            if not python_code or python_code=="" or python_code==" ":
                buffer=""
                continue
            run(python_code,repl_memory)
            buffer=""
            continue
        elif open_blocks==0 and tokens[0][0]=="end":
            exit()
        if open_blocks>0:
            buffer+=command_input+"\n"
            continue
        python_code=parse(tokens)
        if not python_code or python_code==" " or python_code=="":
            continue
        run(python_code,repl_memory)
