# MapBench: Gemini/agy map-generation result

## Result

The comparison with the Codex image run is exploratory because the evaluator topologies differ. The Gemini scores describe this run under its Sol High evaluation; the cross-system deltas do not establish a controlled model ranking.

The Gemini/agy pipeline scores **68.20/100** across the same forty historical-map prompts. The original Codex built-in image-generator run scored **71.11**.

| Measure | Gemini/agy | Original image run | Difference |
| --- | ---: | ---: | ---: |
| Final mean | 68.20 | 71.11 | -2.91 |
| Raw mean | 71.75 | 81.79 | -10.04 |
| Final median | 74.00 | 74.00 | +0.00 |
| Maps with material errors | 28 / 40 | 29 / 40 | -1 |

Gemini scores higher on 12 prompts, ties on 11, and scores lower on 17.

## Gemini dimension means

| Dimension | Mean |
| --- | ---: |
| Spatial construction | 3.55 / 5 |
| Factual and semantic correctness | 3.00 / 5 |
| Required coverage | 4.15 / 5 |
| Cartographic legibility | 3.98 / 5 |

## Classification

| Band | Count |
| --- | ---: |
| Excellent | 6 |
| Good | 6 |
| Usable draft | 10 |
| Misleading | 13 |
| Substantive failure | 5 |
| Not usable | 0 |

## Gemini ranking

Ties use uncapped raw score and then item ID.

