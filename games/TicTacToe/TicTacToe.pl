role(xplayer).
role(oplayer).

index(1). index(2). index(3).
base(cell(X, Y, b)) :-
    index(X),
    index(Y).
base(cell(X, Y, x)) :-
    index(X),
    index(Y).
base(cell(X, Y, o)) :-
    index(X),
    index(Y).
base(control(P)) :-
    role(P).

input(P, mark(X, Y)) :-
    index(X),
    index(Y),
    role(P).
input(P, noop) :-
    role(P).

init(cell(X, Y, b)) :-
    index(X),
    index(Y).
init(control(xplayer)).

next(cell(M, N, x)) :-
    does(xplayer, mark(M, N)),
    true(cell(M, N, b)).

next(cell(M, N, o)) :-
    does(oplayer, mark(M, N)),
    true(cell(M, N, b)).

next(cell(M, N, x)) :-
    true(cell(M, N, x)).

next(cell(M, N, o)) :-
    true(cell(M, N, o)).

next(cell(M, N, b)) :-
    true(cell(M, N, b)),
    role(R),
    index(J),
    index(K),
    does(R, mark(J, K)),
    J =\= M.

next(cell(M, N, b)) :-
    true(cell(M, N, b)),
    role(R),
    index(J),
    index(K),
    does(R, mark(J, K)),
    K =\= N.

next(control(xplayer)) :-
    true(control(oplayer)).

next(control(oplayer)) :-
    true(control(xplayer)).

row(M, X) :-
    true(cell(M, 1, X)),
    true(cell(M, 2, X)),
    true(cell(M, 3, X)).

column(N, X) :-
    true(cell(1, N, X)),
    true(cell(2, N, X)),
    true(cell(3, N, X)).

diagonal(X) :-
    true(cell(1, 1, X)),
    true(cell(2, 2, X)),
    true(cell(3, 3, X)).

diagonal(X) :-
    true(cell(1, 3, X)),
    true(cell(2, 2, X)),
    true(cell(3, 1, X)).


line(V) :-
    index(M),
    row(M, V).
line(V) :-
    index(N),
    column(N, V).
line(V) :-
    diagonal(V).

open :-
    index(M),
    index(N),
    true(cell(M, N, b)).

legal(P, mark(X, Y)) :-
    true(cell(X, Y, b)),
    role(P),
    true(control(P)).

legal(xplayer, noop) :-
    true(control(oplayer)).

legal(oplayer, noop) :-
    true(control(xplayer)).

goal(xplayer, 100) :-
    line(x).

goal(R, 50) :-
    not(line(x)),
    not(line(o)),
    role(R),
    not(open).

goal(xplayer, 0) :-
    line(o).

goal(oplayer, 100) :-
    line(o).

goal(oplayer, 0) :-
    line(x).

terminal :-
    line(x).

terminal :-
    line(o).

terminal :-
    not(open).