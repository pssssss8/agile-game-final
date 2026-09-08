import sys
import math
import random
import pygame
import array

# Safe core initialization with audio subsystem fault isolation 
pygame.init()
HAS_AUDIO = True
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=1)
except Exception:
    HAS_AUDIO = False

# ==========================================
# PREMIUM DESIGN PALETTE & DIMENSIONS
# ==========================================
WIDTH, HEIGHT = 750, 920
BG_COLOR = (15, 23, 42)          # Slate 900 (Deep modern midnight)
BOARD_BG = (30, 41, 59)          # Slate 800 (Rich board plate contrast)
GRID_COLOR = (71, 85, 105)       # Slate 600 (Clean structural lines)
HIGHLIGHT_COLOR = (34, 197, 94)  # Emerald 500 neon glow
TEXT_COLOR = (241, 245, 249)     # Slate 100 clean text
TIGER_COLOR = (239, 68, 68)      # Red 500 (Vibrant crimson velvet)
GOAT_COLOR = (14, 165, 233)      # Sky 500 (Electric royal sapphire)
PANEL_BG = (15, 23, 42)          # Bottom panel dark glass mesh

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aadu Puli Aattam - Neo Court Edition")

# Scale high-fidelity typography
font_sm = pygame.font.SysFont("Segoe UI", 16)
font_md = pygame.font.SysFont("Segoe UI", 20, bold=True)
font_lg = pygame.font.SysFont("Segoe UI", 26, bold=True)

# ==========================================
# PROCEDURAL AUDIO SYNTHESIZER
# ==========================================
def generate_synth_sound(frequency, duration, wave_type='sine'):
    if not HAS_AUDIO:
        return None
    try:
        sample_rate = 22050
        num_samples = int(sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        for i in range(num_samples):
            t = float(i) / sample_rate
            envelope = math.exp(-4.0 * t / duration)
            if wave_type == 'sine':
                value = math.sin(2.0 * math.pi * frequency * t)
            elif wave_type == 'square':
                value = 1.0 if math.sin(2.0 * math.pi * frequency * t) >= 0 else -1.0
            elif wave_type == 'saw':
                value = 2.0 * (t * frequency - math.floor(0.5 + t * frequency))
            buf[i] = int(value * envelope * 16383)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None

SOUND_PLACE = generate_synth_sound(523.25, 0.12, 'sine')    
SOUND_MOVE = generate_synth_sound(392.00, 0.15, 'sine')     
SOUND_CAPTURE = generate_synth_sound(100.00, 0.40, 'square') 
SOUND_WIN = generate_synth_sound(587.33, 0.60, 'saw')        

def play_sound(sound_obj):
    if HAS_AUDIO and sound_obj is not None:
        try: sound_obj.play()
        except Exception: pass

# ==========================================
# TRADITIONAL 23-NODE MOVEMENT GRAPH
# ==========================================
NODES = {
    0: (375, 80),
    1: (375, 180), 2: (270, 180), 3: (480, 180),
    4: (375, 300), 5: (160, 300), 6: (590, 300),
    7: (375, 450), 8: (50, 450),  9: (700, 450),
    10: (375, 620), 11: (160, 620), 12: (590, 620),
    13: (270, 620), 14: (480, 620),
    15: (50, 620),  16: (700, 620),
    17: (50, 300),  18: (700, 300),
    19: (212, 450), 20: (538, 450),
    21: (265, 450), 22: (485, 450)
}

CONNECTIONS = {
    0: [1, 2, 3],
    1: [0, 4, 2, 3],
    2: [0, 1, 5],
    3: [0, 1, 6],
    4: [1, 7, 5, 6],
    5: [2, 4, 8, 17],
    6: [3, 4, 9, 18],
    7: [4, 10, 19, 20, 21, 22],
    8: [5, 15, 19, 21],
    9: [6, 16, 20, 22],
    10: [7, 13, 14, 11, 12],
    11: [10, 15, 13],
    12: [10, 16, 14],
    13: [10, 11, 15],
    14: [10, 12, 16],
    15: [8, 11, 13],
    16: [9, 12, 14],
    17: [5],
    18: [6],
    19: [7, 8],
    20: [7, 9],
    21: [7, 8],
    22: [7, 9]
}

JUMP_MAP = {
    (0, 1): 4, (1, 4): 7, (4, 7): 10,
    (0, 2): 5, (2, 5): 8, (5, 8): 15,
    (0, 3): 6, (3, 6): 9, (6, 9): 16,
    (17, 5): 4, (5, 4): 6, (4, 6): 18,
    (8, 19): 4, (19, 4): 20, (4, 20): 9,
    (8, 21): 7, (21, 7): 22, (7, 22): 9,
    (15, 11): 13, (11, 13): 10, (10, 14): 12, (14, 12): 16
}

for (f, o), t in list(JUMP_MAP.items()):
    JUMP_MAP[(t, o)] = f

def get_jump_target(from_node, over_node):
    return JUMP_MAP.get((from_node, over_node), None)

# ==========================================
# INTERACTIVE ANIMATIONS & PARTICLES ENGINE
# ==========================================
class Particle:
    def __init__(self, pos, color):
        self.x, self.y = pos
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-6, 2)
        self.color = color
        self.radius = random.randint(4, 9)
        self.alpha = 255

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.25  # Dynamic gravity scale
        self.alpha -= 7
        if self.radius > 0.5: self.radius -= 0.12
        return self.alpha > 0

    def draw(self, surface):
        if self.alpha <= 0: return
        s = pygame.Surface((int(self.radius * 2), int(self.radius * 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, self.alpha), (int(self.radius), int(self.radius)), int(self.radius))
        surface.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))

