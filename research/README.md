# Research method

This directory records the study used to shape the collection. It intentionally keeps measurements and source links rather than reproducing other authors' skill text.

## Corpus

`analyze_skill_corpus.py` queried GitHub code search for `SKILL.md` files and terms associated with workflow, evidence, completion and progressive disclosure. Results were deduplicated by exact SHA-256 content hash. The committed `corpus.csv` contains repository, path, URL, content hash and structural features for 400 files across 364 repositories. Raw text is stored only in the gitignored `.research-cache/` directory.

This is a relevance-ranked convenience sample, not a random sample. It measures what instructions contain, not whether an agent follows them or whether users benefit.

## Marketplace snapshot

`capture_leaderboard.py` records the public Skills.sh leaderboard into `leaderboard.csv`. The snapshot contains 185 entries visible during capture. Displayed install counts are popularity signals, not quality measurements, and are analyzed separately from the corpus.

## Reproduce

The scripts require Python 3 and authenticated GitHub CLI access for corpus capture.

```sh
python3 research/analyze_skill_corpus.py --help
python3 research/capture_leaderboard.py --help
```

Exact results will change as search indexes and public marketplaces change. The committed summary is the dated input to this release, not a live claim.

