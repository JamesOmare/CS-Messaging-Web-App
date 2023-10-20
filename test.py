agents = ["Agent 1", "Agent 2", "Agent 3", "Agent 4", "Agent 5"]
agent_index = 0

def assign_message_to_agent(message):
    global agent_index
    agent = agents[agent_index]
    agent_index = (agent_index + 1) % len(agents)  # Circular rotation
    # Here, you would actually assign the message to the selected agent
    print(f"Assigning message '{message}' to {agent}")

# Simulate the arrival of 20 messages
messages = [f"Message {i + 1}" for i in range(20)]

for message in messages:
    assign_message_to_agent(message)