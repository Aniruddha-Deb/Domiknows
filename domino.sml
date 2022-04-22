type Domino = int*int
exception NotImplementedException
exception InvalidMoveException

fun eq (a,b) (c,d) = (a = c andalso b = d) orelse (a = d andalso b = c)
fun connectable (a,b) (c,d) = (a = c orelse a = d) orelse (b = c orelse b = d)

fun first (a,b) = a | first (a,b,c,d) = a | first k = raise NotImplementedException
fun second (a,b) = b | second (a,b,c,d) = b | second k = raise NotImplementedException 

datatype Node = EMPTY 
              | SPINNER of (int*(Node * Node * Node * Node))
              | BONE of ((int*Node)*(int*Node))

(*
 * Multiple thoughts here:
 * 1. for fast computation of available moves, maintaining a bitboard would be best. Bitboard
 *    would be a 7x7 grid of bits, where (r,c) gives us the domino. Since (r,c) = (c,r),
 *    we'd be using only half of the bit grid. 
 *    This makes finding computation only easy, but doesn't encode all the
 *    information about the game 
 * Can't think of any other efficient board implementations, other than the graph
 * one. Hardcodes how many spinners we have, because of summation rules? ugh
 *)

datatype Action = DRAW | BLOCK | MOVE of (Domino*(Domino option)) 

type BoardData = {
    n_bones: int,
    curr_player: int,
    hands: (int*int list) list, 
    boneyard: (int*int) list,
    pipset: (int*int) list,
    board: ((int*int)*((int*int) list)) list,
    actions: (Player*Action) list
}

datatype Status = WON of int | BLOCKED

type GameData = {
    rng: Random.rand
    n_players: int, 
    n_rounds_done: int,
    target: int,
    moves: (BoardData -> (Domino*(Domino option)) list
    scores: int list,
    results: Status list,
    current_board: BoardData
}

fun find_domino (SOME (a,b)) (((c,d),e)::B) = if eq (a,b) (c,d) then true else find_domino (a,b) B
  | find_domino NONE [] = true
  | find_domino (SOME (a,b)) [] = false;

fun remove_domino (a,b) hands curr_player =
      (List.take (hands,curr_player))
    @ ((List.filter (fn (c,d) => not (eq (c,d) (a,b))) (List.nth (hands,curr_player)))
    :: (List.drop (hands, curr_player + 1)))

fun add_domino_to_board ((a,b),SOME (c,d)) B =
let
    val unchanged = List.find (fn ((e,f),g) => not ((eq (a,b) (e,f)) orelse (eq (c,d) (e,f)))) B
    val ((tgt_a,tgt_b),tgt_L) = List.nth (List.find (fn ((e,f),g) => eq (c,d) (e,f)) B, 0)
    val src = List.find (fn ((e,f),g) => eq (a,b) (e,f)) B (* src may not exist *)
    fun newboard ((a',b'),L1) ((c',d'),L2) = 
        (* why is simple stuff so hard in SML! Ughhglajsflsd *)
in
    if src = [] then 
        (* add src to board too *)
    else
        ((tgt_a,tgt_b),(a,b)::tgt_L)::(List.nth (src,1))
end
    if (e = c andalso d = f) then (BONE ((e,,BONE())))

signature GAME =
sig
    val validate_move: (Domino*Node) -> Node -> bool
    val do_action: Action -> BoardData -> BoardData
    val play_round: GameData -> GameData
    val play_game: unit -> unit
end

structure BlockGame: GAME =
struct
    
    fun validate_move ((a,b),BONE ((c,n1),(d,n2))) T =
        if ((a == c orelse b == c) andalso n1 == EMPTY) orelse
           ((a == d orelse b == d) andalso n2 == EMPTY) then 
            find_node (BONE ((c,n1),(d,n2))) T 
        else false
      | validate_move (d,n) T = false

    fun do_move (MOVE ((a,b),BONE ((c,n1),(d,n2)))) BD =
    let
        val {
            n_bones = n_bones,
            hands = hands, 
            boneyard = boneyard,
            pipset = pipset,
            board = board,
            actions = actions
        } = BD
    in
        if validate_move ((a,b),BONE ((c,n1),(d,n2))) then 
            (* do the move now *)
            {
                n_bones = (#n_bones BD)+1,
                hands = remove_domino (a,b) (#hands BD) (#curr_player BD)


                (* need player index as well to update hand! Or do we move hand 
                    out of the board_data? *)
            }

    end

end
