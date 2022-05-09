from random import shuffle, randint, sample
from copy import deepcopy
import math
import re
from collections import deque
import matplotlib.pyplot as plt

class Domino:

    def __init__(self, a, b):
        if a < 0 or b < 0:
            raise ValueError("Pips cannot have negative values")
        if a > (1<<32) or b > (1<<32):
            raise ValueError("Pip values cannot be larger than 2^31")
        self._d = (a,b)

    def __str__(self):
        return f"[{self._d[0]}|{self._d[1]}]"

    def __eq__(self,other):
        if self is None and other is None:
            return True
        elif (self is None and other is not None) or (other is None and self is not None):
            return False
        else:
            return self._d == other._d or self._d == other._d[::-1]

    def __getitem__(self,key):
        return self._d[key]

    def __contains__(self, item):
        return item in self._d

    def __repr__(self):
        return self.__str__()

    def __iter__(self):
        return self._d.__iter__()

    def __hash__(self):
        return (max(self._d)<<32) | min(self._d)

    def connections(self,other):
        j = []
        if self._d[0] == other._d[0] or self._d[0] == other._d[1]:
            j.append(self._d[0])
        if self._d[1] == other._d[0] or self._d[1] == other._d[1]:
            j.append(self._d[1])
        return j

    def is_double(self):
        return self._d[0] == self._d[1]

    def flatten(pips):
        return set([i for p in pips for i in p._d])

    def sum(pips):
        return sum(sum(h) for h in pips)

