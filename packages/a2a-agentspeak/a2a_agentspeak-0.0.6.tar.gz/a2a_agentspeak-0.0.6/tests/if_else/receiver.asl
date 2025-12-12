
!start.

+!start <-
  if (.fail) {
    .print("TEST KO");
    .fail
  }
  else { .print("TEST OK") }.