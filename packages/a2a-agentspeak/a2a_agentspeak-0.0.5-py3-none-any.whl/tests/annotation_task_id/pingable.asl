!start.

+!start <-
    .my_name(N) ;
    .print("Hello from", N).

+!ping[task_id(ID), source(S)] : the_task(CURRENT_ID) & not (CURRENT_ID == ID) <-
    .print("Warning: Received a ping from task", I, "from", S, "Cannot handle this task because already handling task", CURRENT_ID).


+!ping[task_id(ID), source(S)] <-
    .print("Received a ping from task", I, "from", S) ;
    +the_task(ID);
    .send(S, tell, pong).

