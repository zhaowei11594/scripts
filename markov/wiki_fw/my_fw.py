import numpy as np

states = ('rain', 'no rain')

transition_probability = np.array([
        [0.7, 0.3],
        [0.3, 0.7]
    ])

observations = [
    np.array([[0.9, 0.0], 
            [0.0, 0.2]]
    ),
    np.array([[0.9, 0.0], 
            [0.0, 0.2]]
    ),
    np.array([[0.1, 0.0], 
            [0.0, 0.8]]
    ),
    np.array([[0.9, 0.0], 
            [0.0, 0.2]]
    ),
    np.array([[0.9, 0.0], 
            [0.0, 0.2]]
    ),
]

def forward_backward(obs, transition_probability):
    end = -1
    def normalize(x): return x / sum(x.reshape(-1))
    f = [np.array([[0.5] for _ in states])]
    for x in obs:
        new_f = np.dot(np.dot(x, transition_probability.transpose()), f[end])
        f.append(normalize(new_f))
    b = [np.array([[1.0] for _ in states])]
    for x in reversed(obs):
        new_b = np.dot(np.dot(transition_probability, x), b[end])
        b.append(normalize(new_b))
    gamma = [normalize(i_f * i_b) for i_f, i_b in zip(f, reversed(b))]
    return f, b, gamma

for sample in forward_backward(observations, transition_probability):
    print '===================='
    for line in sample:
        print line
