# Population Simulation

The aims of this project are as such:
1. Basic:
   - Square grid, with 3 categories of animals/entities:
     - Plant, can't move, has nutritious value, randomly spawns
     - Plant eater, can move slower, can reproduce with same species, eats plant
     - Meat eater, can move, fastest on the grid, can reproduce with same species, eats plant eater
2. Intermediate:
    - Add vision and hearing to the animals
    - Add evolution via genetic algorithms to animals
    - Add boundaries to the grip

Ideas:
- Boundaries:
  - Water


Todos:

- Add hunger rate
    - Number of steps per day
    - Add background colour for day/night cycle
- Add temperature
- Add weather
- Add seasons
- Add reproduction
  - Add death
  - Add birth
- Add vision
- Add hearing
-


With     
```python
board_size = (200.0, 200.0)
initial_spawns = dict(grass=2000, pig=100, fox=0)
```

- python 3.9 - numpy - 2.1-2.3s per step
- python 3.9 - numpy with pythran - 0.9-1.0s per step
- python 3.9 - list - 1.3-1.7s per step
- pypy3 - list - 0.6-0.9s per step