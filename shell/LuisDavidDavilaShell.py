import os, sys, time, re

# fdOut = os.open("output.txt", os.O_CREAT | os.O_RDWR)
# # userInput = input()
# fdIn = os.open("input.txt", os.O_CREAT | os.O_RDWR)

# # os.write(fdIn, userInput.encode())
# pid = os.getpid()
# while True:
#     #userInput = input("->")
#     os.write(fdIn,(input("->") + "\n").encode())
#     rc = os.fork()
#     if rc < 0:
#         os.write(1,("something went wrong").encode())
#     elif rc == 0:    
#         sys.exit(0)
#     else:
#         os.wait()
#         userInput = os.read(fdIn, 10000)
#         if len(userInput) == 0: break
#         lines = re.split(b"\n", userInput)
#         for line in lines:
#             os.write(1,(line))

userInput = os.read(0,100)