class Board:

    def __init__(self, has_spinner=False):
        self.data = {}
        self.spatial_data = {}
        self.has_spinner = has_spinner
        self.spinner = None

    def get_terminals(self):
        terminals = {}
        for bone in self.data:
            if len(self.data[bone]) < 2:
                terminals.add(bone)
            elif bone == self.spinner and len(self.data[bone]) < 4:
                terminals.add(bone)
        return terminals

    def get_all_connections(self):
        terminals = self.get_terminals()
        conns = {}
        for p in terminals:
            if p.is_double():
                conns.add(p[0])
            else:
                conns.union(set((p[0],p[1])).difference(Domino.flatten(self.data[p])))
        return conns

    def get_connections_for(self, pip):
        if pip == spinner and len(self.data[pip]) < 4:
            conns = (4-len(self.data[pip]))*[pip[0]]
        elif pip.is_double() and len(self.data[pip]) < 2:
            conns = (2-len(self.data[pip]))*[pip[0]]
        else:
            conns = list(set())



    def free_end(self, pip):
        return set((p[0],p[1])).difference(Domino.flatten(self.data[p])).pop()


    #  origin  TT
    #        +───┐
    #     LT │[0]│ RT
    #     LL ├───┤ RR
    #     LB │[1]│ RB
    #        └───┘
    #          BB
    # 
    # rotation is measured anticlockwise w.r.t origin
    # [0] -> number at idx 0 of pip, similarly for [1]

    def connect(self, tgt, src):
        if not src:
            raise ValueError("src cannot be None")
        if src in self.data:
            raise ValueError("src already exists in board")

        if tgt == None and self.data == {}:
            # first move
            self.data[src] = {}
            self.spatial_data[src] = {
                'pos': (-0.5,1),
                'rot': 0 if src.is_double() else 90,
                'conns': {}
            }
        elif tgt not in self.data:
            raise ValueError("tgt does not exist in board")
        elif (len(self.data[tgt]) == 2 and tgt != self.spinner):
            raise ValueError("tgt is already connected to two other pips")
        elif (len(self.data[tgt]) == 4 and tgt == self.spinner):
            raise ValueError("tgt as spinner is already connected to four other pips")
        elif not tgt.connections(src):
            raise ValueError("tgt and src don't have any connections possible")
        else:
            self.data[tgt].add(src)
            self.data[src] = {tgt}

            tgtx = self.spatial_data[tgt]['pos'][0]
            tgty = self.spatial_data[tgt]['pos'][1]
            tgtr = self.spatial_data[tgt]['rot']

            if len(self.data[tgt]) > 2:
                # tgt is a double and a spinner.
                if "TT" not in self.spatial_data[tgt]['conns']:
                    self.spatial_data[tgt]['conns'].add("TT")
                else:
                    self.spatial_data[tgt]['conns'].add("BB")

            elif tgt.is_double():
                if "LL" not in self.spatial_data[tgt]['conns']:
                    # connect to LL
                    self.spatial_data[src] = {
                        'pos': 
                        'rot': 0 if src.is_double() else 90,
                        'conns': {} 
                    }
                    self.spatial_data[tgt]['conns'].add("LL")
                else:

            else:
                # normal pip connect
                tgtx = 
                if tgt[0] == src[0]:
                    if tgtr == 0:
                        self.spatial_data[src] = {
                            'pos': (tgtx+1, tgty),
                            'rot': 180,
                            'conns': {'TT'}
                        }


    def print_board(self):
        # large print v/s small print. Large print only!
        # convert the board to a chain
        if not self.board:
            print("[]")
            return

        # have a curses-like array that you can blit a domino onto at a point
        w = 50
        h = 50
        text_arr = h*[w*[' ']]

        board_arr = []
        curr_pips = deque()
        first_key = list(self.board.keys())[0]
        board_arr.append(first_key)
        curr_pips.append(first_key)
        
        while curr_pips:
            key = curr_pips.popleft()
            key_conns = self.board[key]
            for k in key_conns:
                idx = board_arr.index(key)
                kip = board_arr[board_arr.index(key)]
                if k not in board_arr:
                    curr_pips.append(k)
                    if idx == 0:
                        board_arr.insert(0, k)
                    else:
                        board_arr.append(k)

        # if there's a spinner, construct a top-down array as well.
        while curr_pips:


        print(f"BOARD: ", end="")
        prev_inv = False
        for i in range(len(board_arr)-1):
            c,n = board_arr[i],board_arr[i+1]
            if c[1] == n[0] or c[1] == n[1]:
                print(board_arr[i],end="")
                prev_inv = False
            else:
                print(f"[{board_arr[i][1]}|{board_arr[i][0]}]", end="")
                prev_inv = True

        if len(board_arr) == 1:
            print(board_arr[0])
        else:
            if (not prev_inv and board_arr[-1][0] == board_arr[-2][1]) or \
               (prev_inv and board_arr[-1][0] == board_arr[-2][0]):
                print(board_arr[-1])
            else:
                print(f"[{board_arr[-1][1]}|{board_arr[-1][0]}]")


