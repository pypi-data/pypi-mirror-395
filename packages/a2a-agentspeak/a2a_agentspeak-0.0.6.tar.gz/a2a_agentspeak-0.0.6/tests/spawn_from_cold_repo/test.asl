!start.

repository_url("http://127.0.0.1:9970/").

mandatory_skill(action,ping,0).

skill_list([]).

# FIX ME : use a for loop instead of recursion
+!fill_skill_list : skill_list(L) & mandatory_skill(A,B,C) <-
    .print("add a skill in the list") ;
    -mandatory_skill(A,B,C) ;
    -skill_list(L) ;
    +skill_list([ mandatory_skill(A,B,C) | L ]) ;
    !fill_skill_list.

+!fill_skill_list : skill_list(L) & not mandatory_skill(_,_,_) <-
    .print("skill list:", L).


+!start <-
    .my_name(N) ;
    .print("Hello from", N) ;
    !fill_skill_list ;
    !request.


+!request : repository_url(A) & skill_list(L) <-
    .print("Sending a request to the repository");
    +requested ;
    .send(A,ask,cold_by_skills(L)).

+selected(cold_agent(A,[])) : requested <-
    .print("Selecting agent", A) ;
    .str_concat("../../sample_agents/",A,F) ;
    .print("Going to spawn",F);
    .spawn(F,RES_URL) ;
    .wait(1000) ;
    .send(RES_URL, achieve, ping) ;
    .print("Finished").

+selected(Other) : requested <-
    .print("Unable to decode selection").

+selected(A) : not requested <-
    .print("Warning : unexpected selection received.").

+pong:
    .print("TEST OK").