class StatsTracker:
    def __init__(self):
        self.games_played = 0
        self.goat_wins = 0
        self.tiger_wins = 0
        self.match_history = []

    def record_match(self, winner, caps):
        self.games_played += 1
        outcome = "Goats Won (Trapped)" if winner == "GOATS" else "Tigers Won (Hunted)"
        if winner == "GOATS": self.goat_wins += 1
        else: self.tiger_wins += 1
        self.match_history.append(f"M{self.games_played}: {outcome} ({caps} Caps)")
        if len(self.match_history) > 3: self.match_history.pop(0)

class GameState:
    def __init__(self):
        self.stats = StatsTracker()
        self.game_mode = "VS_AI_TIGER" # "LOCAL_2P", "VS_AI_TIGER", "VS_AI_GOAT"
        self.reset_board()

    def reset_board(self):
        self.board = {i: 0 for i in NODES}
        # Traditional Apex Starting Placements for Tigers
        self.board[0] = 1
        self.board[1] = 1
        self.board[4] = 1
        
        self.turn = "GOAT_PLACE"
        self.goats_in_hand = 15
        self.goats_captured = 0
        self.selected_node = None
        self.message = "Goats' Turn: Place a piece down."
        
        # Piece positional interpolation targets setup
        self.curr_positions = {i: list(NODES[i]) for i in NODES}

    def update_positions(self):
        for i, target in NODES.items():
            cx, cy = self.curr_positions[i]
            self.curr_positions[i][0] += (target[0] - cx) * 0.22
            self.curr_positions[i][1] += (target[1] - cy) * 0.22

# ==========================================
# ADVANCED ARTIFICIAL INTELLIGENCE BOT
# ==========================================
class AIEngine:
    @staticmethod
    def get_best_move(state):
        if state.turn == "TIGER_MOVE":
            return AIEngine._compute_tiger_move(state)
        elif state.turn in ["GOAT_PLACE", "GOAT_MOVE"]:
            return AIEngine._compute_goat_move(state)
        return None

    @staticmethod
    def _compute_tiger_move(state):
        tiger_nodes = [k for k, v in state.board.items() if v == 1]
        
        # Priority 1: Instant Capture Moves
        for t in tiger_nodes:
            for n in CONNECTIONS[t]:
                if state.board[n] == 2:
                    tgt = get_jump_target(t, n)
                    if tgt is not None and state.board[tgt] == 0:
                        return {"type": "JUMP", "from": t, "over": n, "to": tgt}
                        
        # Priority 2: Safe adjacent strategic movements
        valid_steps = []
        for t in tiger_nodes:
            for n in CONNECTIONS[t]:
                if state.board[n] == 0:
                    valid_steps.append({"type": "STEP", "from": t, "to": n})
        if valid_steps:
            valid_steps.sort(key=lambda m: len(CONNECTIONS[m["to"]]), reverse=True)
            return random.choice(valid_steps[:2]) if len(valid_steps) > 1 else valid_steps[0]
        return None

    @staticmethod
    def _compute_goat_move(state):
        empty_nodes = [k for k, v in state.board.items() if v == 0]
        tiger_nodes = [k for k, v in state.board.items() if v == 1]
        
        if state.turn == "GOAT_PLACE":
            safe_spots = []
            for e in empty_nodes:
                unsafe = False
                for t in tiger_nodes:
                    if e in CONNECTIONS[t]:
                        tgt = get_jump_target(t, e)
                        if tgt is not None and state.board[tgt] == 0:
                            unsafe = True
                if not unsafe: safe_spots.append(e)
            chosen = random.choice(safe_spots) if safe_spots else random.choice(empty_nodes)
            return {"type": "PLACE", "to": chosen}
        else:
            goat_nodes = [k for k, v in state.board.items() if v == 2]
            valid_steps = []
            for g in goat_nodes:
                for n in CONNECTIONS[g]:
                    if state.board[n] == 0:
                        valid_steps.append({"type": "STEP", "from": g, "to": n})
            return random.choice(valid_steps) if valid_steps else None

