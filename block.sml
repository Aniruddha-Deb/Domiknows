datatype loc = LEFT | RIGHT
datatype move = P1 | P2
exception EmptyException
exception InvalidMoveException

fun right [] = raise EmptyException | right [l] = l | right (l::L) = right L
fun left [] = raise EmptyException | left [l] = l | left (l::L) = l
fun remove _ [] = [] | remove (a,b) ((a,b)::L) = L | remove (a,b) ((b,a)::L) = L 
  | remove a (b::L) = remove a L
fun max a b = (if a > b then a else b)
fun sum [] = 0 | sum ((a,b)::L) = a+b+(sum L)
fun max_pip_sum [] S = S | max_pip_sum ((a,b)::L) S = if (a+b) > S then max_pip_sum L (a+b) else max_pip_sum L S
fun max_double [] D = D | max_double ((a,a)::L) D = if a > D then max_double L a else max_double L D

fun connect (a,b) _ [] pips = ([(a,b)],remove (a,b) pips)
  | connect (a,b) LEFT ((a,c)::L) pips = ((b,a)::(a,c)::L, remove (a,b) pips)
  | connect (b,a) LEFT ((a,c)::L) pips = ((b,a)::(a,c)::L, remove (a,b) pips)
  | connect (a,b) RIGHT [(c,a)] pips = ([(c,a),(a,b)], remove (a,b) pips)
  | connect (b,a) RIGHT [(c,a)] pips = ([(c,a),(a,b)], remove (a,b) pips)
  | connect (a,b) RIGHT (l::L) pips = (l::(connect L (a,b) RIGHT), remove (a,b) pips)
  | connect a b c d = raise InvalidMoveException

fun can_connect (a,b) _ [] = true
  | can_connect (a,b) LEFT ((a,c)::L) = true
  | can_connect (b,a) LEFT ((a,c)::L) = true
  | can_connect (a,b) RIGHT [(c,a)] = true
  | can_connect (b,a) RIGHT [(c,a)] = true
  | can_connect (a,b) RIGHT (l::L) = true
  | can_connect a b c d = false

fun has_move board [] = false
  | has_move [] _ = true
  | has_move board ((a,b)::P) =
let
    val (la,lb) = left board
    val (ra,rb) = right board
in
    la = a orelse la = b orelse rb = a orelse rb = b orelse has_move board P
end

fun p1move board [] = raise InvalidMoveException
  | p1move board ((a,b)::L) = if can_connect (a,b) LEFT board then (connect (a,b) LEFT)
else if can_connect (a,b) RIGHT board then (connect (a,b) RIGHT) 
else p1move board L

fun p2move board pips = p1move board pips (* for now *)

fun play board [] p2pips P2 = (sum p2pips,0)
  | play board p1pips [] P1 = (0,sum p1pips)
  | play board p1pips p2pips P1 = 
if (not (has_move board p1pips)) andalso (not (has_move board p2pips)) then
    (* both are blocked *)
    if (sum p1pips) > (sum p2pips) then (0,sum p1pips) else (sum p2pips, 0)
else if (not (has_move board p1pips)) then
    play board p1pips p2pips P2
else
    let
        val move = (p1move board p1pips)
        val (newboard, newpips) = move board p1pips
    in
        play newboard newpips p2pips P2
    end
  | play board p1pips p2pips P1 = 
if (not (has_move board p1pips)) andalso (not (has_move board p2pips)) then
    (* both are blocked *)
    if (sum p1pips) > (sum p2pips) then (0,sum p1pips) else (sum p2pips, 0)
else if (not (has_move board p2pips)) then
    play board p1pips p2pips P1
else
    let
        val move = (p2move board p2pips)
        val (newboard, newpips) = move board p2pips
    in
        play newboard p1pips newpips P1
    end

fun arbiter p1pips p2pips = 
    if max_pip_sum p1pips 0 > max_pip_sum p2pips 0 then P1 
    else if max_pip_sum p1pips 0 = max_pip_sum p2pips 0 then
        if max_double p1pips -1 > max_double p2pips -1 then P1
        else if max_double p1pips -1 < max_double p2pips -1 then P2
        else P1 (* should ideally coin toss at this point *)
    else P2

fun shuffle rng _ 0 = []
  | shuffle rng l len = 
let
    val rnum = Random.randRange (0,len-1) rng
    val relem = List.nth (l, rnum)
    val rlist = List.take (l, rnum) @ List.drop (l, rnum+1)
in
    [relem] @ (shuffle rng rlist (len-1))
end

fun gen_pips [] = [(0,0)]
  | gen_pips ((a,b)::L) = 
    if a = 6 then ((a,b)::L)
    else if b = 6 then gen_pips ((a+1,0)::(a,b)::L)
    else gen_pips ((a,b+1)::(a,b)::L)

fun match () = 
let
    val seed = Real.floor (Time.toReal(Time.now()) - 1.48e9)
    val rng = Random.rand (seed,seed+5)
    val pips = shuffle rng (gen_pips []) 28
    val p1pips = List.take (pips,7)
    val p2pips = List.take (List.drop (pips,7),7)
in
    play [] p1pips p2pips (arbiter p1pips p2pips)
end