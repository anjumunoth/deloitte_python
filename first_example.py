import asyncio

def greet():
    print("HI there!")
    print("Hello, World!")  
    print("Bye")

async def greetAsync():# creating an async function also called coroutine
    print("HI there from Asyncio!")
    await asyncio.sleep(2) # simulate a delay for 2 secs; crates an async task and waits for it to complete
    #await is pause keyword
    print("Hello, World from Asyncio!")  
    print("Bye from Asyncio")


def greetWithNoWait():
    print("HI there from Asyncio WithNoWait ")
    asyncio.sleep(2) # post request -- async task ; but this function will not wait for the async task to complete before its proceeds
    print("Hello, World from Asyncio! WithNoWait")  
    print("Bye from Asyncio WithNoWait")


#greet() # synchronous call
#asyncio.run(greetAsync()) # asynchronous call
#greetWithNoWait() #synchronous call

greetAsync()
# same answer as calling greetAsync with asyncio.run
# throw an error as coroutines cant be called directly without await or asyncio.run
# coroutine object is created but not called/executed


#output:
# HI there!
# Hello, World!     
# Bye
# HI there from Asyncio!
#  (2 sec delay)
#  Hello, World from Asyncio!     
# Bye from Asyncio
# HI there from Asyncio WithNoWait !
# (no delay)    
# Hello, World from Asyncio! WithNoWait
# Bye from Asyncio WithNoWait



def bigComputation():
    #long running computation
    print("Starting big computation...")
    total = 0
    for i in range(10**7):
        total += i
    print("Big computation done.")
    return total

bigComputation()
asyncio.run(greetAsync())

#blocking code -- 
#non blocking code




