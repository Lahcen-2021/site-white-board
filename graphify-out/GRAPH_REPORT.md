# Graph Report - feltboard-site  (2026-11-24)

## Corpus Check
- 51 files · ~59,164 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 343 nodes · 582 edges · 12 communities
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 86 edges (avg confidence: 0.84)
- Token cost: 312,463 input · 0 output

## Community Hubs (Navigation)
- Whiteboard Canvas Engine
- Brainstorming and Recall Methods
- Competitor Tool Landscape
- Static Site Generator
- Local-First Trade-offs
- Kanban and Retrospectives
- Teaching and Tutoring Practice
- Hardware and Display Setups
- French Teaching Content
- App Shell and Brand Identity
- Marketing Page Scripts
- PNG Export and Sharing

## God Nodes (most connected - your core abstractions)
1. `dirty()` - 18 edges
2. `endPointer()` - 14 edges
3. `main()` - 13 edges
4. `head()` - 12 edges
5. `get()` - 12 edges
6. `ui()` - 12 edges
7. `10 creative ways to use a whiteboard for brainstorming` - 12 edges
8. `closeEditor()` - 11 edges
9. `blog_url()` - 10 edges
10. `foot()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Undo makes children braver` --references--> `Whiteboard app shell (app.html)`  [INFERRED]
  content/blog/en/whiteboard-for-kids-activities.md → src/app.html
- `Spaced repetition with saved boards` --references--> `Pro plan`  [INFERRED]
  content/blog/en/study-techniques-whiteboard.md → README.md
- `Boards popover (new, save, backup, restore)` --references--> `Pro plan`  [INFERRED]
  src/app.html → README.md
- `Whiteboard app shell (app.html)` --references--> `Brand blue #1f5fd1`  [INFERRED]
  src/app.html → src/icon.svg
- `Standard flowchart symbols (ellipse, rectangle, diamond, arrow)` --shares_data_with--> `Tool palette (select, hand, pen, eraser, sticky, text, shape, arrow)`  [INFERRED]
  content/blog/en/how-to-draw-a-flowchart-online.md → src/app.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **No-backend, local-first design and its trade-offs** — readme_no_backend_architecture, content_blog_en_sitewhiteboard_vs_miro_vs_mural_local_storage_privacy, content_blog_en_sitewhiteboard_vs_miro_vs_mural_no_live_collaboration, readme_licence_key_validation, content_blog_en_how_to_use_online_whiteboard_for_teaching_browser_storage_risk, content_blog_en_whiteboard_for_kids_activities_child_safety_privacy [INFERRED 0.85]
