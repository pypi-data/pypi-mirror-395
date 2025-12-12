from .multi_profile_strategy import MultiProfileBiddingStrategy
from .reading_bids_strategy import ReadingBidsStrategy
from .satellite_model import SatelliteModel as SatelliteModel
from .simple_demo import SimpleMultiHourBiddingStrategy

strategies = {
    "multi_profile": MultiProfileBiddingStrategy,
    "reading_bids": ReadingBidsStrategy,
    "simple": SimpleMultiHourBiddingStrategy,
}
