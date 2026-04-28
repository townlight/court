"""HTML landing surface for the CivicCourt runtime."""


def render_public_lookup_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CivicCourt v0.1.0</title>
  <style>
    :root{--ink:#211b1b;--muted:#655858;--line:#dec3bd;--card:#fff8f4;--accent:#8a3b2f;--bg:#fff1ec}
    body{margin:0;font-family:Aptos,Segoe UI,sans-serif;background:radial-gradient(circle at 10% 10%,#ffe1d8,var(--bg) 38%,#f8f1ff);color:var(--ink)}
    main{width:min(1080px,calc(100% - 32px));margin:auto;padding:52px 0}
    h1{font:800 clamp(2.3rem,7vw,5rem)/.95 Georgia,serif;margin:.2em 0}
    .eyebrow{font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
    .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin-top:28px}
    .card{background:rgba(255,248,244,.94);border:1px solid var(--line);border-radius:24px;padding:24px;box-shadow:0 18px 50px rgba(85,36,30,.10)}
    code{background:#f7ded7;padding:.14rem .36rem;border-radius:.5rem}
    a{color:var(--accent);font-weight:700}
    @media(max-width:800px){.grid{grid-template-columns:1fr}main{padding:34px 0}}
  </style>
</head>
<body>
<main>
  <p class="eyebrow">CivicSuite / CivicCourt</p>
  <h1>Court clerk support with sealed-record boundaries.</h1>
  <p>CivicCourt v0.1.0 helps court clerks draft forms, answer procedure questions with citations, search public sample records, and prepare hearing checklists.</p>
  <section class="grid">
    <article class="card"><h2>Ships Today</h2><p>Procedure Q&A, form drafts, restricted-record-aware search, hearing prep, and deterministic API endpoints.</p></article>
    <article class="card"><h2>Clerk Review</h2><p>Court clerks verify every draft, citation, form, and hearing checklist before use.</p></article>
    <article class="card"><h2>Boundary</h2><p>No court CMS replacement, e-filing, warrant issuance, judicial decisions, legal advice, live LLM calls, or court connector runtime ships in v0.1.0.</p></article>
  </section>
  <section class="card" style="margin-top:24px">
    <h2>Architecture</h2>
    <p><strong>Clerk request</strong> → CivicCourt deterministic API → CivicCore foundation. Court CMS integrations are future isolated read-only adapters, not v0.1.0 write paths.</p>
  </section>
  <p>Dependency: <code>civiccore==0.2.0</code>. Repo: <a href="https://github.com/CivicSuite/civiccourt">CivicSuite/civiccourt</a>.</p>
</main>
</body>
</html>
"""