# ==========================================
# MECHANICS & EVENT HANDLERS
# ==========================================
def check_win_conditions(state):
    tiger_nodes = [k for k, v in state.board.items() if v == 1]
    tiger_can_move = False
    for t in tiger_nodes:
        for n in CONNECTIONS[t]:
            if state.board[n] == 0:
                tiger_can_move = True
                break
            if state.board[n] == 2:
                tgt = get_jump_target(t, n)
                if tgt is not None and state.board[tgt] == 0:
                    tiger_can_move = True
                    break
    if not tiger_can_move and state.goats_in_hand == 0: return "GOATS"
    if state.goats_captured >= 5: return "TIGERS"
    return None

def execute_action(action, state, particles):
    if not action:
        return
    
    action_type = action.get("type")
    
    if action_type == "PLACE":
        # Goat placement
        node = action.get("to")
        if state.board[node] == 0 and state.goats_in_hand > 0:
            state.board[node] = 2
            state.goats_in_hand -= 1
            play_sound(SOUND_PLACE)
            particles.extend([Particle(NODES[node], GOAT_COLOR) for _ in range(5)])
            
            # Check if all goats placed
            if state.goats_in_hand == 0:
                state.turn = "TIGER_MOVE"
                state.message = "Tigers' Turn: Move or capture."
            else:
                state.turn = "GOAT_PLACE"
                state.message = f"Goats' Turn: Place a piece. ({state.goats_in_hand} left)"
    
    elif action_type == "STEP":
        # Single step move
        from_node = action.get("from")
        to_node = action.get("to")
        
        if state.board[from_node] != 0 and state.board[to_node] == 0:
            piece = state.board[from_node]
            state.board[from_node] = 0
            state.board[to_node] = piece
            play_sound(SOUND_MOVE)
            particles.extend([Particle(NODES[to_node], GOAT_COLOR if piece == 2 else TIGER_COLOR) for _ in range(3)])
            
            # Switch turns
            if state.turn == "GOAT_MOVE":
                state.turn = "TIGER_MOVE"
                state.message = "Tigers' Turn: Move or capture."
            else:
                state.turn = "GOAT_MOVE"
                state.message = "Goats' Turn: Move your pieces."
    
    elif action_type == "JUMP":
        # Capture move
        from_node = action.get("from")
        over_node = action.get("over")
        to_node = action.get("to")
        
        if state.board[from_node] == 1 and state.board[over_node] == 2 and state.board[to_node] == 0:
            # Tiger captures goat
            state.board[from_node] = 0
            state.board[to_node] = 1
            state.board[over_node] = 0
            state.goats_captured += 1
            play_sound(SOUND_CAPTURE)
            particles.extend([Particle(NODES[over_node], GOAT_COLOR) for _ in range(8)])
            
            # Check win condition
            winner = check_win_conditions(state)
            if winner:
                state.stats.record_match(winner, state.goats_captured)
                state.message = f"{winner} WIN! (Captured: {state.goats_captured})"
                state.turn = "GAME_OVER"
            else:
                state.turn = "TIGER_MOVE"
                state.message = "Tigers' Turn: Move or capture."
    
    # Check general win conditions
    winner = check_win_conditions(state)
    if winner:
        state.stats.record_match(winner, state.goats_captured)
        state.message = f"{winner} WIN!"
        state.turn = "GAME_OVER"
        play_sound(SOUND_WIN)

def get_node_at_click(pos):
    """Return node index if click is near a node, else None."""
    x, y = pos
    for node_id, (nx, ny) in NODES.items():
        if (x - nx) ** 2 + (y - ny) ** 2 <= 25 ** 2:  # 25px radius
            return node_id
    return None

