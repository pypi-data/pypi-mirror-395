!start.

secret(42).
pingable_agent_address("http://127.0.0.1:9998").

+!start <-
    .my_name(N) ;
    .print("Hello from", N) ;
    ?pingable_agent_address(A) ;
    !do_ping(A).

+!do_ping(DEST) <-
    .print("I received a ping request with destination", DEST);
    .send_cb(DEST, achieve, ping, ack);
    .print("Sent.").

+pong <-
    .print("pong received").

+!ack(M) <- .print("Synchronous ack received (with content:",M,")").