component(antenna).
component(transponder).
component(radar).
component(spectrometer).
component(imu).
component(camera).
component(cpu).
component(ram).

safe_with(radar,cpu).
safe_with(cpu,radar).
safe_with(radar,imu).
safe_with(imu,radar).
safe_with(imu,camera).
safe_with(camera,imu).
safe_with(imu,cpu).
safe_with(cpu,imu).
safe_with(imu,ram).
safe_with(ram,imu).
safe_with(ram,cpu).
safe_with(cpu,ram).
safe_with(ram,camera).
safe_with(camera,ram).
safe_with(camera,transponder).
safe_with(transponder,camera).
safe_with(camera,cpu).
safe_with(cpu,camera).
safe_with(cpu,spectrometer).
safe_with(spectrometer,cpu).
safe_with(cpu,antenna).
safe_with(antenna,cpu).
safe_with(antenna,spectrometer).
safe_with(spectrometer,antenna).
safe_with(antenna,transponder).
safe_with(transponder,antenna).
safe_with(transponder,spectrometer).
safe_with(spectrometer,transponder).

% Exercise 1: Predicate to check if a list of components is safe
safe_list([]).
safe_list([Component | Rest]) :- safe_list(Component, Rest).

% Predicate to check if a component is safe with all other components in the list
safe_list(_, []). % Base case - empty list means no other components to compare
safe_list(Component, [Other | Rest]) :-
    safe_with(Component, Other), % Check if Component is safe with Other
    safe_list(Component, Rest). % Recursively check if Component is safe with all other components in the list


% Exercise 2: Predicate to check if a design is safe
part(C) :- component(C).
shield(L) :- is_list(L), L = [H|_], part(H). % Predicate to check if L is a valid shield


safe_design([]). % Base case - empty list is always safe
safe_design([part(C) | Ds]) :- part(C), safe_with_all_shielded(C, Ds). % If the first element in the list is a valid part, check if it is safe with all other components
safe_design([shield(L) | Ds]) :- safe_design(Ds), safe_design(L).


safe_with_all_shielded(_, []).
safe_with_all_shielded(C, [part(D) | Ds]) :- safe_with(C, D), safe_with_all_shielded(C, Ds). % Check if component C is safe with part D and recursively check if C is safe with all other parts in the list
safe_with_all_shielded(C, [shield(D) | Ds]) :- safe_design(D), safe_with_all_shielded(C, Ds). % Check if component C is safe with all components in the shield D and recursively check if C is safe with all other shields in the list


% Exercise 3: Predicate to count the number of shields in a list
count_shields([], 0).
count_shields([shield(A) | T], N) :- count_shields(T, N1),count_shields(A, N2), N is N1 + N2 + 1 .
count_shields([_ | T], N) :- count_shields(T, N).


% Exercise 4
split_list([], [], []).
split_list([X|Xs], [X|L], R) :- split_list(Xs, L, R).
split_list([X|Xs], L, [X|R]) :- split_list(Xs, L, R).


design_uses(Design, Components) :-
    is_design(Design), % Design must be a valid design
    split_list(Design, Parts, Shields), % Split the design into two halves: parts and shields.
    flatten_list(Parts, FlatParts), % Flatten the parts into a single list.
    permutation(Components, FlatParts), % Check if Components is a permutation of the flattened parts.
    verify_shields(Shields, Components). % Check if the remaining components can be used to build the shields.

% Checks if a given design follows the required format.
is_design([]).
is_design([part(_)|Design]) :- is_design(Design).
is_design([shield([part(_)|InnerDesign])|Design]) :- is_design(InnerDesign), is_design(Design).

% Flattens a nested list into a single list.
flatten_list([], []).
flatten_list([part(C)|Parts], [C|FlatParts]) :- flatten_list(Parts, FlatParts).
flatten_list([shield(InnerDesign)|Parts], FlatParts) :-
    flatten_list(InnerDesign, InnerFlat),
    flatten_list(Parts, OtherFlat),
    append(InnerFlat, OtherFlat, FlatParts).

% Checks if the given components can be used to build the shields.
verify_shields([], _).
verify_shields([shield(InnerDesign)|Shields], Components) :-
    flatten_list(InnerDesign, InnerFlat),
    permutation(InnerFlat, Components),
    subtract(Components, InnerFlat, Remaining), % Subtract the used components from the remaining components.
    verify_shields(Shields, Remaining).


