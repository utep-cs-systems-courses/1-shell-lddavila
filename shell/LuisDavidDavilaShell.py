#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 20:34:49 2022

@author: ldd775
"""
import os, sys, time, re
import fileinput


def userEnteredExit():
    sys.exit()
    
def userEnteredCD(userInput):
    try:
        os.chdir(userInput[1])
    except FileNotFoundError:
        print("File Not Found")
    except PermissionError:
        print("PermissionError")
    except NotADirectoryError:
        print("NotADirectory")    
    userInput = None;
    return None

def redirectOutputDetected(userInput):
    print("WENT INTO REDIRECT OUTPUT")
    try:
        userInput[1] = re.sub(">", "", userInput[1])
        userInput[1] = re.sub("\s", "", userInput[1], 1)
        os.close(1)
        os.open(userInput[1],os.O_CREAT | os.O_WRONLY)
        userInput = [userInput[0]]
    except:
        print("Something went wrong with output redirection")
    return userInput

def redirectInputDetected(userInput):
    print("WENT INTO REDIRECT INPUT")
    try:
        userInput[1] = re.sub("<","",userInput[1])
        os.close(0)
        userDesignatedFD = userInput[0]
        os.open(userDesignatedFD, os.O_RDONLY)
        userInput[0] = userInput[1]
        userInput[1] = (os.read(0,10000)).decode()
    except:
        print("SOMETHING WENT HECKA WRONG WITH INPUT REDIRECTION")
    return userInput

def backgroundTaskDetected(userInput):
    os.SCHED_IDLE
    userInput[0] = userInput[1]
    
def determinePath(userInput):
    if (userInput[0] =="exit"):     #check for the special input "exit" which terminates the shell
        print("exit path followed")
        userEnteredExit() #terminates the program
    try:
        if re.search(">",userInput[1]) != None: #checks if there are any redirect output commands
            userInput = redirectOutputDetected(userInput)
            print("Redirect output path followed")
    except:
        pass
    try:
        if re.search("<",userInput[1]) != None: #checks if there are any redirect input commands
            userInput = redirectInputDetected(userInput)
            print("redirect input path followed")
            
    except:
        pass
    try:
        if re.search("&",userInput[0]) != None: #checks if the task should be run in the background
            userInput = backgroundTaskDetected(userInput)
            print("Background path followed")
    except:
        pass
    try:
        if re.search("\|",userInput[1]) != None: #checks for pipes
               print("PIPE WAS FOUND")
               multipleCommands(userInput)
               print("Pipe path followed")
               userInput = None
    except:
        pass


        
    if (userInput != None):
        singleCommand(userInput)
        print("single command path followed")
        
def singleCommand(userInput):
        #print("THIS IS THE VALUE OF USER INPUT AT THE BEGINNING OF SINGLE COMMAND: ", userInput )
        rc = os.fork() #creates the child
        if rc < 0:#in case the fork fails
             os.write(2, ("fork failed, returning %d\n" % rc).encode()) 
             sys.exit(1)
        elif rc == 0:
            
            try:
                args = [userInput[0], userInput[1]]
                #print("args Went into the try")
                #print(args)
            except:
                #print("args went into the except")
                args = [userInput[0]]   
            #print("This is the value of args!!!!!!!!!!!!!!!!", args)
            #os.set_inheritable(1, True)
            sets = re.split(":", os.environ['PATH'])

            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ) # try to exec program
                    break;
                except FileNotFoundError:             # ...expected
                    if(dir == set[len(set)-1]):    
                        os.write(1,(args[0] +" Command not found\n").encode())
                             # terminate with error
            sys.exit(0)
            print("The child did not exit")
        else:
            childPidCode = os.wait()
            os.write(1, ("Program %d terminated with exit code %d\n" % childPidCode).encode())
            #sys.exit(0)

def multipleCommands(userInput):
    print("WENT INTO MULTIPLE COMMANDS")
    readFD, writeFD = os.pipe()
    
    
    for f in (readFD, writeFD):
        os.set_inheritable(f, True)
        
    rc = os.fork()
    if rc<0:
        print("Pipe failed")
    elif rc ==0:
        os.close(1)
        os.dup(writeFD)
        os.close(writeFD)
        os.close(readFD)
        args = [userInput[0]]    
        sets = re.split(":", os.environ['PATH'])

        for dir in re.split(":", os.environ['PATH']): # try each directory in path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) # try to exec program
                
            
            except FileNotFoundError:             # ...expected
                 if(dir == sets[len(sets)-1]):    
                      os.write(1,(args[0] +" Command not found\n").encode())
              
                     
                # terminate with error
        sys.exit(0)
        
    else:
        os.waitpid(rc, 0)
        rc = os.fork()
        if rc<0:
            print("something went wrong when creating the second child")
        elif rc ==0:
            os.close(0)
            os.dup(readFD)
            os.close(readFD)
            os.close(writeFD)
            userInput[0] = re.sub("\|\s", "",userInput[1])
            #userInput[1] = (os.read(0,10000)).decode()
            args = [userInput[0]]
            #print("THIS IS WHAT ARGS IS FOR SECOND CHILD!!!!!!!!!!!!!!!!!!",args)
            os.set_inheritable(1, True)
            sets = re.split(":", os.environ['PATH'])

            for dir in re.split(":", os.environ['PATH']): # try each directory in path
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program, args, os.environ) # try to exec program
                    break;
                except FileNotFoundError:             # ...expected
                    if(dir == sets[len(sets)-1]):    
                        os.write(1,(args[0] +" Command not found\n").encode())
            sys.exit(0)                 # terminate 
        else:
            os.waitpid(rc, 0)
            

if __name__ == "__main__":
    pid = os.getpid()
    while True:
        
        
        os.write(1,("->").encode())                         #print the prompt
        userInput = (os.read(0,100))                        #get the next 100 chars of input from user
        userInput = (userInput.decode()).replace("\n","")   #remove the "\n" char
        if(len(userInput) == 0):
            continue
        #print("This is the user input given: " + userInput)
        userInput = (userInput).split(" ",1)                #split the command into 2 parts
        if(userInput[0] == "cd"):       #checks for special input "cd" which will change the directory
            userInput = userEnteredCD(userInput) #returns a None user input so that execution will fail
            continue         #execution failing is ideal since the order that needs to performed in this case has already been done
        determinePath(userInput)
