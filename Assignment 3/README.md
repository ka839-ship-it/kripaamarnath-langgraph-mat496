Simple Graph
We define the states between the nodes. Each node takes in the state and overrides the value of the graph state. We use edges to connect nodes. We compile our graph and display it.

Studio
It contains requirements, multiple python scripts and dotenv file. We can load this as a project on langraph. Every module has a studio directory.

Chain
This combines the idea of chat messages, chta models and binding tools and executing tools in langraph.

Router
Graph can return a tool call or return a natural language response. This is a simple router. The LLM chooses one of two outputs. A basic router is to either tool call or end.

Agent
 Making one simple modification to the router will lead to a very popular architechture called ReAct. It has the same proceedure we just add something called agent which is an assisting node.

 Agent with memory
 To introduce the idea of memory. Add an additional task but to retain the previos task's answer as a memory to perform the new task, we use persistence to address this.