def draw_game(state, particles):
    """Render the entire game board and UI."""
    screen.fill(BG_COLOR)
    
    # Draw board background
    pygame.draw.rect(screen, BOARD_BG, (20, 20, WIDTH - 40, 680))
    
    # Draw connections
    for node_id, neighbors in CONNECTIONS.items():
        x1, y1 = NODES[node_id]
        for neighbor_id in neighbors:
            if neighbor_id > node_id:  # Avoid drawing twice
                x2, y2 = NODES[neighbor_id]
                pygame.draw.line(screen, GRID_COLOR, (x1, y1), (x2, y2), 2)
    
    # Draw nodes
    for node_id, (x, y) in NODES.items():
        pygame.draw.circle(screen, GRID_COLOR, (int(x), int(y)), 8)
    
    # Draw pieces
    for node_id, piece in state.board.items():
        x, y = state.curr_positions[node_id]
        if piece == 1:  # Tiger
            pygame.draw.circle(screen, TIGER_COLOR, (int(x), int(y)), 12)
        elif piece == 2:  # Goat
            pygame.draw.circle(screen, GOAT_COLOR, (int(x), int(y)), 10)
    
    # Highlight selected node
    if state.selected_node is not None:
        x, y = NODES[state.selected_node]
        pygame.draw.circle(screen, HIGHLIGHT_COLOR, (int(x), int(y)), 18, 3)
    
    # Draw particles
    for particle in particles:
        particle.draw(screen)
    
    # Draw UI panel
    pygame.draw.rect(screen, PANEL_BG, (0, 710, WIDTH, 210))
    pygame.draw.line(screen, GRID_COLOR, (0, 710), (WIDTH, 710), 2)
    
    # Draw stats and messages
    msg_surface = font_lg.render(state.message, True, TEXT_COLOR)
    screen.blit(msg_surface, (20, 730))
    
    stats_text = f"Goats in hand: {state.goats_in_hand}  |  Captured: {state.goats_captured}  |  Games: {state.stats.games_played}"
    stats_surface = font_md.render(stats_text, True, TEXT_COLOR)
    screen.blit(stats_surface, (20, 770))
    
    # Draw match history
    for i, match in enumerate(state.stats.match_history):
        hist_surface = font_sm.render(match, True, TEXT_COLOR)
        screen.blit(hist_surface, (20, 810 + i * 25))
    
    # Draw instructions
    inst_surface = font_sm.render("Click nodes to move | R: Reset | Q: Quit", True, GRID_COLOR)
    screen.blit(inst_surface, (20, 880))
    
    pygame.display.flip()

# ==========================================
# MAIN GAME LOOP
# ==========================================
def main():
    state = GameState()
    clock = pygame.time.Clock()
    particles = []
    running = True
    ai_delay = 0

    while running:
        ai_delay += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    state.reset_board()
                    particles = []
                    ai_delay = 0
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state.turn != "GAME_OVER":
                    clicked_node = get_node_at_click(event.pos)
                    if clicked_node is not None:
                        # Simple click-based UI: click a node to select/move
                        if state.selected_node is None:
                            # Select a piece
                            if state.board[clicked_node] != 0:
                                state.selected_node = clicked_node
                        else:
                            # Try to move to clicked node
                            from_node = state.selected_node
                            to_node = clicked_node
                            
                            # Check valid move
                            if to_node in CONNECTIONS[from_node]:
                                if state.board[to_node] == 0:
                                    # Simple step move
                                    if state.turn == "GOAT_PLACE":
                                        action = {"type": "PLACE", "to": to_node}
                                    else:
                                        action = {"type": "STEP", "from": from_node, "to": to_node}
                                    execute_action(action, state, particles)
                                    state.selected_node = None
                                elif state.board[to_node] != state.board[from_node]:
                                    # Possible capture
                                    target = get_jump_target(from_node, to_node)
                                    if target is not None and state.board[target] == 0:
                                        action = {"type": "JUMP", "from": from_node, "over": to_node, "to": target}
                                        execute_action(action, state, particles)
                                        state.selected_node = None
                            else:
                                state.selected_node = None
        
        # AI moves (if applicable)
        if state.turn in ["TIGER_MOVE", "GOAT_MOVE", "GOAT_PLACE"] and ai_delay > 30:
            if state.game_mode == "VS_AI_TIGER" and state.turn == "TIGER_MOVE":
                action = AIEngine.get_best_move(state)
                execute_action(action, state, particles)
                ai_delay = 0
            elif state.game_mode == "VS_AI_GOAT" and state.turn in ["GOAT_PLACE", "GOAT_MOVE"]:
                action = AIEngine.get_best_move(state)
                execute_action(action, state, particles)
                ai_delay = 0
        
        # Update game state
        state.update_positions()
        particles = [p for p in particles if p.update()]
        
        # Render
        draw_game(state, particles)
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
