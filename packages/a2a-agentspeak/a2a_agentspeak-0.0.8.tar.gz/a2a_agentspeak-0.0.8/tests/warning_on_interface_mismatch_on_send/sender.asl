!start.

secret(42).

+!start <-
    .my_name(N) ;
    .print("Hello from", N).

+!do_ping(DEST) <-
    .print("I received a ping request with destination", DEST);
    .send(DEST, achieve, risky);
    .wait(1000);
    .print("Sent.").


+pong <-
    .print("pong received").