| Rank | ID | Final | Raw | Original | Subject |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | MB010 | 96 | 96 | 90.0 | Viking expansion from the eighth through eleventh centuries, showing settlement areas, major raiding and trade routes, and Atlantic exploration |
| 2 | MB002 | 95 | 95 | 95.0 | Ancient Egypt, showing Upper and Lower Egypt, the Nile, major settlements, and surrounding seas and deserts |
| 3 | MB003 | 95 | 95 | 97 | Classical Greece and the Aegean around the fifth century BCE, showing major regions, city-states, islands, and neighboring lands |
| 4 | MB007 | 95 | 95 | 59 | The Mauryan Empire under Ashoka around 250 BCE, showing its territorial extent, major cities, neighboring regions, and important geographic features |
| 5 | MB028 | 95 | 95 | 97.5 | The Indian Ocean trading world around 1450, showing the major commercial regions and ports, monsoon-driven sea routes, strategic straits, and connections among East Africa, the Middle East, South Asia, Southeast Asia, and China |
| 6 | MB008 | 92 | 92 | 59 | The Han dynasty around 60 BCE, showing its territory, commanderies or major regions, neighboring powers, the Great Wall, and major cities |
| 7 | MB014 | 87 | 87 | 59 | Central and southeastern Europe in 1683, showing the Ottoman Empire, its vassal states, the Habsburg lands, neighboring states, and major cities |
| 8 | MB001 | 84 | 84 | 74 | Eastern Mediterranean and Near East around 1200 BCE, showing the Late Bronze Age powers, Sea Peoples invasions and migrations, and major destroyed cities |
| 9 | MB013 | 83 | 83 | 74 | The spread of the Black Death across Europe and the Mediterranean from 1346 through 1353, showing chronological progression and principal land and maritime transmission routes |
| 10 | MB023 | 83 | 83 | 84 | The Byzantine-Sasanian War around 620 CE at the height of Sasanian expansion, showing effective control, the remaining Byzantine territories, major campaign areas, cities, and frontiers |
| 11 | MB035 | 83 | 83 | 96.0 | The Indian Rebellion of 1857-1858, showing British-controlled and princely territories, principal centers of rebellion, major campaign movements, cities, rivers, and regions that remained outside the main uprising |
| 12 | MB037 | 83 | 83 | 59 | The Russian Civil War around 1919, showing Bolshevik-controlled territory, the principal White fronts and other armed movements, foreign intervention zones, major cities, rail corridors, and campaign directions |
| 13 | MB017 | 74 | 82 | 59 | The Thirteen British Colonies around 1775, showing colonial boundaries, principal cities, neighboring British territories, Indigenous territory, Louisiana, and Spanish possessions |
| 14 | MB025 | 74 | 78 | 74 | East and Central Asia around 750 CE, showing the Tang dynasty, the principal neighboring states and steppe powers, frontier regions, major cities, and long-distance connections |
| 15 | MB032 | 74 | 78 | 74 | Europe immediately after the Peace of Westphalia in 1648, showing the principal states, the political fragmentation of the Holy Roman Empire, major territorial settlements, recognized independences, and important cities |
| 16 | MB006 | 74 | 77 | 97.5 | The major overland and maritime Silk Road routes connecting East Asia, Central Asia, India, the Middle East, East Africa, and Europe |
| 17 | MB011 | 74 | 77 | 59 | Europe and the Near East during the Crusades, 1095–1291, showing the principal Crusader states, neighboring powers, major cities, and expedition routes |
| 18 | MB021 | 74 | 77 | 74 | The Hellenistic world after the Battle of Ipsus around 300 BCE, showing the principal successor kingdoms, contested territories, major cities, and frontiers |
| 19 | MB024 | 74 | 77 | 39 | The Islamic world during the Abbasid Revolution around 750 CE, showing the collapsing Umayyad order, emerging Abbasid control, principal regions, campaign movement, major cities, and surviving rivals |
| 20 | MB016 | 74 | 75 | 74 | Major precolonial African kingdoms and civilizations roughly between 1000 and 1500 CE, showing their approximate extents, major cities, trade centers, and regional geography |
| 21 | MB022 | 74 | 74 | 59 | The Roman world during the Crisis of the Third Century around 271 CE, showing the central Roman Empire, major breakaway states, contested regions, frontiers, and principal cities |
| 22 | MB027 | 73 | 73 | 74 | Eurasia around 1330 after the fragmentation of the Mongol Empire, showing the principal successor khanates, their frontiers and overlaps, major cities, neighboring powers, and continental routes |
| 23 | MB029 | 59 | 70 | 59 | The Americas around 1491, showing the principal states and large cultural regions, major urban centers, exchange networks, and the geographic relationships among North America, Mesoamerica, the Caribbean, and South America |
| 24 | MB030 | 59 | 67 | 59 | West Africa around 1590 on the eve of the Moroccan invasion of Songhai, showing the principal states, trade cities and routes, the Niger system, Saharan connections, and the invasion corridor |
| 25 | MB038 | 59 | 65 | 98.0 | The partition of British India in 1947, showing the new international boundaries, the princely-state problem, principal migration flows, major affected regions and cities, and the geographic separation of Pakistan's two wings |
| 26 | MB005 | 59 | 64 | 100 | The Roman Empire at its greatest territorial extent around 117 CE, showing provinces, major cities, neighboring peoples, and frontiers |
| 27 | MB040 | 59 | 63 | 59 | The global Cold War around 1962, showing the major alliance systems, aligned and non-aligned states, divided countries, principal military flashpoints, and strategically important overseas positions |
| 28 | MB009 | 59 | 62 | 59 | The geographic extent of the Maya civilization during the Classic period, showing major regions, cities, lowlands, highlands, and surrounding seas |
| 29 | MB015 | 59 | 61 | 74 | The principal European voyages of exploration during the fifteenth and sixteenth centuries, including Columbus, da Gama, Cabot, and Magellan, with accurate routes and dates |
| 30 | MB026 | 59 | 61 | 74 | Maritime Southeast Asia around 900 CE, showing the principal states and cultural centers, major ports, strategic straits, regional seas, and important maritime connections |
| 31 | MB020 | 54 | 54 | 59 | A political and military map of Europe at the outbreak of World War I in 1914, showing national borders, alliance blocs, major cities, and the principal fronts |
| 32 | MB019 | 53 | 53 | 74 | Central Europe's railway network in 1866, showing major rail lines, junctions, cities, national boundaries, and surrounding seas |
| 33 | MB012 | 51 | 51 | 74 | The Mongol Empire at its greatest extent around 1279, showing the major khanates, important cities, neighboring states, and the principal continental extent |
| 34 | MB031 | 50 | 50 | 39 | The Ottoman, Safavid, and Mughal imperial worlds around 1600, showing their actual frontiers, major contested borderlands, neighboring powers, principal cities, and overland connections |
| 35 | MB034 | 47 | 47 | 96.0 | The Atlantic Revolutions from roughly 1775 to 1825, showing the principal revolutionary and independence movements, their chronology, major centers, imperial settings, and transatlantic connections |
| 36 | MB018 | 39 | 72 | 59 | Europe in 1811 at the height of Napoleon's power, showing the French Empire, directly controlled territories, satellite states, allies, and opposing powers |
| 37 | MB039 | 39 | 61 | 97.5 | The decolonization of Africa from 1957 to 1975, showing the chronology of independence, remaining colonial rule, major liberation-war regions, and the changing continental pattern |
| 38 | MB004 | 39 | 53 | 39 | The Persian Empire around 1730, showing its territorial extent, major internal regions, neighboring powers, cities, rivers, and seas |
| 39 | MB036 | 39 | 42 | 39 | Africa around 1885 at the beginning of the major European partition, distinguishing effective European control from claims or spheres, showing major independent African states, colonial footholds, and contested regions |
| 40 | MB033 | 35 | 35 | 59 | The global Seven Years' War from 1756 to 1763, showing the alliance system, principal theaters in Europe and overseas, major campaigns and naval connections, and the territories most directly contested |

