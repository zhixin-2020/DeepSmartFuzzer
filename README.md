# RLforDL

# Generating coverage-increasing mutated inputs by exploiting the explored coverage-increase patterns

### 1) Install Dependencies
```
pip install -r requirements.txt
```

### 2) Usage
```
usage: run_experiment.py [-h] [--params_set {mnist_lenet,cifar10}]
                         [--dataset {MNIST,CIFAR10}]
                         [--model {LeNet1,LeNet4,LeNet5,CIFAR_ORIGINAL}]
                         [--implicit_reward [IMPLICIT_REWARD]]
                         [--coverage {neuron,kmn,nbc,snac}]
                         [--input_chooser {random,clustered_random}]
                         [--runner {mcts,mcts_clustered,mcts_selected,deephunter}]
                         [--batch_size BATCH_SIZE]
                         [--nb_iterations NB_ITERATIONS] [--verbose [VERBOSE]]
                         [--image_verbose [IMAGE_VERBOSE]]

Experiments Script For RLforDL

optional arguments:
  -h, --help            show this help message and exit
  --params_set {mnist_lenet,cifar10}
  --dataset {MNIST,CIFAR10}
  --model {LeNet1,LeNet4,LeNet5,CIFAR_ORIGINAL}
  --implicit_reward [IMPLICIT_REWARD]
  --coverage {neuron,kmn,nbc,snac}
  --input_chooser {random,clustered_random}
  --runner {mcts,mcts_clustered,mcts_selected,deephunter}
  --batch_size BATCH_SIZE
  --nb_iterations NB_ITERATIONS
  --verbose [VERBOSE]
  --image_verbose [IMAGE_VERBOSE]
```

## Copyright Notice
RLforDL Copyright (C) 2019 Bogazici University

RLforDL is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

RLforDL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with RLforDL. If not, see https://www.gnu.org/licenses/.

mail: hasan.eniser@boun.edu.tr, samet.demir1@boun.edu.tr

