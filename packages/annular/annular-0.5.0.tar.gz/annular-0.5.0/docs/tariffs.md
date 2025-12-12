# Tariffs

Annular supports simulating the effect of market interventions through various
policies and tariffs. We aim to support a wide range of potential tariffs, and
provide an easy interface for accessing their values in the internals of any
bidding strategy.

This page will explain the:
- design philosophy
- expected data format and schema
- provided runtime interface

## Design philosophy

Tariffs can be defined for many different scenarios, and are commonly separated
according to both some categorical values and some temporal aspect. Each tariff
should be recorded in a separate file to avoid having to specify unnecessary
values for all possible index combinations. This means that each file only
specifies the required indexing levels relevant for that particular tariff. As
an added benefit, this makes the system very modular, as replacing a single
tariff means exactly replacing a single file, without being bound by indexing
levels of those other tariffs.

In use, we see the main distinction between 'categorial' and 'temporal' index
levels, with the categorical index assumed to be fixed during the runtime of a
simulation. This leaves the temporal index to be selected at runtime through a
simple interface.

We acknowledge that some of these categories may depend on the maximum used
capacity, with jumps in tariff value between them. In such cases, we assume that
the final category in which you end up is known to you beforehand with a high
degree of certainty.

## Data format and schema

All tariffs should be defined in [tidy][tidy-verse] CSV files. A single CSV file
`<tariff_name>.csv` should contain the full specification of a _single_ tariff.
The name of the file will be used as the identifier for that tariff when loaded.
The collection of tariff files should be contained in a single folder. This
should include any other tariff-related variables such as weighting factors.

Each CSV file should be formatted as follows:

| Grid level | Consumer type | ... | month | weekday/weekend | ... | hour | value |
|------------|---------------|-----|-------|-----------------|-----|------|-------|
| ...        | ...           | ... | ...   | ...             | ... | ...  | ...   |

In order, the file should contain the following columns, preferably in this order:
- Categorical index levels (Grid level, Consumer type, ...)
- Temporal index levels if relevant (month, weekday/weekend, ..., hour)
- Value

Each file should only contain those columns that are necessary to specify the
tariff. E.g., if there is no monthly variance in a tariff, a `month` column
should not be specified.

## Runtime interface

A folder of tariffs can be loaded using the `TariffManager.from_folder()`
method. This takes an argument of type `Path` pointing to the folder containing
the collection of CSV files defining the tariffs. Additionally, a dictionary of
categorical index keys must be passed in with the `preselect` argument to select
values that remain fixed for the runtime of the simulation.

Once the `TariffManager` has been instantiated, tariff values can be retrieved
by name and date using the `fetch(name=..., date=...)` method. The tariff
returned by the `fetch` method can be either a single value, or a pandas Series
object of tariff values indexed by hour.

### Fetch types

We distinguish between the following 'tariff fetching scenarios':

- A tariff is not temporally indexed: `fetch(name) -> float`

  If there is no time to vary by, then the only relevant selection is the preselection that's already happened.
  Just return the relevant value.

- A tariff is *at least* indexed by hour: `fetch(name, timestamps) -> pd.Series`, with `timestamps` as its index.

  If it is *at least* indexed by hour, then we want to have an exact value for each timestamp.
  Date-parsing should happen as part of this.

- A tariff only date-indexed, not time-indexed: `fetch(name, timestamps) -> pd.Series`

  When not time-indexed, there is no need to return a value for every timestamp.
  But it will still be necessary to distinguish between e.g. January/February within a single 'fetch' cycle.
  The fetch function should boil down the index to only those columns for which a selection can still be made,
  with the only relevant values being those that can be parsed from the given collection of timestamps.


### Temporal index level parsing

Since all remaining index levels are temporal in nature, the `date` argument
of the `fetch` method is used to select the relevant values. The `TariffManager`
supports automatically parsing the date to certain kinds of index levels if the
column name exactly matches one of the following:

- `"year"`
- `"month"`
- `"weekday/weekend"` (where Dutch national holidays are included in the 'weekend' category)



[tidy-verse]: https://r4ds.hadley.nz/data-tidy.html
