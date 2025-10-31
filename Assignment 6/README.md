Parallelization
We are fanning out and then fan in the nodes. When we are running nodes in parallel you need to use a reducer that can aggregate the updates. The parallel branches run in the same step. We customise the reducer to determine the order in which the nodes should run in.
  -Tweaking
  .Graph Structure and Node Name Changes (Cells 5, 7, 9, 11)
  .LLM and Embedding Model Changes (Cell 13)
  .Example Questions (Cells 17, 20)
