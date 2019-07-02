role(white).
base(s).
init(nothing).
input(mark).
legal(mark).
next(s) :-
    does(white, mark).
q :-
    true(s).
terminal :-
    q.
goal(white, 100) :-
    q.
goal(white, 0) :-
    not(q).