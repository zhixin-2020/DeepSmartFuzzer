#!/bin/bash

# this function is called when Ctrl-C is sent
function trap_ctrlc ()
{
    echo " Stopping"
    exit 2
}
# initialise trap to call trap_ctrlc function
# when signal 2 (SIGINT) is received
trap "trap_ctrlc" 2


models=( "CIFAR_CNN" )
covs=( "kmn" )

for model in "${models[@]}"
do
    for cov in "${covs[@]}"
    do
        echo "cifar - mcts_clustered - $model - $cov experiments"
        for (( counter=1; counter<=3; counter++ )) 
        do
            echo "cifar - mcts_clustered - $model - $cov iteration: $counter"
            python3 run_experiment.py --params_set cifar10 $model mcts $cov --dataset CIFAR10 --model $model --coverage $cov --input_chooser clustered_random --runner mcts_clustered --random_seed $counter --image_verbose False > "experiments/cifar/mcts_clustered/$model-$cov-$counter.txt" 
        done
    done
done
