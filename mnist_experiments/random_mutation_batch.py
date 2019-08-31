from mnist_lenet_experiment import mnist_lenet_experiment
import numpy as np
import itertools
import src.image_transforms
import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure(1)
ax = plt.imshow(np.random.randint(0,256,size=(28,28)))
fig2 = plt.figure(2)
ax2 = plt.imshow(np.random.randint(0,256,size=(28,28)))
plt.title("NOT FOUND ANY COVERAGE INCREASE")

args, (train_images, train_labels), (test_images, test_labels), model, coverage, input_chooser = mnist_lenet_experiment("random_multi_image")

np.random.seed(seed=213123)

test_input, _ = input_chooser()

coverage.step(test_images)
print("initial coverage: %g" % (coverage.get_current_coverage()))

input_lower_limit = 0
input_upper_limit = 255
action_division_p1 = (1,3,3,1)
actions_p2 = [-30, 30, ("translation", (10, 10)), ("rotation", 3), ("contrast", 1.2), ("blur", 1), ("blur", 4), ("blur", 7)]

input_shape = test_input.shape
options_p1 = []
actions_p1_spacing = []
for i in range(len(action_division_p1)):
    spacing = int(input_shape[i] / action_division_p1[i])
    options_p1.append(list(range(0, input_shape[i], spacing)))
    actions_p1_spacing.append(spacing)

actions_p1 = list(itertools.product(*options_p1))

def apply_action(mutated_input, action1, action2):
    action_part1 = actions_p1[action1]
    action_part2 = actions_p2[action2]
    lower_limits = np.subtract(action_part1, actions_p1_spacing)
    lower_limits = np.clip(lower_limits, 0, action_part1) # lower_limits \in [0, action_part1]
    upper_limits = np.add(action_part1, actions_p1_spacing)
    upper_limits = np.clip(upper_limits, action_part1, input_shape) # upper_limits \in [action_part1, self.input_shape]
    s = tuple([slice(lower_limits[i], upper_limits[i]) for i in range(len(lower_limits))])
    if not isinstance(action_part2, tuple):
        mutated_input[s] += action_part2
    else:
        f = getattr(image_transforms,'image_'+action_part2[0])
        m_shape = mutated_input[s].shape
        i = mutated_input[s].reshape(m_shape[-3:])
        i = f(i, action_part2[1])
        mutated_input[s] = i.reshape(m_shape)
    mutated_input[s] = np.clip(mutated_input[s], input_lower_limit, input_upper_limit)
    return mutated_input

def tc3(level, test_input, mutated_input):
    c1 = level > 10 # Tree Depth Limit
    c2 = not np.all(np.abs(mutated_input - test_input) < 100) # L_infinity < 20
    return  c1 or c2

verbose, verbose_image = True, True

for i in range(1, 1000):
    test_input, test_label = input_chooser()
    best_coverage, best_input = 0, np.copy(test_input)
    iteration_count = 0
    while not iteration_count > 100:
        level = 0
        mutated_input = np.copy(test_input)
        while not tc3(level, test_input, mutated_input):
            action1 = np.random.randint(0,len(actions_p1))
            action2 = np.random.randint(0,len(actions_p2))
            mutated_input = apply_action(mutated_input, action1, action2)
            level += 1
            _, coverage_sim = coverage.step(mutated_input, update_state=False, with_implicit_reward=args.implicit_reward)
            if verbose_image:
                plt.figure(1)
                ax.set_data(mutated_input.reshape((28,28)))
                plt.title("Action: " + str((action1,action2)) + " Coverage Increase: " + str(coverage_sim))
                fig.canvas.flush_events()
            #print("coverage", coverage_sim)
            if coverage_sim > best_coverage:
                best_input, best_coverage = np.copy(mutated_input), coverage_sim
                if verbose_image:
                    plt.figure(2)
                    ax2.set_data(best_input.reshape((28,28)))
                    plt.title("BEST Coverage Increase: " + str(best_coverage))
                    fig2.canvas.flush_events()
        if verbose:
            print("Completed Iteration #%g" % (iteration_count))
            print("Current Coverage: %g" % (coverage_sim))
            print("Best Coverage up to now: %g" % (best_coverage))
        
        if iteration_count > 10 and best_coverage == 0:
            break
        
        iteration_count += 1
    
    if best_coverage > 0:
        input_chooser.append(best_input, test_label)
        coverage.step(best_input, update_state=True)
        print("IMAGE %g SUCCEED" % (i))
        print("found coverage increase", best_coverage)
        print("found different input", np.any(best_input-test_input != 0))
        print("Current Total Coverage", coverage.get_current_coverage())
    else:
        print("IMAGE %g FAILED" % (i))