# Reading Bids Strategy

The `ReadingsBidsStrategy` is an easy way to pre-program time-varying behavior of a satellite model
without relying on any computation logic. The exact bids that should be submitted to the central
market can be defined, for as many or few days as desired. This strategy will continuously iterate
over the bids, looping back to the start of the file when the end is reached.

Example use cases for this strategy include submitting the same set of profile bids every day, or
defining fixed weekly behavior that will repeat every 7 days.

## Configuration

The `ReadingsBidsStrategy` has various parameters to configure to perform its function. They
are listed below with an explanation.

These attributes are mandatory: the strategy cannot function without this information. All paths are
interpreted as relative to the location of the configuration file they are specified in. This is the
recommended usage. Alternatively, paths can be given as absolute, although this is discouraged for
the sake of reproducibility across different machines.

- `bids_csv_path`
  The bids to be repeated should be listed in this csv file. The expected format is:

  | exclusive_group_id | profile_block_id | timestamp | quantity | price |
  |--------------------|------------------|-----------|----------|-------|
  | ...                | ...              | ...       | ...      | ...   |

  Note that the earliest value in the `timestamp` column must match the first timestamp used by
  the central market and other bidding strategies. The global `start_hour` attribute (or local
  overwrite of it) is ignored.

- `rolling_horizon_step`
  Defines the number of timesteps for the bidding window. Changing this value to anything other than
  that used for the whole simulation is not recommended, and will likely result in infeasibility
  issues.

Any other globally shared or defined attributes are ignored by this strategy.