- **Sticky-note divergent-then-convergent facilitation flow** — content_blog_en_creative_whiteboard_brainstorming_ideas_silent_storm, content_blog_en_creative_whiteboard_brainstorming_ideas_affinity_grouping, content_blog_en_sticky_notes_retrospective_affinity_mapping_affinity_mapping, content_blog_en_sticky_notes_retrospective_affinity_mapping_dot_voting, content_blog_en_creative_whiteboard_brainstorming_ideas_two_by_two_matrix, content_blog_en_creative_whiteboard_brainstorming_ideas_separate_generating_from_judging [INFERRED 0.85]
- **Teaching on a big screen: pen input, write big, move don't erase, export** — content_blog_en_interactive_whiteboard_classroom_projector_tv_three_parts, content_blog_en_teach_math_with_online_whiteboard_pen_input, content_blog_en_interactive_whiteboard_classroom_projector_tv_high_contrast_colours, content_blog_en_how_to_use_online_whiteboard_for_teaching_move_dont_erase, content_blog_en_what_is_a_digital_whiteboard_png_export, content_blog_en_whiteboard_on_screen_video_calls_thick_bright_for_compression [INFERRED 0.85]
- **Enseignement au tableau blanc (classe, maths, cours particuliers, affichage)** — content_blog_fr_tableau_blanc_en_ligne_pour_enseigner_enseigner_au_tableau_blanc, content_blog_fr_enseigner_les_maths_tableau_blanc_en_ligne_enseigner_les_maths, content_blog_fr_tableau_blanc_en_ligne_pour_cours_particuliers_cours_particuliers, content_blog_fr_tableau_interactif_videoprojecteur_tv_classe_tableau_interactif_improvise [INFERRED 0.85]
- **Flux post-it : produire puis organiser les idées** — content_blog_fr_idees_creatives_remue_meninges_tableau_blanc_tempete_silencieuse, content_blog_fr_idees_creatives_remue_meninges_tableau_blanc_regroupement_affinites, content_blog_fr_post_it_retrospective_carte_affinites_carte_affinites, content_blog_fr_tableau_kanban_planification_projet_tableau_kanban [INFERRED 0.75]
- **Paysage des outils de tableau blanc comparés** — content_blog_fr_meilleurs_tableaux_blancs_en_ligne_gratuits_2026_excalidraw, content_blog_fr_meilleurs_tableaux_blancs_en_ligne_gratuits_2026_tldraw, content_blog_fr_meilleurs_tableaux_blancs_en_ligne_gratuits_2026_google_jamboard, content_blog_fr_tableau_blanc_vs_miro_vs_mural_miro, content_blog_fr_tableau_blanc_vs_miro_vs_mural_mural, content_blog_fr_meilleurs_tableaux_blancs_en_ligne_gratuits_2026_sitewhiteboard [INFERRED 0.85]
- **مجموعة التدريس بالسبورة الأونلاين** — content_blog_ar_sabbora_bayda_online_lil_tadris_teaching_whiteboard, content_blog_ar_tadris_riyadiyat_sabbora_online_teach_math, content_blog_ar_sabbora_online_lil_dourous_alkhousousiya_tutoring_whiteboard, content_blog_ar_sabbora_tafaouliya_jihaz_ard_tv_qism_interactive_whiteboard [INFERRED 0.85]
- **مسار العمل بالأوراق اللاصقة: كتابة صامتة ثم تجميع ثم ترتيب** — content_blog_ar_afkar_asf_dihni_sabbora_silent_sticky_storm, content_blog_ar_afkar_asf_dihni_sabbora_affinity_grouping, content_blog_ar_awraq_lasiqa_murajaa_tajmi_taqarub_team_retrospective, content_blog_ar_lawhat_kanban_takhtit_almashari_three_columns [INFERRED 0.85]
- **اختيار أداة السبورة: الأنواع والمقارنات** — content_blog_ar_ma_hiya_sabbora_raqmiya_digital_whiteboard, content_blog_ar_afdal_sabbora_bayda_majjania_2026_free_whiteboard_tools_comparison, content_blog_ar_sabbora_online_vs_miro_vs_mural_comparison [INFERRED 0.85]

## Communities (12 total, 0 thin omitted)

### Community 0 - "Whiteboard Canvas Engine"
Cohesion: 0.07
Nodes (67): addItems(), applyLang(), applyMap(), bbox(), cancelGesture(), clean(), clip(), closeEditor() (+59 more)

### Community 1 - "Brainstorming and Recall Methods"
Cohesion: 0.06
Nodes (45): التجميع حسب التقارب, 10 طرق إبداعية لاستعمال السبورة في العصف الذهني, الثمانيات السريعة, العاصفة الصامتة بالأوراق اللاصقة, اللوحة اللانهائية, كيف ترسم خريطة ذهنية أونلاين, الأسهم اللاصقة بالأشكال, كيف ترسم مخططًا انسيابيًا أونلاين (+37 more)

### Community 2 - "Competitor Tool Landscape"
Cohesion: 0.05
Nodes (43): أفضل السبورات البيضاء الأونلاين المجانية في 2026, الإفصاح عن تطوير SiteWhiteboard في المقارنة, إغلاق Google Jamboard, بدون حساب ولا تثبيت, سبورة للأطفال: 12 نشاطًا, السبورة البيضاء الأونلاين وMiro وMural, اللوحات تبقى على جهازك, السبورة البسيطة مقابل منصة التعاون (+35 more)

### Community 3 - "Static Site Generator"
Cohesion: 0.18
Nodes (31): about(), ad(), blog_index(), blog_post(), blog_url(), board(), contact(), doc() (+23 more)

### Community 4 - "Local-First Trade-offs"
Cohesion: 0.07
Nodes (30): How to use an online whiteboard for teaching, Browser storage loss risk on shared school computers, 45 minute lesson board layout, Move, don't erase, Saved project file as a lesson template, When to move to Trello or Jira, Share only the whiteboard window, Boards stored in your browser, not the cloud (+22 more)

