alice_url("http://localhost:8001").
test_value(50).

!start.

+!start : alice_url(A) & test_value(V)<-
    .print("Trying",  V);
    .send_int_cb(A,tell, V, hint).

+!hint("Go higher") : test_value(V) <-
    .print("Received ++ .") ;
    -+test_value(V+1);
    !start.

+!hint("Go lower") : test_value(V) <-
    .print("Received -- .") ;
    -+test_value(V-1);
    !start.

+!hint(X) <-
    .starts_with(X,"correct", RES) ;
    if (RES){ .print("Complete :-)") }
    else { .print("Received other:", X) }.