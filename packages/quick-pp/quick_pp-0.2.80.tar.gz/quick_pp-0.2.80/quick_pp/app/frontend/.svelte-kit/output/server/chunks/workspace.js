import { w as writable, g as get } from "./index.js";
const projects = writable([]);
const workspace = writable({
  title: "QPP - Petrophysical Analysis",
  subtitle: void 0,
  project: null,
  depthFilter: {
    enabled: false,
    minDepth: null,
    maxDepth: null
  },
  zoneFilter: {
    enabled: false,
    zones: []
  }
});
function selectProject(project) {
  workspace.update((s) => {
    const curId = s.project && s.project.project_id != null ? String(s.project.project_id) : null;
    const newId = project && project.project_id != null ? String(project.project_id) : null;
    const curName = s.project && s.project.name ? s.project.name : null;
    let incomingName = null;
    if (project && project.name) incomingName = project.name;
    else if (project && project.project_id) {
      try {
        const list = get(projects) || [];
        const found = list.find((p) => String(p.project_id) === String(project.project_id));
        if (found && found.name) incomingName = found.name;
      } catch (e) {
      }
    }
    const newName = incomingName;
    if (curId === newId && curName === newName) return s;
    const projToSet = project ? { ...project, ...newName ? { name: newName } : {} } : null;
    return { ...s, project: projToSet, title: projToSet ? projToSet.name ?? "QPP - Petrophysical Analysis" : "QPP - Petrophysical Analysis" };
  });
}
function selectWell(well) {
  workspace.update((s) => ({ ...s, selectedWell: well }));
}
function applyDepthFilter(rows, depthFilter) {
  if (!depthFilter?.enabled || !depthFilter.minDepth && !depthFilter.maxDepth) {
    return rows;
  }
  return rows.filter((row) => {
    const depth = Number(row.depth ?? row.DEPTH ?? row.Depth ?? NaN);
    if (isNaN(depth)) return false;
    if (depthFilter.minDepth !== null && depth < depthFilter.minDepth) return false;
    if (depthFilter.maxDepth !== null && depth > depthFilter.maxDepth) return false;
    return true;
  });
}
function extractZoneValue(row) {
  if (!row || typeof row !== "object") return null;
  const candidates = ["name", "zone", "Zone", "ZONE", "formation", "formation_name", "formationName", "FORMATION", "formation_top", "formationTop"];
  for (const k of candidates) {
    if (k in row && row[k] !== null && row[k] !== void 0 && String(row[k]).trim() !== "") {
      return String(row[k]);
    }
  }
  for (const k of Object.keys(row)) {
    if (/zone|formation/i.test(k) && row[k] !== null && row[k] !== void 0 && String(row[k]).trim() !== "") {
      return String(row[k]);
    }
  }
  return null;
}
function applyZoneFilter(rows, zoneFilter) {
  if (!zoneFilter?.enabled || !zoneFilter.zones || zoneFilter.zones.length === 0) return rows;
  const allowed = new Set(zoneFilter.zones.map((z) => String(z)));
  return rows.filter((row) => {
    const val = extractZoneValue(row);
    if (val === null) return false;
    return allowed.has(val);
  });
}
export {
  selectWell as a,
  applyDepthFilter as b,
  applyZoneFilter as c,
  projects as p,
  selectProject as s,
  workspace as w
};
