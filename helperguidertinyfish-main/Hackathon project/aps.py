from tinyfish import TinyFish
client = TinyFish()

with client.agent.stream(url="https://example.com",
                         goal="Extract the page title. Return JSON.") as stream:
    for event in stream:
        print(event)