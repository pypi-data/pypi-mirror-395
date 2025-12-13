!start.

sleep_time(2000).

repository_url("http://127.0.0.1:9970/").

mandatory_skill(input,spec,1).
mandatory_skill(action,build,0).


!fill_skill_list.

+!fill_skill_list <-
    +skill_list([]) ;
    for (mandatory_skill(A,B,C)) {
        .print("add a skill in the list") ;
        ?skill_list(L) ;
        -skill_list(L) ;
        +skill_list([mandatory_skill(A,B,C)|L])
    }
    ?skill_list(R) ;
    .print("skill list:", R).



+!start <-
    .my_name(N) ;
    .print("Hello from", N).

+!request : repository_url(A) & skill_list(L) <-
    .send(A,ask,by_skills(L)) ;
    +requested.

+selected(A) : requested <-
    .print("Selecting agent", A) ;
    !build.

+selected(A) : not requested <-
    .print("Warning : unexpected selection received.").

+reply_to(F) <-
    .print("Reply-to:", F).


+!reply_with_failure : reply_to(F) <-
    .my_name(N) ;
    .send(F, tell, failure(N)).


+failed(A) : selected(A) <-
    .print("Received: failure from", A);
    -selected(A) ;
    ?repository_url(R) ;
    .send(R, tell, failure(A)) ;
    .wait(1000) ;
    !request.

+failed(A) : not selected(A) <-
    .print("Warning: Received a failure about", A, "but that agent was not selected").

+failure : selected(A) <-
    .print("received failure message") ;
    -failure ;
    +failed(A).

+spec(S)[source(F)] <-
    +reply_to(F) ;
    .print("Specification received.").

+!build : spec(S) & selected(A) & sleep_time(T) <-
    .print("Received the order to start the job.");
    .send(A, tell, sleep_time(T)) ;
    .send(A, tell, spec(S)) ;
    .print("(spec sent)") ;
    .wait(500);
    .send(A, achieve, build) ;
    .print("(build sent)").

+!build : not spec(_) <-
    .print("Error: Cannot process because of missing spec.").

+!build : not selected(_) & not requested <-
    .print("Sending a selection request.") ;
    !request ;
    .wait(500).

+!build : not selected(_) & requested <-
    .print("Waiting for repository to answer.") ;
    .wait(500) ;
    !build.

+!build : not available_agent(_) <-
    .print("Error: Cannot process because no agent is available.").

+!build : selected(A) & available_agent(B) <-
    .print("Error: Cannot process (mismatch between selected agent", A, "and available agents).").


+reply(L) : reply_to(F)<-
    .print ("Answer received from requirement manager.") ;
    .print("Answer is:", L) ;
    .send(F,tell, result(L)) ;
    .print("Reply sent.").

+reply(L) <-
    .print ("Answer received from requirement manager.") ;
    .print("Answer is:", L) ;
    .print("Don't know who to forward that.").

+reply(H,R) <-
    .print ("Answer received from requirement manager.") ;
    .print("Answer is badly formatted (received two arguments)").

+reply <-
    .print ("Error: Bad answer received from requirement manager.").