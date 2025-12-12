# Coupled Simulation

This page explains the working of the coupled simulation.

## Bids

A satellite model expresses its (flexible) demand by submitting bids to the market.
These bids should have the following structure:

| exclusive_group_id | profile_block_id | timestamp | quantity | price |
|--------------------|------------------|-----------|----------|-------|
| ...                | ...              | ...       | ...      | ...   |

Where `quantity` is **positive** for demand, and **negative** for supply. A
consumer who can shift their demand will only submit positive values, while a
Vehicle-to-Grid prosumer may also submit negative quantity values.
