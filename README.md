⚙️ Setup
Install python version 3.11 and add path in environment variable.
pip install -r requirements.txt

📊 Run the app
Go to root folder Run "streamlit run app.py"

🔎 Project description

Purpose: Automated RFP analysis tool that inspects a website (URL index / sitemap) and produces a structured RFP-ready output focused on page types, exhaustive UX-led component identification, and third‑party integration detection.
Role: Acts as a SENIOR CMS SOLUTION ARCHITECT + UX designer to infer page taxonomy, visual/content components (atomic and composite, unbounded), and integration surface from crawl data and page context.
Key outputs:
Strict JSON analysis (overview, page_types, components, pages, third_party_integrations, recommendations).
Excel export with sheets:
Page Types (includes new "component" and "components_reusable" columns listing all components per page type and reusable subset).
Components (per-component metadata and "reusable" flag).
Component-Page Mapping (one row per component × page URL with reusable flag and page_type).
Per-page entries for every URL in the index (no omissions), plus aggregated summaries.
Component identification approach:
UX‑led, unbounded: infer components from layout, IA, headers, repeated patterns, media and content structure; include variants and both atomic/composite components.
Mark components as reusable when observed across multiple page types; map components into Page Types sheet.
Third‑party detection:
Open‑ended analysis (no predefined whitelist) that infers integrations from script/iframe/link sources, API/form endpoints, embeds, CDN domains, tag managers, widgets, etc., with evidence and detected URLs.
Architecture / tech notes:
Core analysis logic lives in ai_service.py (prompt-driven generation + post‑processing).
Frontend/UX: Streamlit app (app.py) to run analysis and export Excel.
Environment: requires OPENAI_API_KEY; Excel output built from aggregated pages/components data.
Intended users: solution architects, UX teams, CMS migration planners, RFP authors.
