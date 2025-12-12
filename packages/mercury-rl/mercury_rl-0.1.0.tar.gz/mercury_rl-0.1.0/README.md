# mercury-rl
[![Build Status](./docs/img/build-status.svg)](https://jenkins.globaldevtools.bbva.com/jenkins-gl-infraestructura/job/KAIF_repos/job/KAIF_repos/job/mercury-rl/job/master/)
[![Quality Gate Status](./docs/img/quality-gate.svg)](https://sonar.globaldevtools.bbva.com/datacenter/dashboard?id=GL_KAIF_APP-ID-2866825_DSG%3Amercury-rl)
[![Coverage](./docs/img/coverage.svg)](https://sonar.globaldevtools.bbva.com/datacenter/dashboard?id=GL_KAIF_APP-ID-2866825_DSG%3Amercury-rl)
[![Version](https://img.shields.io/badge/latest-0.1.0-blue/)](https://globaldevtools.bbva.com/bitbucket/projects/GL_KAIF_APP-ID-2866825_DSG/repos/mercury-rl/browse)

## Introduction

Welcome to `mercury-rl`, a library for offline deep reinforcement learning. This library offers classic implementations of state-of-the-art algorithms such as Conservative Q-Learning (CQL) and its variations, including Deep Q-Network (DQN), Actor-Critic (AC), Trust Region Policy Optimization (TRPO), and Proximal Policy Optimization (PPO).

Our goal is to provide a toolkit to develop, experiment, and deploy reinforcement learning models efficiently. `mercury-rl` aims to make your offline RL journey smoother and more productive.

### What is Offline Reinforcement Learning?

Offline reinforcement learning (offline RL) is a subfield of reinforcement learning where the agent is trained using a static dataset of interactions with the environment. On the other hand, in online reinforcement learning the agent continuously interacts with the environment to collect data and update its policy.

Offline RL is particularly useful in scenarios where real-time interaction with the environment is costly, risky, or impractical. Some examples include healthcare, robotics, and autonomous driving, where it is often not feasible to let an untrained agent explore freely. 

### Key Differences Between Offline RL and Online RL

| Aspect               | Offline RL                                             | Online RL                                                |
|----------------------|--------------------------------------------------------|----------------------------------------------------------|
| **Data Collection**  | Static dataset collected from previous interactions | Collects data through interaction with the environment |
| **Exploration**      | Does not involve exploration during training; the agent learns from the provided dataset | Requires exploration to improve the policy |
| **Safety and Feasibility** | Ideal for applications where exploration is dangerous or impractical | Suitable for environments where real-time feedback and interaction are feasible |
| **Algorithm Complexity** | Often requires more sophisticated algorithms to handle the limitations of fixed datasets | Can leverage simpler algorithms due to continuous data collection and real-time feedback |

![](https://offline-rl.github.io/assets/OFFLINE_RL.gif)

Figure taken from this [post](https://offline-rl.github.io/)


## Components

***

## Algorithms

The `mercury-rl` library implements a range of state-of-the-art algorithms for both discrete and continuous control tasks. Below is a summary of the key algorithms included in the library:

| algorithm | discrete control | continuous control |
|:-|:-:|:-:|
| [Imitation Learning](https://link.springer.com/chapter/10.1007/11564096_32) | :white_check_mark: | :white_check_mark: |
| [Conservative Deep Q-Network (DQN)](https://www.nature.com/articles/nature14236) | :white_check_mark: | :no_entry: |
| [Conservative Double DQN](https://arxiv.org/abs/1509.06461) | :white_check_mark: | :no_entry: |
| [Conservative Actor-Critic](https://arxiv.org/abs/1509.06461) | :white_check_mark: | :no_entry: |

### Requirements

mercury-rl development requires the following software installed:

- Python 3.6 or higher

Once the developer has checked out the source code from the repository, any changes to the code can be done through the creation of a new branch.

### Install

To install ***mercury-rl*** you only need a `pip-install`:

#### Datio

```sh
pip install --user mercury-rl
```

#### Local

You'll need to configure your Artifactory credentials. If you don't know how, you can find a mini tutorial on
our [Mercury’s developer handbook][Mercury’s developer handbook].

```sh
pip install mercury-rl --extra-index-url https://\${ARTIFACTORY_BOT_BASIC_AUTH}@artifactory.globaldevtools.bbva.com/artifactory/api/pypi/gl-datio-runtime-pypi-local/simple
```

## Exploratory notebooks

```python
from mercury.rl import create_tutorials

create_tutorials('mercury_tutorials')
```

The code above creates a local folder named `mercury_tutorials` and places a collection of notebooks inside showing different `mercury.rl` features.

## Contributing

Want to contribute to ***mercury-rl***?
More info about it on [Mercury’s developer handbook][Mercury’s developer handbook].

Powered by [Mercury](mailto:mercury.group@bbva.com).

[//]: # (TO-DO: pasar las URLs como variables)
[Mercury’s developer handbook]: https://globaldevtools.bbva.com/bitbucket/projects/GL_KAIF_APP-ID-2866825_DSG/repos/mercury-contrib/browse/CONTRIBUTING.md
