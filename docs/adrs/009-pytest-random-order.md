# Choosing pytest-randomly for randomizing test order

## Status

Accepted

## Context

Unit tests should not have any run order dependency on each other. However, if you always run the tests in the same
order, then there can be accidental dependencies on artifacts or side effects of previous tests that are unknown until
something goes wrong.

Running tests in different orders on different runs tends to expose created and accidental test order dependencies,
helping to keep tests independent.

This project uses pytest, so a pytest test order "randomizer" should be used to  mix up test order.

## Decision

We will use the **pytest-randomly** plugin for this purpose, with the following rationale:

- **Prior experience**: The developer has experience with this module from prior work.
- **Wide Adoption**: The [`pytest-randomly` repository](https://github.com/pytest-dev/pytest-randomly) has 634 stars
- **Easy To Use**: The library is easy to configure with `nox` and other project tools.

## Consequences

We are constrained to working within the limitations of the options of this plugin. However, no blocking constraints
are known of.

## Alternatives Considered

1. `pytest-random`
   - Written in 2013 and not maintained.
   - Less wide adoption, with 19 stars in GitHub.

1. `pytest-random-order`
   - While maintained, requires configuration to **turn on** random order for tests.
   - Less wide adoption, with 67 stars in GitHub.

## Decision Owner

Tom Willis

## Date

2024-12-10
