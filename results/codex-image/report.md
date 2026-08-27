# MapBench v0.2: 40-map benchmark

## Result

Across forty one-shot, text-only map generations, the image model scores **71.11/100** under the MECE v3 map-drawing rubric. The median is **74** and the uncapped raw mean is **81.79**.

| Measure | Result |
| --- | ---: |
| Final mean | 71.11 |
| Final median | 74.00 |
| Uncapped raw mean | 81.79 |
| Maps with material errors | 29 / 40 |
| Independent material errors | 61 |
| Excellent | 10 / 40 |
| Good | 1 / 40 |
| Usable drafts | 11 / 40 |
| Misleading | 14 / 40 |
| Substantive failures | 4 / 40 |

## What the benchmark measures

| Dimension | Weight | Mean |
| --- | ---: | ---: |
| Spatial construction | 40 | 4.16 / 5 |
| Factual and semantic correctness | 25 | 3.19 / 5 |
| Required coverage | 15 | 4.35 / 5 |
| Cartographic legibility | 20 | 4.88 / 5 |

The model is consistently excellent at making information look like a clear professional map. Factual correctness is the limiting capability. Of the 61 material errors, 42 are factual, ten spatial, nine omissions, and none primarily legibility failures.

## Cohort comparison

| Cohort | Final mean | Raw mean | Excellent | Good | Usable | Misleading | Failure |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MB001-MB020 | 71.73 | 83.63 | 5 | 0 | 6 | 8 | 1 |
| MB021-MB040 harder set | 70.50 | 79.95 | 5 | 1 | 5 | 6 | 3 |

The harder set lowers the raw mean by 3.68 points and the capped mean by 1.23. Caps compress the difference because many maps in both cohorts already hit 74 or 59. The harder cohort's clearer effect is three central-frame failures instead of one.

## Combined ranking

Maps tied at 74 or 59 share the same reliability classification. Raw score is only a tie-breaker within those groups.

| Rank | ID | Subject | Final | Raw |
| ---: | --- | --- | ---: | ---: |
| 1 | MB005 | Roman Empire, 117 CE | 100 | 100 |
| 2 | MB038 | Partition of India, 1947 | 98 | 98 |
| 3 | MB006 | Silk Roads | 97.5 | 97.5 |
| 4 | MB028 | Indian Ocean trade, c. 1450 | 97.5 | 97.5 |
| 5 | MB039 | African decolonization | 97.5 | 97.5 |
| 6 | MB003 | Classical Greece | 97 | 97 |
| 7 | MB034 | Atlantic Revolutions | 96 | 96 |
| 8 | MB035 | Indian Rebellion, 1857-1858 | 96 | 96 |
| 9 | MB002 | Ancient Egypt | 95 | 95 |
| 10 | MB010 | Viking expansion | 90 | 90 |
| 11 | MB023 | Byzantine-Sasanian War, c. 620 | 84 | 84 |
| 12 | MB001 | Late Bronze Age collapse | 74 | 90 |
| 13 | MB012 | Mongol Empire | 74 | 90 |
| 14 | MB025 | Tang and neighboring powers | 74 | 90 |
| 15 | MB021 | Diadochi after Ipsus | 74 | 87 |
| 16 | MB026 | Maritime Southeast Asia | 74 | 87 |
| 17 | MB032 | Europe after Westphalia | 74 | 87 |
| 18 | MB016 | Precolonial Africa | 74 | 86 |
| 19 | MB019 | Central European railways | 74 | 83 |
| 20 | MB015 | Early European voyages | 74 | 82 |
| 21 | MB027 | Mongol successor states | 74 | 82 |
| 22 | MB013 | Black Death | 74 | 78 |
| 23 | MB014 | Ottoman Europe, 1683 | 59 | 85 |
| 24 | MB017 | Thirteen Colonies, 1775 | 59 | 85 |
| 25 | MB030 | West Africa and Songhai | 59 | 85 |
| 26 | MB020 | Europe, 1914 | 59 | 84 |
| 27 | MB009 | Maya civilization | 59 | 81 |
| 28 | MB018 | Napoleonic Europe, 1811 | 59 | 79 |
| 29 | MB040 | Cold War world, 1962 | 59 | 79 |
| 30 | MB011 | Crusades | 59 | 77 |
| 31 | MB007 | Mauryan Empire | 59 | 74 |
| 32 | MB022 | Roman crisis, 271 CE | 59 | 74 |
| 33 | MB033 | Seven Years' War | 59 | 74 |
| 34 | MB037 | Russian Civil War, 1919 | 59 | 74 |
| 35 | MB008 | Han dynasty | 59 | 69 |
| 36 | MB029 | Americas, 1491 | 59 | 62 |
| 37 | MB036 | Africa: claims and control, 1885 | 39 | 59 |
| 38 | MB004 | Persia, 1730 | 39 | 50 |
| 39 | MB024 | Abbasid Revolution, 750 | 39 | 45 |
| 40 | MB031 | Ottoman, Safavid, and Mughal worlds | 39 | 45 |

## Protocol

- Every generation received one saved text prompt and no reference pixels.
- One generation call was made per map, with no correction, retry, or image editing.
- Hidden references were supplied only to judges as comparative evidence, not infallible ground truth.
- Sol Medium and Terra High scored every map independently; substantive disputes received fresh Sol High adjudication.
- No OCR, pixel similarity, or reconstruction score was used.

## Verdict

The forty-item result supports a stable conclusion: **the model is an excellent map renderer but an unreliable historical cartographer.** One quarter of the maps are excellent with no detected material defect. Nearly three quarters contain at least one substantive historical, spatial, or coverage error, often presented with publication-quality confidence.
