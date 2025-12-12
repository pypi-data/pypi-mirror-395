import re
from crossref_matcher import Strategy, MatchTask


def is_doi(input_str):
    doi_pattern = re.compile(r"^10.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
    return bool(doi_pattern.match(input_str))


class ExampleMatchingStrategy(Strategy):
    strategy = "example-matching-strategy"
    task = MatchTask.REFERENCE
    description = "Example strategy. Takes a DOI and returns the same DOI. If the input is not a DOI, returns no match."
    default = False

    def __init__(self):
        pass

    def match(self, input_data):
        input_data = (
            input_data.replace("https://doi.org/", "").replace("doi:", "").strip()
        )
        if is_doi(input_data):
            return [
                {
                    "id": f"https://doi.org/{input_data}",
                    "confidence": 1.0,
                    "strategies": [self.strategy],
                }
            ]
        return []
