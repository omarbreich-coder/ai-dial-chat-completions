import asyncio

from task.clients.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    # TODO:
    # 1.1. Create DialClient
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    dial_client = DialClient(deployment_name="gpt-4o")
    # 1.2. Create CustomDialClient
    customDialClient = DialClient(deployment_name="gpt-4o")

    # 2. Create Conversation object
    conversation = Conversation()

    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    print("Enter a system prompt or click 'enter' to continue")
    system_prompt = input(">").strip()
    if system_prompt:
        conversation.add_message(Message(Role.SYSTEM, system_prompt))
        print("System prompt added successfully")
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(
            f"No system prompt was provided so will fallback to the default prompt{DEFAULT_SYSTEM_PROMPT}"
        )

    # 4. Use infinite cycle (while True) and get yser message from console
    while True:
        user_input = input("Enter a message, otherwise type 'exit' to close the app\n")
        # 5. If user message is `exit` then stop the loop
        if user_input.lower() != "exit":
            # 6. Add user message to conversation history (role 'user')
            conversation.add_message(Message(Role.USER, user_input))
            # 7. If `stream` param is true -> call DialClient#stream_completion()
            #    else -> call DialClient#get_completion()
            if stream:
                ai_response = await customDialClient.stream_completion(
                    conversation.get_messages()
                )
            else:
                ai_response = customDialClient.get_completion(
                    conversation.get_messages()
                )
            conversation.add_message(ai_response)
            print("Ai response")
            print(ai_response)

        # 8. Add generated message to history

        # 9. Test it with DialClient and CustomDialClient
        # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response
        else:
            print("Exiting the app")
            break


asyncio.run(start(True))
