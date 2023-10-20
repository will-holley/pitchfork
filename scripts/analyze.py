"""
Analyzes the scraped reviews.
"""
import pandas as pd

# ============================================================
# Constants
# ============================================================

CACHE_FILE_PATH = "cache/reviews.pkl"

# ============================================================
# Main
# ============================================================

df = pd.read_pickle(CACHE_FILE_PATH)
df.set_index("id", inplace=True, drop=True)

# Drop reviews that don't have a score (i.e. a "tombstone")
df.dropna(subset=["tombstone"], inplace=True)

# Prepend the host to urls so they're clickable when inspecting the dataframe
df["url"] = df.url.apply(lambda x: f"https://pitchfork.com{x}")

# TODO: Signal as to whether an album is historical, re-issue, etc. is unstructured and inconsistent.
# TODO: There are a few other ways to determine this, for example if the artist is dead when the album
# TODO: is released.
# # Attempt to find historical / re-issues.
# df["reissue"] = df.tombstone.apply(lambda x: x["bnr"])

# # Determine whether a review is archival or historical
# df["labeled_historical"] = df.dek.str.contains(r"(not in our archives)|(reissue)|(Today on Pitchfork)", case=False)

# # Pitchfork's Sunday reviews are historical
# df["is_sunday_review"] = df.tags.apply(lambda x: len([t for t in x if t["slug"] == "sunday-review"]) > 0)

# # For now, drop historical reviews. It would be interesting later to see
# # wether these receive higher average scores (which may reflect a nostalgia bias).
# df.drop(df[df["reissue"]].index, inplace=True)
# df.drop(df[df["labeled_historical"]].index, inplace=True)
# df.drop(df[df["is_sunday_review"]].index, inplace=True)

# Get album count
df["album_count"] = df.tombstone.apply(lambda x: len(x["albums"]))

# Drop reviews that have no albums i.e. no scores
df.drop(df[df["album_count"] == 0].index, inplace=True)

# Get all of the scores associated with a given review
df["scores"] = df.tombstone.apply(lambda x: [album["rating"]["rating"] for album in x["albums"]])

# Isolate the review scores as Series
scores = df.explode("scores")["scores"]
scores = scores.astype(float)

# Get the mean rating
mean = scores.mean()

# Get albums with a ten
tens = df.loc[scores[scores == 10].index]

# Get the rounded distribution
rounded = scores.round(0)

# Get the distribution of scores
distribution = rounded.value_counts().sort_index(ascending=False)

# Get dist as percentage
distribution_percentages = (distribution / distribution.sum() * 100).round(2)

print(f"Mean rating: {mean:.2f}")
print(f"Number of 10s: {len(tens)}")
print(f"Distribution (%):\n{distribution_percentages}")