Parallelization
We are fanning out and then fan in the nodes. When we are running nodes in parallel you need to use a reducer that can aggregate the updates. The parallel branches run in the same step. We customise the reducer to determine the order in which the nodes should run in.
  -Tweaking
  .Graph Structure and Node Name Changes (Cells 5, 7, 9, 11)
  .LLM and Embedding Model Changes (Cell 13)
  .Example Questions (Cells 17, 20)

Sub-graphs
Sub-graphs is an important controlability topic. Sub-graphs allow you to create and manage different states within different parts of your graph. The key concept is to undrstand how the sub-graphs communicate with the entry graphs and that is done by overlapping keys.
  -Tweaking
  .Included the HuggingFaceEmbeddings import in cell 4
  .Replaced generic dummy logs with more varied and descriptive Log entries, including distinct successful and failed scenarios, to better      illustrate the graph's processing capabilities.

Map-Reduce
It is an efficient task decomosition and parallel processing method. It has two phases. The map phase takes some task and breaks it into subtasks and does them in parallel. The reduce is the aggregate results from all the parallalized subtasks and brings them back together.
   -Tweaking
    .Model and Node Name Changes (Cells 5, 7, 8, 9, 10)
    .Included the HuggingFaceEmbeddings import in cell 4
    .Example Topic (Cells 11)

Research Assisstant
We initially need sources for the AI to wok on so we take a couple of arbitary sources using web search tools or we can cutomize them. We useall the methods seen above like parallelization and map reduce to have a conversation between an expert and an analyst. We then compile them into a report. we give instructions for our analysts. We include a human node so that the human's feedback can be taken into account.
    -Tweaking
    .LLM provider was changed from Openai to Groq (Cells 1,3,6,17,21,25)
    .Included the HuggingFaceEmbeddings import instead of the Openai Embeddings 
    .Example Topic and the topic variables were changes(Cells 7,9,23,26,27)
    .Prompts were modified



    
