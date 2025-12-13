spec("A function to compare two words.").

worker("../../sample_agents/requirement_generators/stub_requirement_manager").
worker("../../sample_agents/requirement_generators/naive_requirement_manager").

!start.


+!count_workers <-
    +nb_workers(0) ;
    for (worker(F)) {
        ?nb_workers(NB) ;
        -nb_workers(NB) ;
        +nb_workers(NB+1)
        }.


+!start <-
    !count_workers ;
    .my_name(N) ;
    .print("Hello from", N) ;
    +answers([]) ;
    for (worker(F)) {
        .spawn(F, URL) ;
        +active_worker(URL)
        }
    .wait(1000) ;
    ?spec(S) ;
    for (active_worker(URL)){
        .send(URL, tell, spec(S))
        }
    .wait(1000) ;
    for (active_worker(URL)){
        .send(URL, achieve, build)
        }.

+reply(R) : answers(L) <-
    -answers(L) ;
    +answers([R|L]).

+answers(L) <-
    .length(L, LEN) ;
    ?nb_workers(N) ;
    if (LEN == N) {
        .print(N, "answers received. Launching arbitration.") ;
        .spawn("arbitrator", URL_ARBITRATOR);
        ?spec(S) ;
        .send(URL_ARBITRATOR, tell, spec(S));
        .send(URL_ARBITRATOR, tell, proposal_list(L)) ;
        .wait(1000) ;
        .send(URL_ARBITRATOR, achieve, arbitrate) ;
        .print("Waiting for arbitrator reply.")
        }
    else {
        .print(LEN, "answers received.")
        }.

+selected(I) : answers(L) <-
    .print("Received a result of an arbitration :", I) ;
    .nth(I, L, R) ;
    .print("Selected requirement list :", R) ;
    .print("End.").



