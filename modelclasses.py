import random

# Agent class definition
class Agent(object):
    def __init__(self, status, config):
        self.config = config
        self.status = status # 'S' (Susceptible), 'I' (Infected), 'R' (Recovered)
        self.position = (random.randint(0, config.grid_size - 1), random.randint(0, config.grid_size - 1)) 
        self.history = [self.status]  # store initial state too

    def move(self, grid):
        if self.config.avoidance:
            #See if any neighboring cells have infected agents
            if self.check_neighbors(grid):
                # move away from infected neighbors
                x, y = self.position
                possible_moves = [(-1,0), (1,0), (0,-1), (0,1)]
                safe_moves = []
                for dx, dy in possible_moves:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.config.grid_size and 0 <= ny < self.config.grid_size:
                        if grid[nx][ny] is None or grid[nx][ny].get_status() != 'I':
                            safe_moves.append((nx, ny))
                if safe_moves:
                    self.position = random.choice(safe_moves)
                else:
                    self.position = (x, y)  # stay in place if no safe moves
            else:
                if self.config.social_distancing:
                    levy_prob = self.config.levy_prob_distancing
                    self.Levy_move(levy_prob)
                else:
                    levy_prob = self.config.levy_prob_nodistancing
                    self.Levy_move(levy_prob)
        elif self.config.social_distancing:
            levy_prob = self.config.levy_prob_distancing
            self.Levy_move(levy_prob)
        else:
            levy_prob = self.config.levy_prob_nodistancing
            self.Levy_move(levy_prob)
    
    def expose(self):
        #check if current status is susceptible and wasn't changed this step
        if self.status == 'S' and self.history[-1] == 'S':
            if random.random() < self.config.p:  # Probability of infection
                self.status = 'I'
    
    def recover(self):
        #check if current status is infected and wasn't changed this step
        if self.status == 'I' and self.history[-1] == 'I':
            if random.random() < self.config.q:  # Probability of recovery
                self.status = 'R'

    def update_status(self, exposed_yn):
        if exposed_yn:
            self.expose()
        self.recover()
        self.history.append(self.status)

    def check_neighbors(self, grid):
        # See if any neighboring cells have infected agents
        x, y = self.position
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.config.grid_size and 0 <= ny < self.config.grid_size:
                    neighbors.append(grid[nx][ny])
        infected_neighbors = any(neighbor is not None and neighbor.get_status() == 'I' for neighbor in neighbors)
        return infected_neighbors
    
    def Levy_move(self, prob):
        if random.random() >= prob:
            return  # Stay in place

        # Implement Levy walk movement
        step_size = int(random.paretovariate(1.5))  # Levy distribution step size
        step_size = min(step_size, self.config.grid_size - 1)  # Limit step size to grid size
        #move in only x or y direction
        if random.random() < 0.5:
            new_x = self.position[0] + random.choice([-step_size, 0, step_size])
            new_y = self.position[1]
        else:
            new_x = self.position[0]
            new_y = self.position[1] + random.choice([-step_size, 0, step_size])
        new_position = (new_x, new_y)
        # Ensure the agent stays within bounds
        if 0 <= new_x < self.config.grid_size and 0 <= new_y < self.config.grid_size:
            self.position = new_position

    def get_position(self):
        return self.position
    
    def get_status(self):
        return self.status
    
    def get_history(self):
        return self.history
    
    def __iter__(self):
        return iter((self.get_position(), self.get_status()))

# SimulationConfig class definition    
class SimulationConfig:
    def __init__(self, grid_size = 75, agent_count = 100, steps = 200, social_distancing = False, avoidance = False, levy_prob_nodistancing = 1, levy_prob_distancing = 0.5, fraction_infected = 0.05, p = 0.3, q = 0.01):
        self.grid_size = grid_size
        self.agent_count = agent_count
        self.steps = steps
        self.social_distancing = social_distancing
        self.avoidance = avoidance
        self.levy_prob_nodistancing = levy_prob_nodistancing
        self.levy_prob_distancing = levy_prob_distancing
        self.fraction_infected = fraction_infected
        self.p = p
        self.q = q
    