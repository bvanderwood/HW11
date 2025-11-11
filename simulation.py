from modelclasses import Agent, SimulationConfig
import matplotlib.pyplot as plt

def makeAgents(SimulationConfig):
    agents = []
    num_infected = int(SimulationConfig.agent_count * SimulationConfig.fraction_infected)
    for _ in range(num_infected):
        agents.append(Agent('I', SimulationConfig))
    for _ in range(SimulationConfig.agent_count - num_infected):
        agents.append(Agent('S', SimulationConfig))
    return agents

def makeGrid(SimulationConfig):
    return [[None for _ in range(SimulationConfig.grid_size)] for _ in range(SimulationConfig.grid_size)]

def runSimulation(SimulationConfig):
    agents = makeAgents(SimulationConfig)
    grid = makeGrid(SimulationConfig)
    for _ in range(SimulationConfig.steps):
        # Move everyone first
        for agent in agents:
            agent.move(grid)
            x, y = agent.get_position()
            grid[x][y] = agent

        # Iterate over the entire grid, find populated cells, check if any are infected and if so expose others
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell is None:
                    continue
                local_agents = [agent for agent in agents if agent.get_position() == (i, j)]
                infected_present = any(agent.get_status() == 'I' for agent in local_agents)
                for agent in local_agents:
                    agent.update_status(infected_present)
    return [agent.get_history() for agent in agents]

def collateResults(history):
    time_steps = len(history[0])
    susceptible_counts = [0] * time_steps
    infected_counts = [0] * time_steps
    recovered_counts = [0] * time_steps

    for agent_history in history:
        for i, state in enumerate(agent_history):
            if state == 'S':
                susceptible_counts[i] += 1
            elif state == 'I':
                infected_counts[i] += 1
            elif state == 'R':
                recovered_counts[i] += 1

    plt.plot(range(time_steps), susceptible_counts, label='Susceptible')
    plt.plot(range(time_steps), infected_counts, label='Infected')
    plt.plot(range(time_steps), recovered_counts, label='Recovered')
    plt.xlabel('Time Steps')
    plt.ylabel('Number of Agents')
    plt.legend()
    plt.show()

    max_infected = max(infected_counts)
    print(f'Maximum number of infected agents at any time: {max_infected}')
    mean_infected = sum(infected_counts) / time_steps
    print(f'Mean number of infected agents over time: {mean_infected:.2f}')
    std_dev_infected = (sum((x - mean_infected) ** 2 for x in infected_counts) / time_steps) ** 0.5
    print(f'Standard deviation of infected agents over time: {std_dev_infected:.2f}')
    peak_time = infected_counts.index(max_infected)
    print(f'Time step at which peak infection occurs: {peak_time}')
    total_recovered = recovered_counts[-1]
    print(f'Total number of agents that recovered by the end: {total_recovered}')
    return susceptible_counts, infected_counts, recovered_counts