class Board:

    def __init__(self, pipset, hands, boneyard):
        self.curr_player = -1
        self.n_players = len(hands)
        self.hands = hands
        self.boneyard = boneyard
        self.pipset = pipset
        self.spinner = None
        self.board = {}
        self.actions = []

    def deal_board(n_players, n_pips, pipset_size):
        if (n_pips*n_players > (pipset_size+2)*(pipset_size+1)/2):
            raise Exception("Too few pips to deal")
        pip_cpy = [Domino(i,j) for i in range(pipset_size+1) for j in range(i+1)]
        pips = tuple(pip_cpy)
        shuffle(pip_cpy)
        hands = []
        for i in range(n_players):
            hands.append(pip_cpy[i*n_pips:(i+1)*n_pips])
        boneyard = pip_cpy[n_players*n_pips:]

        return Board(pips, hands, boneyard)

    def connect_domino(self, tgt, src):
        if tgt == None and self.board == {}:
            # first move
            self.board[src] = []
        else:
            if tgt in self.board:
                self.board[tgt].append(src)
                if src in self.board:
                    self.board[src].append(tgt)
                else:
                    self.board[src] = [tgt]
            else:
                raise Exception("tgt does not exist in board")

    # works only for hidden boards
    def curr_player_is_us(self):
        return isinstance(self.hands[self.curr_player],list)

    def get_connections(self):
        connections = []
        for bone in self.board:
            flat = Domino.flatten(self.board[bone])
            if len(self.board[bone]) < 2:
                if bone.is_double():
                    connections.append(bone[0])
                else:
                    connections += [a for a in bone if a not in flat]
            elif bone == self.spinner and len(self.board[bone]) < 4:
                # implicitly assuming spinners are doubles here
                connections.append(bone[0])
        return connections;

    def get_terminals(self):
        return [bone for bone in self.board if (len(self.board[bone]) < 2) or (bone == self.spinner and len(self.board[bone]) < 4)]

    def hidden_copy(self, player_idx):
        hands = []
        for i in range(len(self.hands)):
            if i == player_idx:
                hands.append(self.hands[i])
            else:
                hands.append(len(self.hands[i]))
        b = Board(self.pipset, hands, None)
        b.curr_player = self.curr_player
        b.boneyard = len(self.boneyard)
        b.spinner = self.spinner
        b.board = deepcopy(self.board)
        b.actions = self.actions.copy()

        # any changes to the hidden board won't affect the game board now
        return b

    def copy(self):
        return deepcopy(self)

    def visible_hands(self):
        hands = []
        for h in self.hands:
            if isinstance(h,list):
                hands += h
        return hands

    def visible_pips(self):
        vpips = list(self.board.keys())
        vpips += self.visible_hands()

        if isinstance(self.boneyard, list):
            vpips += self.boneyard

        return vpips

    # Can't connect 
    def do_move(self, action, move):
        if move is None:
            return
        else:
            board.connect_domino(move[0],move[1])
            board.hands[board.curr_player].remove(move[1])
        board.curr_player = (board.curr_player+1)%board.n_players
        board.actions.append(action)

    def undo_move(self):
        if not self.actions:
            raise Exception("No move to be undone!")
        self.curr_player -= 1
        self.curr_player %= len(self.hands)
        lastmove = self.actions[-1]
        if lastmove == "BLOCK":
            pass
        else:
            (tgt,src) = lastmove
            self.board[tgt].remove(src)
            self.board.pop(src)
            if self.curr_player_is_us():
                self.hands[self.curr_player].append(src)
            else:
                self.hands[self.curr_player] += 1

        self.actions.pop()

    def print_board(self):
        # convert the board to a chain
        if not self.board:
            print("[]")
            return
        board_arr = []
        curr_pips = deque()
        first_key = list(self.board.keys())[0]
        board_arr.append(first_key)
        curr_pips.append(first_key)
        while curr_pips:
            key = curr_pips.popleft()
            key_conns = self.board[key]
            for k in key_conns:
                idx = board_arr.index(key)
                kip = board_arr[board_arr.index(key)]
                if k not in board_arr:
                    curr_pips.append(k)
                    if idx == 0:
                        board_arr.insert(0, k)
                    else:
                        board_arr.append(k)

        print(f"BOARD: ", end="")
        prev_inv = False
        for i in range(len(board_arr)-1):
            c,n = board_arr[i],board_arr[i+1]
            if c[1] == n[0] or c[1] == n[1]:
                print(board_arr[i],end="")
                prev_inv = False
            else:
                print(f"[{board_arr[i][1]}|{board_arr[i][0]}]", end="")
                prev_inv = True

        if len(board_arr) == 1:
            print(board_arr[0])
        else:
            if (not prev_inv and board_arr[-1][0] == board_arr[-2][1]) or \
               (prev_inv and board_arr[-1][0] == board_arr[-2][0]):
                print(board_arr[-1])
            else:
                print(f"[{board_arr[-1][1]}|{board_arr[-1][0]}]")

    def debug_board(self):
        print(self.__dict__)


def locate_max(a):
    largest = max(a)
    return largest, [index for index, element in enumerate(a) 
                      if largest == element]

def locate_min(a):
    smallest = min(a)
    return smallest, [index for index, element in enumerate(a) 
                      if smallest == element]

def hand_sum(hand):
    return sum(sum(h) for h in hand)

