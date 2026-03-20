An agentic framework in which every resource is treated as a REST API.

Mildly inspired by https://arxiv.org/html/2601.11672v1, I wanted to see if it was possible to just treat everything as a REST API instead.

Why?

- Because I wanted to try lol
- Agents have a lot of training in using REST APIs
- Natural integration with actual external APIs
- Authentication using keys instead of file permissions seems, again, more natural when integrating with externa APIs

Still a work in progress. I can only guarantee that agents will have identifiers. Maybe.


# TODO:

- [ ] Add event listeners to the conversation itself, so that we can have internal control over the conversation while it's doing the conversation loop. Consider a Conversation object that allows for an event listener to be attached. Otherwise, just wrap the conversation adding into a method and add the listeners to the agent itself.