## Largest exploratory score differences

| ID | Gemini | Original | Difference | Sol High judgment of Gemini map |
| --- | ---: | ---: | ---: | --- |
| MB039 | 39 | 97.5 | -58.5 | The continental pattern and liberation-war hatching are visible, but the requested independence chronology is systematically unreliable. |
| MB034 | 47 | 96.0 | -49 | The principal revolutions are named, but campaign geography, chronology, labels, and the French account contain several independent failures. |
| MB005 | 59 | 100 | -41 | The provincial atlas presentation is readable, but it misses Dacia and misclassifies Armenia at the very territorial maximum the prompt asks for. |
| MB038 | 59 | 98.0 | -39 | Borders, princely states, and the two separated regions are visible, but a wing is misidentified and the bidirectional migration legend does not decode the arrows. |
| MB007 | 95 | 59 | +36 | The Mauryan extent, capital, cities, neighboring powers, rivers, and unconquered southern regions form a complete and highly legible account. |
| MB024 | 74 | 39 | +35 | The revolutionary core and east-to-west campaign are clear, but the prompt's requested surviving rivals are not given a usable account. |
| MB008 | 92 | 59 | +33 | A coherent Western Han map with convincing territorial reach, commandery structure, neighbors, wall, cities, and Silk Road connection. |
| MB014 | 87 | 59 | +28 | The Ottoman core, vassals, Habsburg lands, neighboring states, cities, and terrain are clearly separated in a coherent 1683 frame. |
| MB033 | 35 | 59 | -24 | The map has attractive panels, but its European political frame is anachronistic, major names are corrupted, and the promised global theater coverage is incomplete. |
| MB037 | 83 | 59 | +24 | The Bolshevik core, principal White and other forces, interventions, cities, rail corridors, and offensive directions are all mapped coherently. |
| MB006 | 74 | 97.5 | -23.5 | A strong Eurasian route map with useful historical context, limited by omission of the requested East African maritime branch. |
| MB012 | 51 | 74 | -23 | The khanate labels are readable, but the Golden Horde's continental extent is grossly wrong and a key dated event is false. |

## Protocol and comparability

Each map was generated in a fresh `agy` conversation by Gemini 3.7 Flash High at high effort, using Antigravity's native `generate_image` tool backed by `gemini-3.1-flash-image`. Every item used one completed image-tool call, no reference image, and no corrective iteration. Sol High alone scored the forty resulting maps under the unchanged MECE v3 rubric without access to prior ratings.

The generation prompts and map subjects are identical across systems, but the evaluator topology differs: this Gemini run uses one Sol High judge, while the original canonical score used Sol/Terra scoring plus Sol High adjudication. Treat the score difference as a strong benchmark comparison, not a laboratory estimate of a pure model parameter effect. The tested Gemini system is an agent-plus-image-backend pipeline, not Gemini 3.7 Flash emitting pixels directly.