### Community 5 - "Kanban and Retrospectives"
Cohesion: 0.09
Nodes (26): خريطة التقارب, الورقة اللاصقة تفرض الاختصار, الأوراق اللاصقة: جلسة مراجعة أو خريطة تقارب, جلسة مراجعة الفريق, لوحة كانبان لتخطيط المشاريع, الأعمدة الثلاثة: للعمل، جارٍ، منتهٍ, Plan a project on a whiteboard with a kanban board, Blocked area (+18 more)

### Community 6 - "Teaching and Tutoring Practice"
Cohesion: 0.08
Nodes (26): تحضير اللوحة قبل الحصة, الكتابة بالقلم بدل الفأرة, السبورة البيضاء الأونلاين في التدريس, مشاركة الشاشة, سبورة مستقلة بدل السبورة المدمجة, السبورة في Zoom وGoogle Meet وTeams, اللوحة كورقة مشتركة بين المدرّس والتلميذ, سبورة أونلاين للدروس الخصوصية (+18 more)

### Community 7 - "Hardware and Display Setups"
Cohesion: 0.10
Nodes (21): ما هي السبورة البيضاء الرقمية؟, الشاشات التفاعلية, السبورات الأونلاين, تطبيقات السبورة, حوّل جهاز العرض أو التلفاز إلى سبورة تفاعلية, الفائدة من البرنامج لا من العتاد, Turn any projector or TV into an interactive whiteboard, USB drawing tablet pen input (+13 more)

### Community 8 - "French Teaching Content"
Cohesion: 0.11
Nodes (20): Carte mentale, Export PNG et sauvegarde navigateur, Toile infinie (surface sans fin), Enseigner les maths au tableau blanc en ligne, Fond quadrillé (grille), Saisie au stylet, Une étape par ligne, Tableau blanc pour cours particuliers (+12 more)

### Community 9 - "App Shell and Brand Identity"
Cohesion: 0.18
Nodes (13): Separate generating from judging, Standard flowchart symbols (ellipse, rectangle, diamond, arrow), Sticky notes force brevity and separate producing from organising, HTML canvas object model (strokes smoothed, objects selectable), Online whiteboard, Sticky note, Whiteboard app shell (app.html), Bricolage Grotesque / Readex Pro / Shantell Sans brand fonts (+5 more)

### Community 10 - "Marketing Page Scripts"
Cohesion: 0.39
Nodes (5): col(), draw(), path(), size(), up()

### Community 11 - "PNG Export and Sharing"
Cohesion: 0.67
Nodes (3): Exported board as a record for students and parents, PNG export of a board, Share/export popover

## Knowledge Gaps
- **42 isolated node(s):** `Canonical, hreflang, sitemap and robots.txt`, `Share/export popover`, `Styles island (thickness, colours, swatches)`, `Grid toggle`, `Bricolage Grotesque / Readex Pro / Shantell Sans brand fonts` (+37 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Use a whiteboard on screen in Zoom, Google Meet and Teams` connect `Competitor Tool Landscape` to `Brainstorming and Recall Methods`, `Local-First Trade-offs`, `Kanban and Retrospectives`, `Teaching and Tutoring Practice`, `French Teaching Content`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Why does `What is a digital whiteboard?` connect `Hardware and Display Setups` to `App Shell and Brand Identity`, `Local-First Trade-offs`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `Arrows that stay attached to shapes` connect `Brainstorming and Recall Methods` to `App Shell and Brand Identity`, `Competitor Tool Landscape`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **What connects `Canonical, hreflang, sitemap and robots.txt`, `Share/export popover`, `Styles island (thickness, colours, swatches)` to the rest of the system?**
  _42 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Whiteboard Canvas Engine` be split into smaller, more focused modules?**
  _Cohesion score 0.07052631578947369 - nodes in this community are weakly interconnected._
- **Should `Brainstorming and Recall Methods` be split into smaller, more focused modules?**
  _Cohesion score 0.05656565656565657 - nodes in this community are weakly interconnected._
- **Should `Competitor Tool Landscape` be split into smaller, more focused modules?**
  _Cohesion score 0.05204872646733112 - nodes in this community are weakly interconnected._