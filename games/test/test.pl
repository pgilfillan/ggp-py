base(0). base(1).
init(0).
input(0). input(1).
role(player1). role(player2).

legal(R, action1) :-
    role(R),
    true(1).
legal(R, action2) :-
    role(R),
    true(0).

next(0) :-
    true(1).
next(1) :-
    true(0).

goal(R, 100) :-
    role(R).

terminal :-
    true(1).
