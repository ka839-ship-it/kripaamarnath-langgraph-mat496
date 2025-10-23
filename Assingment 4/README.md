State Schema
Schema is the structure and the type of data that the graph will use. The most commonly used is type dict (a type of dictionary). There are different ways to establish schema for your graph like python data classes.

State Reducers
Reducers specify how state updates are performed on specific keys or channels in a schema. The updates automatically overwrite the prior value of the state keys or channels. An thus only update per step can be done. These are were reducers are used, they allow us to specify how to perform state updates. Thiscan lead to incrementation instead of immediate overriding.

Multiple Schemas
Where more control is required in schemas when multiple inputs and outputs don't affect each other that is when this is implemented. In this example it is specified that the nodes interact with each other only in the private state. And the private state is not in the overall state. We can also specify the differnt input and output schemas on our graph.

Trim and Filter Messages
Messages are normally token intensive which won't be  very efficient in terms of time and actual cost. We can thus use a shortvut by defining a message to filter messages based on the measure IDs.  We can use langsmith to trace the modifications done to the filteing of messages. Trimming can be done based on the number of tokens as LLMs might have specific token requirements.

Chatbot with Summarising Messages and Memory
A means to preserve more information of the schema. We add the key summary to get a running summary, if there is a summary it gets added to the messages and if not the message is taken and the model is invoken. We use theMemorySaver check pointer to give us the memory and get the message history. We can create a running summary with all the previous questions and this can happen indfinitely. 

Chatbot with Summarising and External Memory
LangGraph supports  few checkpointers that suppor external databases. Here we have learnt abt SQLite. SQLite is a small, fast and well-known database. We import the SQLite and pass the memory in it. This has been written to a loal database on the machine instead of the notebook itself, so it can exist even after the notebook not being in use.
