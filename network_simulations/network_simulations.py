"""Main module."""
from network_simulations import environment, builder


def sim():
    results = [0, 0, 0]
    for _ in range(50):
        env = environment.Environment(
            agent_count=100,
            opinion_a_count=2,
            opinion_b_count=2,
            sample_size=3,
            bias=False,
            builder=builder.RandomNetworkBuilder(min_neighbors=3),
        )
        converged = 0
        sanity = 10000
        count = 0
        while not converged and count < sanity:
            env.advance()
            if count % 1000 == 0:
                converged = env.is_converged()
            count += 1
        results[converged] += 1

    print("FINAL: ")
    print(f"    UNDECIDED: {results[0]}")
    print(f"    OPINION_A: {results[1]}")
    print(f"    OPINION_B: {results[2]}")
