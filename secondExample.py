import asyncio

def greet():
    print("HI there!")
    print("Hello, World!")  
    print("Bye")

async def greetAsync(name):# creating an async function also called coroutine
    print(f"HI {name}")
    await asyncio.sleep(2) 
    print(f"Bye {name}")


async def sendEmailAsync(name,emailId):# creating an async function also called coroutine
    print(f"HI {name} Email is going to be sent to {emailId}")
    await asyncio.sleep(5) # send email
    print(f"Bye {name} Email sent to {emailId}")


async def main():
    print("Starting main function")
    # running coroutines concurrently -- gather 
    await asyncio.gather(
            greetAsync("User1"), 
            sendEmailAsync("User1","user1@gmaul.com")
                           )
                           
    print("Main function done")

asyncio.run(main())
                           
