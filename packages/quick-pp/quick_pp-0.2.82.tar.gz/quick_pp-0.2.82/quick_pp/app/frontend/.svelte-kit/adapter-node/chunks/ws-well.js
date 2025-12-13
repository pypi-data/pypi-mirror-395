import "clsx";
import { o as onDestroy, a4 as List_details, a5 as Wall, a6 as Text_wrap_disabled, a7 as Wash_temperature_6, a8 as Table } from "./vendor.js";
import { w as workspace } from "./workspace.js";
import { W as WsWellPlot } from "./WsWellPlot.js";
import "@sveltejs/kit/internal";
import "@sveltejs/kit/internal/server";
function Ws_well($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    const API_BASE = "http://localhost:6312";
    let selectedProject = null;
    let selectedWell = null;
    async function fetchProjectDetails(id) {
      try {
        if (!selectedProject || String(selectedProject.project_id) !== String(id)) {
          selectedProject = { project_id: id, name: selectedProject?.name };
        }
        const res = await fetch(`${API_BASE}/quick_pp/database/projects/${id}/wells`);
        if (res.ok) {
          const data = await res.json();
          selectedProject = { ...selectedProject, ...data || {} };
        }
      } catch (err) {
        console.warn("Failed to fetch project wells", err);
      } finally {
      }
    }
    const unsubscribe = workspace.subscribe((w) => {
      if (w && w.project && w.project.project_id) {
        selectedProject = { ...w.project };
        fetchProjectDetails(w.project.project_id);
      } else {
        selectedProject = null;
      }
      selectedWell = w?.selectedWell ?? null;
    });
    onDestroy(() => unsubscribe());
    $$renderer2.push(`<div class="project-workspace p-4">`);
    if (selectedProject) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="grid grid-cols-1 md:grid-cols-3 gap-4"><div class="col-span-1"><div class="bg-panel rounded p-4">`);
      if (selectedWell) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="mt-4"><div class="font-semibold">Well Workspace</div> <nav class="mt-2 flex flex-col gap-2"><button class="w-full text-left flex items-center gap-3 p-2 rounded hover:bg-muted/50 transition" aria-label="Overview"><span class="!size-5 text-muted-foreground">`);
        List_details($$renderer2, {});
        $$renderer2.push(`<!----></span> <span>Data Overview</span></button> <button class="w-full text-left flex items-center gap-3 p-2 rounded hover:bg-muted/50 transition" aria-label="Lithology and porosity"><span class="!size-5 text-muted-foreground">`);
        Wall($$renderer2, {});
        $$renderer2.push(`<!----></span> <span>Lithology &amp; Porosity</span></button> <button class="w-full text-left flex items-center gap-3 p-2 rounded hover:bg-muted/50 transition" aria-label="Permeability"><span class="!size-5 text-muted-foreground">`);
        Text_wrap_disabled($$renderer2, {});
        $$renderer2.push(`<!----></span> <span>Permeability</span></button> <button class="w-full text-left flex items-center gap-3 p-2 rounded hover:bg-muted/50 transition" aria-label="Saturation"><span class="!size-5 text-muted-foreground">`);
        Wash_temperature_6($$renderer2, {});
        $$renderer2.push(`<!----></span> <span>Saturation</span></button> <button class="w-full text-left flex items-center gap-3 p-2 rounded hover:bg-muted/50 transition" aria-label="Reservoir summary"><span class="!size-5 text-muted-foreground">`);
        Table($$renderer2, {});
        $$renderer2.push(`<!----></span> <span>Reservoir Summary</span></button></nav></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--></div></div> <div class="col-span-2"><div class="bg-panel rounded p-4 min-h-[300px]">`);
      if (selectedWell) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="mt-3">`);
        WsWellPlot($$renderer2, {
          projectId: selectedProject.project_id,
          wellName: selectedWell.name
        });
        $$renderer2.push(`<!----></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
        $$renderer2.push(`<div class="text-center py-12"><div class="font-semibold">No well selected</div> <div class="text-sm text-muted-foreground mt-2">Select a well on the left to view its logs and analysis.</div> <div class="mt-4"><button class="btn btn-primary">Open Projects</button></div></div>`);
      }
      $$renderer2.push(`<!--]--></div></div></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      $$renderer2.push(`<div class="bg-panel rounded p-6 text-center"><div class="font-semibold">No project selected</div> <div class="text-sm text-muted-foreground mt-2">Select a project in the Projects workspace to begin well analysis.</div> <div class="mt-4"><button class="btn btn-primary">Open Projects</button></div></div>`);
    }
    $$renderer2.push(`<!--]--></div>`);
  });
}
export {
  Ws_well as W
};
