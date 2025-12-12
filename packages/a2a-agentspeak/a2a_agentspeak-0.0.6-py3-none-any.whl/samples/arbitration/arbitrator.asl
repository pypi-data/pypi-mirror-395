
!start.

+!start <-
    .my_name(N) ;
    .print("Hello from", N).

+spec(S) <-
    .print("Spec received").

+proposal_list(L)<-
    .print("List of proposals received").

+!arbitrate[source(TO)] : spec(S) & proposal_list(L) <-
    .send(TO, tell, selected(1)).
