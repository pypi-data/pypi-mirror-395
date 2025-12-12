!start.

pos(0).

+!start <-
    .my_name(N) ;
    .print("Hello from", N) ;
    !do_special.

+!do_move : pos(X) <-
    .print("I received a move request.") ;
    -+pos(X+1) ;
    ?pos(Y) ;
    .print("I moved at position", Y).

+!move_by(D) : pos(X) <-
    .print("I received a move_by request.") ;
    -+pos(X+D) ;
    ?pos(Y) ;
    .print("I moved at position", Y).

+!do_special <-
    ?pos(P);
    .print("I received a special request, while I am at position", P);
    .special(RES).
