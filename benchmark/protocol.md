# MapBench generation protocol

## Generation unit

Each benchmark item consists of a historical-map subject and a shared atlas-map instruction. The generator receives only the resulting text prompt. It does not receive the hidden reference image, a style image, a description of the reference layout, or another generated attempt.

Each item runs in a fresh session with one completed image-generation call. There are no corrective prompts, retries chosen for visual quality, or post-generation edits. Provider failures that occur before an image call completes do not count as attempts.

## Evaluation unit

The saved prompt defines the requested content. A hidden historical map supplies comparative evidence, but judges may disagree with it when historical knowledge or stronger evidence warrants doing so. The generated image is not scored for pixel similarity, visual imitation, ornament, or fidelity to the reference's palette and composition.

Judges inspect the image at normal size and with reasonable zoom. They score the four dimensions in [`rubric.md`](rubric.md), record each material error once, apply the required cap, and retain the raw score.

## Ranking

Maps rank by final capped score. Ties use raw score, followed by item ID. System-level summaries report both raw and final means because the cap distribution deliberately compresses maps with material errors into usability bands.

## Current generation systems

### Codex image run

The initial run used the image generator exposed inside Codex. The tool did not expose an exact image-model identifier or seed. Sol Medium and Terra High independently scored every map using whole-number dimension scores.

Sol High adjudicated an item when the initial judges disagreed about a material error or cap, placed it in different interpretation bands, differed by more than ten raw-score points, or had a two-point dimension disagreement affecting a central claim. The adjudicator's complete record became final.

For a non-adjudicated item, the two judges had to agree on the cap and material-error count. Their dimension scores were averaged, the raw score was recomputed from those means, and the shared cap was applied. In the hard extension, non-adjudicated items additionally required both judges to assign no material errors and a cap of 100. This is why final aggregate dimension scores can contain half-points even though individual judges used whole numbers.

The released judge records are under [`../results/codex-image/judges/`](../results/codex-image/judges/). The aggregate identifies each map as `two-judge-mean` or `sol-high-adjudication`.

### Gemini agent and image-backend run

Gemini 3.7 Flash High ran through `agy` at high reasoning effort and called Antigravity's native `generate_image` tool. Quota metadata identified the image backend as `gemini-3.1-flash-image`. Sol High alone scored all 40 outputs without access to the earlier Codex scores.

This is a test of the complete agent and image-backend pipeline. It is not a claim that Gemini 3.7 Flash directly rendered the pixels. Because this run used a different evaluator topology, its score deltas against the Codex run are exploratory rather than a controlled model ranking.
