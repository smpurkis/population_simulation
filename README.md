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

seed 1
```commandline
step_no: 3001, time: 50.13427400588989, average: 16.71ms
Grass: 1167, Pigs: 294, Foxes: 0, Alive: 1990, Dead: 36077
  entity_class             name  mins     means  maxs
                                value     value value
0          pig   eating_penalty  0.42  0.803825  1.59
1          pig           health  0.38  1.036746  1.89
2          pig           hunger  0.45  1.062459  1.76
3          pig         lifespan  0.28  1.009685  1.61
4          pig  reproduce_cycle  0.29  1.206448  1.66
5          pig            speed  0.42  0.955613  1.53
6          pig    vision_radius  0.25  0.654780  1.59
Analyze genes time: 21.094 ms
Analyze time: 21.118 ms
```

seed 2
```commandline
step_no: 3001, time: 49.434587717056274, average: 16.47ms
Grass: 1050, Pigs: 240, Foxes: 0, Alive: 1720, Dead: 40608
  entity_class             name  mins     means  maxs
                                value     value value
0          pig   eating_penalty  0.39  0.925242  1.60
1          pig           health  0.46  1.131719  1.73
2          pig           hunger  0.46  0.981970  1.75
3          pig         lifespan  0.29  0.993590  1.74
4          pig  reproduce_cycle  0.46  1.116140  1.77
5          pig            speed  0.29  0.976306  1.48
6          pig    vision_radius  0.25  0.714550  1.52
Analyze genes time: 17.784 ms
Analyze time: 17.803 ms
```

seed 3
```commandline
step_no: 3001, time: 82.81284141540527, average: 27.60ms
Grass: 802, Pigs: 864, Foxes: 0, Alive: 2386, Dead: 37798
  entity_class             name  mins     means  maxs
                                value     value value
0          pig   eating_penalty  0.29  0.911202  1.69
1          pig           health  0.44  1.062222  1.82
2          pig           hunger  0.25  1.067163  1.58
3          pig         lifespan  0.32  1.031164  1.76
4          pig  reproduce_cycle  0.33  1.202554  1.72
5          pig            speed  0.30  0.873362  1.74
6          pig    vision_radius  0.25  0.600957  1.69
Analyze genes time: 27.152 ms
Analyze time: 27.175 ms
```
