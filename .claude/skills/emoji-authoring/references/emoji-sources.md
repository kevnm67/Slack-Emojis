# Where to get emoji

Licenses verified 2026-09-01. Re-check before relying on any of this — emoji
projects relicense and go unmaintained frequently.

## The distinction that matters here

This repository is **public**, so committing an image redistributes it.
Downloading an emoji and uploading it to your own Slack workspace is a
different act with different rules than committing it to this repo. A source
can be perfectly fine for the first and unusable for the second.

Judge a source on **redistribution rights**, not on whether the download is
free.

## Browsing and discovery

**[Slackmojis](https://slackmojis.com/)** — the primary place to find what
exists. Best curated collection of Slack-specific custom emoji, organized by
category, downloads already sized for Slack.

**Caveat, and it is a real one:** Slackmojis states no license for its images.
They are user submissions, largely fan art of third-party characters and
brands, and the site's terms assign submission rights to the site rather than
placing anything in the public domain. That makes it excellent for finding and
uploading an emoji to your own workspace, and unsuitable as a source for files
committed here, because there is no license to point at for any given image.

If you take something from Slackmojis into this repo anyway, that is a
deliberate call about fan-art risk on a personal project — make it knowingly,
and do not pretend a license exists.

## Safe to redistribute

Ordered by how little the license asks of you.

| Source | Graphics license | Attribution | Notes |
|---|---|---|---|
| [Fluent Emoji](https://github.com/microsoft/fluentui-emoji) (Microsoft) | MIT | copyright + license text | Lightest obligations; 3D, flat, and high-contrast styles |
| [Noto Emoji](https://github.com/googlefonts/noto-emoji) (Google) | Apache 2.0 | license notice, note modifications | Actively maintained, Unicode 17.0 |
| [Twemoji](https://github.com/jdecked/twemoji) (jdecked fork) | CC BY 4.0 | credit + license link | Use this fork — [twitter/twemoji](https://github.com/twitter/twemoji) is deprecated |
| [OpenMoji](https://openmoji.org/) | CC BY-SA 4.0 | credit + **ShareAlike** | Derivatives must stay CC BY-SA |

## Conditional

**[emoji.gg](https://emoji.gg/)** — per-emoji licensing chosen by the uploader,
across six license options. Only the **CC BY 4.0** and **WTFPL** ones may be
redistributed; the "Basic" and "Streamer" licenses forbid it. Check the license
badge on the individual emoji page, every time. Has a documented API.

**[Mutant Standard](https://mutant.tech/)** — CC BY-**NC**-SA 4.0. The
NonCommercial clause is deliberate and there is no commercial option. Fine for
a personal repo; a blocker the moment anything commercial touches it, and the
ShareAlike term propagates.

## Avoid

- **[twitter/twemoji](https://github.com/twitter/twemoji)** — deprecated by its
  own maintainers; use the jdecked fork.
- **[blobmoji](https://github.com/C1710/blobmoji)** — same permissive license
  as Noto, but archived read-only since June 2026. Take blobs from Noto Emoji
  directly instead.
- **Emojipedia** — a reference work, not a source. Its images are the vendors'
  copyrighted artwork; it does not grant redistribution rights.
- **Flaticon / Icons8 and similar** — "free" tiers carry mandatory attribution
  and license terms that generally do not survive redistribution in a repo.

## Recording provenance

When you add an emoji from a licensed source, note the source and license in
the PR description. Nothing in the tooling enforces this, and a year from now
the origin of an unattributed file is unrecoverable.