def hand_max_sum(hand):
    mpip = max(x,key=lambda y: y[0]+y[1])

class BlockGame:

    def __init__(self, n_players, n_pips, pipset_size, max_score, player_moves):
        self.n_players = n_players;
        self.n_pips = n_pips;
        self.pipset_size = pipset_size;
        self.max_score = max_score;

        self.game_results = [] # 0 for both blocked, int for winner 
        self.scores = [0 for i in range(n_players)]
        self.board = None
        self.prev_boards = []
        self.player_moves = player_moves

    def arbiter(self, board):
        if not self.game_results or self.game_results[-1] == 0:
            (m,idxs) = locate_max(list(map(lambda x: sum(max(x,key=lambda y: y[0]+y[1])), board.hands)))
            print((m,idxs))
            if len(idxs) > 1:
                # tiebreak on highest double
                print(list(map(lambda x: max(x,key=lambda y: y[0] if y[0]==y[1] else -1), board.hands)))
                (m,idxs) = locate_max(list(map(lambda z: z[0],list(map(lambda x: max(x,key=lambda y: y[0] if y[0]==y[1] else -1), board.hands)))))
                if len(idxs) == len(board.hands) or len(idxs) == 0:
                    # none of the players have a double, and all have highest tile sum same.
                    # EXERCISE: find probability of this happening.
                    # In this case, randomly arbiter first player
                    return randint(0,len(board.hands)-1)
                else:
                    return idxs[0]
            else:
                return idxs[0]
        elif self.game_results[-1] > 0:
            return self.game_results[-1]-1

    def matches(connections, pips):
        if not connections:
            return True
        fltpips = Domino.flatten(pips)
        for c in connections:
            if c in fltpips:
                return True
        return False

    def validate_move(board, tgt, src):
        if (not tgt and board.board == {}):
            return True
        intersecn = tgt.connections(src)
        if len(intersecn) < 1:
            return False
        return (tgt in board.board \
               and len(board.board[tgt]) < 2 and (tgt.is_double() or intersecn[0] not in Domino.flatten(board.board[tgt])))

    def valid_moves_from_pips(board, pips):
        terminals = board.get_terminals()
        val_moves = []
        for t in terminals:
            for p in pips:
                if BlockGame.validate_move(board, t, p):
                    val_moves.append((t,p))
        return val_moves        

    def valid_moves(board):
        return BlockGame.valid_moves_from_pips(board,board.hands[board.curr_player])

    def valid_pips(board, pips):
        terminals = board.get_terminals()
        val_pips = []
        for p in pips:
            for t in terminals:
                if BlockGame.validate_move(board, t, p):
                    val_pips.append(p)
                    break
        return val_pips

    def blocked(self, board):
        return (len(self.board.actions) > self.n_players and all(c == "BLOCK" for c in self.board.actions[-self.n_players:]))

    def play_board(self):

        self.board = Board._deal_board(self.n_players, self.n_pips, self.pipset_size)
        self.board.curr_player = self.arbiter(self.board)

        while not (min(map(lambda x: len(x),self.board.hands)) == 0 or self.blocked(self.board)):
            self.board.print_board()
            curr_player = self.board.curr_player
            connections = self.board.get_connections()
            if BlockGame.matches(connections, self.board.hands[curr_player]):
                (tgt, src) = self.player_moves[curr_player](self.board.hidden_copy(curr_player))
                if BlockGame.validate_move(self.board, tgt, src):
                    board._do_move((tgt,src),(tgt,src))
                else:
                    print((tgt,src))
                    self.board._debug_board()
                    raise Exception("Invalid Move")
            else:
                print(f"Player {curr_player+1} Blocked!")
                board._do_move("BLOCK",None)

        # What do we do if two (or more) people tie on minimum scores? 
        # A: split the rest of the sum between the two
        (min_score, ms_idxs) = locate_min(list(map(lambda x: hand_sum(x), self.board.hands)))
        rem_sum = 0
        for i in range(self.n_players):
            if i not in ms_idxs:
                rem_sum += hand_sum(self.board.hands[i])

        return (rem_sum, ms_idxs)

    def play_game(self):
        while (max(self.scores) < self.max_score):
            (score, idxs) = self.play_board()
            for i in idxs:
                self.scores[i] += (score//len(idxs))

            for i, score in enumerate(self.scores):
                print(f"Player {i+1}: {score}")
                i += 1

            if self.blocked(self.board):
                self.game_results.append(0)
            else:
                self.game_results.append(idxs[0]+1)
            self.prev_boards.append(self.board)

def user_move(board):
    print("Accepting user move")
    print(board.hands[board.curr_player])
    if (board.board == {}):
        in_str = input("<src>: ")
        if (in_str == "d"):
            board._debug_board()
            return user_move(board)
        captures = re.match("\(([0-9]),([0-9])\)", in_str)
        D = tuple(int(i) for i in captures.groups())
        return (None, Domino(D[0],D[1]))
    else:
        in_str = input("<tgt> <src>: ")
        if (in_str == "d"):
            board._debug_board()
            return user_move(board)
        captures = re.match("\(([0-9]),([0-9])\)\\s*\(([0-9]),([0-9])\)",in_str)
        vals = [int(i) for i in captures.groups()]
        tgt = Domino(vals[0], vals[1])
        src = Domino(vals[2], vals[3])
        print(tgt, src)
        if not BlockGame.validate_move(board, tgt, src):
            print("Invalid move.")
            return user_move(board)
        return (tgt, src)

def pick(A,n):
    L = []
    for p in A:
        if n in p:
            L.append(p)
    return L

def computer_move_adhoc(board):
    #print("Thinking...")
    conns = board.get_connections()
    terms = board.get_terminals()
    if not conns:
        return (None, board.hands[board.curr_player][0])
    for c in conns:
        for p in board.hands[board.curr_player]:
            if (p[0] == c or p[1] == c):
                for k in pick(terms, c):
                    if BlockGame.validate_move(board, k, p):
                        return (k,p)
    raise Exception("No move available")

def computer_move_greedy(board):
    #print("Thinking...")
    conns = board.get_connections()
    terms = board.get_terminals()
    if not conns:
        return (None, board.hands[board.curr_player][0])
    moveset = []
    for c in conns:
        for p in board.hands[board.curr_player]:
            if (p[0] == c or p[1] == c):
                for k in pick(terms, c):
                    if BlockGame.validate_move(board, k, p):
                        moveset.append((k,p))
    if moveset:
        return max(moveset, key=lambda x: sum(x[1]))
    else:
        raise Exception("No move available")

def computer_move_block(board):
    conns = board.get_connections()
    terms = board.get_terminals()
    if not conns:
        return (None, board.hands[board.curr_player][0])
    moveset = []
    for c in conns:
        for p in board.hands[board.curr_player]:
            if (p[0] == c or p[1] == c):
                for k in pick(terms, c):
                    if BlockGame.validate_move(board, k, p):
                        moveset.append((k,p))

    if (len(conns) == 2):
        for move in moveset:
            d = move[1]
            if (conns[0] == d[1] and d[0] == conns[1]) or (conns[1] == d[0] and d[1] == conns[0]):
                return move
    if moveset:
        return max(moveset, key=lambda x: sum(x[1]))
    else:
        raise Exception("No move available")

#
# TODO heuristic for search tree: 
# a simple first level heuristic could be number of pips in hand
# another is degrees of freedom: the number of different pips one can connect to
# from their hand
#
# TODO inference: use the block information to more accurately predict the 
# opponent's pipset
# eg if they've been blocked at a 3 and a 5, they have no pips with a 3 or 5 in 
# them. This reduces the candidate pips they can play from.

def EMM_eval_pos(board,ilvl,alpha,beta):
    #for i in range(ilvl):
    #    print("  ",end="")
    #board.print_board()

    visible_pips = board.visible_pips()
    our_pips = board.visible_hands()
    n_visible_pips = len(visible_pips)
    invis_pips = Domino.exclusion(board.pipset,visible_pips)
    n_invis_pips = len(invis_pips)
    n_opp_pips = n_invis_pips - board.boneyard

    if (n_opp_pips <= 0):
        return -Domino.sum(our_pips)
    if (len(our_pips) <= 0):
        return Domino.sum(invis_pips)*n_opp_pips/n_invis_pips

    if len(board.actions) >= 2 and board.actions[-1] == "BLOCK" and board.actions[-2] == "BLOCK":
        # terminal node!
        # Expected value of sum of opponent's pips is Sum of all unknown
        # pips * (no. of opp pips)/(no. of total unknown pips)
        #
        # TODO calc standard deviation: assume S is normally distributed, so 
        # pick win with a safer error margin (P > 80%, say?)
        S = Domino.sum(invis_pips)
        if S*n_opp_pips*0.5/n_invis_pips > Domino.sum(our_pips):
            # we win
            return S*n_opp_pips/n_invis_pips
        else:
            return -Domino.sum(our_pips)

    if (board.curr_player_is_us()):
        # get the valid moves and pick the one with the most (expected) gain
        valid_moves = BlockGame.valid_moves(board)
        if not valid_moves:
            # blocked!
            board._do_move("BLOCK",None)
            val = EMM_eval_pos(board,ilvl+1,alpha,beta)
            board.undo_move()
            return val
        else:
            val = -math.inf
            for move in valid_moves:
                board._do_move(move,move)

                val = max(val,EMM_eval_pos(board,ilvl+1,alpha,beta))
                board.undo_move()
                if val >= beta:
                    break
                alpha = max(alpha,val)


            return val
    else:
        # random move: get expectation of this node
        # the dominoes possible are the ones we don't have
        valid_moves = BlockGame.valid_moves_from_pips(board,invis_pips)
        valid_pips = BlockGame.valid_pips(board,invis_pips)
        terminals = board.get_terminals()

        n = n_invis_pips
        vp = len(valid_pips)
        r = n_opp_pips
        vm = len(valid_moves)

        if vm == 0:
            # unconditionally blocked. 
            board._do_move("BLOCK",None)
            val = EMM_eval_pos(board,ilvl+1,alpha,beta)
            board.undo_move()
            return val

        # Assume each valid move is equiprobable.
        # Probability of block is C(n-vp,r)/C(n,r)
        # (v = no. valid pips, n = no. invisible pips, r = no. pips in opp hand)
        # Hence, probability of each move is (1 - C(n-vp,r)/C(n,r))/vm
        # There's a more convincing derivation with the law of total probability
        # in my notes. Too lengthy (and math-y) to type here.
        #
        # note that vm need not neccessarily be equal to vp (a single pip may 
        # have more than one move available to it)
        P_block = math.comb(n-vp,r)/math.comb(n,r)
        val_accum = 0
        for move in valid_moves:
            board._do_move(move,move)

            val_accum += EMM_eval_pos(board,ilvl+1,alpha,beta)

            board.undo_move()
        val_accum *= ((1-P_block)/vm)

        # opp block calc
        board.actions.append("BLOCK")
        board.curr_player = (board.curr_player+1)%board.n_players
        val_accum += EMM_eval_pos(board,ilvl+1,alpha,beta)*P_block
        board.undo_move()
        
        return val_accum

def computer_move_EMM(board):
    if len(board.hands) != 2:
        raise Exception("EMM is only two-player for now")
    # construct the game tree here
    if len(board.board) < 4:
        return computer_move_greedy(board)
    try:
        valid_moves = BlockGame.valid_moves(board)
        val = -math.inf
        i = 0
        idx = -1
        for move in valid_moves:
            board._do_move(move,move)

            nval = EMM_eval_pos(board,1,math.inf,-math.inf)
            if nval > val:
                val = nval
                idx = i
            
            board.undo_move()
            i += 1

        return valid_moves[idx]
    except ValueError:
        board._debug_board()

def get_valid_pips(invis_pips, blocked_nos):
    ret_pips = []
    for pip in invis_pips:
        if not (pip[0] in blocked_nos or pip[1] in blocked_nos):
            ret_pips.append(pip)
    return ret_pips

# Two ways to do this: 
# 1. MAX^n strategy for multiple players [https://www.aaai.org/Papers/AAAI/1986/AAAI86-025.pdf]
# 2. simple minmax with alpha-beta
# I'll start off with 2, see if it's fast and simple, then try implementing 1
# (with the improvements described in it)
def solve_PI(board, player):
    if board.n_players != 2:
        raise Exception("PI solving works only for two players now")

    if (n_opp_pips <= 0):
        return -Domino.sum(board.hands[player])
    if (len(our_pips) <= 0):
        return Domino.sum(board.hands[(player+1)%2]) # 2 player so no worries

    if len(board.actions) >= 2 and board.actions[-1] == "BLOCK" and board.actions[-2] == "BLOCK":
        # terminal node!
        our_sum = Domino.sum(board.hands[player])
        opp_sum = Domino.sum(board.hands[(player+1)%2])
        if our_sum < opp_sum: 
            # we win
            return opp_sum
        else:
            return -our_sum

    valid_moves = BlockGame.valid_moves(board)

    if board.curr_player == player:
        val = -math.inf
        bmove = None
        for move in valid_moves:
            board._do_move(move,move)
            nval = solve_PI(board, player)
            board.undo_move()
            if nval > val:
                val = nval
                bmove = move

        if not bmove:
            # blocked
            board._do_move("BLOCK", None)
            nval = solve_PI(board, player)
            board.undo_move()
            val = nval
            bmove = "BLOCK"
        else:
    else:
        val = math.inf
        bmove = None
        for move in valid_moves:
            board._do_move(move,move)
            nval = solve_PI(board, player)
            board.undo_move()
            if nval < val:
                val, bmove = nval, move

        if not bmove:
            # blocked
            board._do_move("BLOCK", None)
            nval = solve_PI(board, player)
            board.undo_move()
            val = nval
            bmove = "BLOCK"

    return val

def computer_move_PIMC(board):
    # get candidate pipset(s), given board information
    move_stack = []
    unavailable_conns = [[] for i in range(board.n_players)]
    head_player = (board.curr_player-1)%board.n_players
    while board.actions:
        last_action = board.actions[-1]
        move_stack.push(last_action)
        if last_action == "BLOCK":
            conns = board.get_connections()
            unavailable_conns[head_player] += conns
        head_player = (head_player-1)%board.n_players

    while move_stack:
        move = move_stack.pop()
        if move == "BLOCK":
            board._do_move("BLOCK",None)
        else:
            board._do_move(move,move)

    # do PIMC for 200 samples:
    moves = []
    for i in range(200):
        board_cpy = board.copy()
        visible_pips = board_cpy.visible_pips()
        invis_pips = Domino.exclusion(board_cpy.pipset,visible_pips)
        for i in range(board_cpy.n_players):
            if not isinstance(board_cpy.hands[i],list):
                # get invis_pips with pips of a particular color removed
                pips_to_choose = get_valid_pips(invis_pips, unavailable_conns[i])
                board_cpy.hands[i] = sample(pips_to_choose, board_cpy.hands[i])
                invis_pips = Domino.exclusion(invis_pips, board_cpy.hands[i])
        moves.append(solve_PI(board_cpy, board.curr_player))

    # return most frequent move
    # TODO tiebreaks: go greedy if a tie happens?
    return max(moves, key=moves.count)

if __name__ == "__main__":
    gscores = []
    nwins = 0
    for i in range(40):
        game = BlockGame(2, 7, 6, 120, [computer_move_EMM, computer_move_block])
        game.play_game()
        if game.scores[0] > game.scores[1]:
            nwins += 1
        gscores.append(game.scores)

    print(nwins)
    plt.plot(gscores)
    plt.show()
