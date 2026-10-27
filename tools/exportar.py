"""Convierte la exportación de la base del radar (ArtifactData con out_dir) en los archivos data/*.json de la página pública.
Uso: python3 tools/exportar.py <carpeta_exportada> <carpeta_del_repositorio>
Nunca borra reportes: une lo exportado con lo que ya está publicado."""
import json, glob, os, sys
src, repo = sys.argv[1], sys.argv[2]
data = os.path.join(repo, "data"); os.makedirs(data, exist_ok=True)
path = os.path.join(data, "reports.json")
prev = {r["id"]: r for r in json.load(open(path))} if os.path.exists(path) else {}
for f in glob.glob(os.path.join(src, "reports", "*.json")):
    d = json.load(open(f)); d["id"] = os.path.basename(f)[:-5]; prev[d["id"]] = d
reps = sorted(prev.values(), key=lambda r: r.get("generatedAt", ""), reverse=True)
json.dump(reps, open(path, "w"), ensure_ascii=False)
for name, rel in [("search.json", "settings/search.json"), ("lastRun.json", "status/lastRun.json"), ("general.json", "settings/general.json")]:
    p = os.path.join(src, rel)
    if os.path.exists(p): json.dump(json.load(open(p)), open(os.path.join(data, name), "w"), ensure_ascii=False)
print(len(reps), "reportes publicados")
