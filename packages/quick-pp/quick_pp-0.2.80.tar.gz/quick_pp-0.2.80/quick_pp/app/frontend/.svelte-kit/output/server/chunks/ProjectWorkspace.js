import { b as slot, c as bind_props } from "./index2.js";
import { f as fallback } from "./context.js";
import "@sveltejs/kit/internal";
import "./exports.js";
import "./utils.js";
import "clsx";
import "@sveltejs/kit/internal/server";
import "./state.svelte.js";
import { W as WsWellPlot } from "./WsWellPlot.js";
function ProjectWorkspace($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let project = fallback($$props["project"], null);
    let selectedWell = fallback($$props["selectedWell"], null);
    if (project) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="grid grid-cols-1 md:grid-cols-2 gap-4"><div class="col-span-1"><div class="bg-panel rounded p-4"><!--[-->`);
      slot($$renderer2, $$props, "left", {});
      $$renderer2.push(`<!--]--></div></div> <div class="col-span-1">`);
      if (selectedWell) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="bg-panel rounded p-4 min-h-[300px]">`);
        WsWellPlot($$renderer2, {
          projectId: project?.project_id ?? "",
          wellName: selectedWell.name ?? ""
        });
        $$renderer2.push(`<!----></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
        $$renderer2.push(`<div class="bg-panel rounded p-4 min-h-[300px]"><div class="text-center py-12"><div class="font-semibold">No well selected</div> <div class="text-sm text-muted-foreground mt-2">Select a well to view its logs and analysis.</div></div></div>`);
      }
      $$renderer2.push(`<!--]--></div></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      $$renderer2.push(`<div class="bg-panel rounded p-6 text-center"><div class="font-semibold">No project selected</div> <div class="text-sm text-muted mt-2">Select a project in the Projects workspace to begin.</div> <div class="mt-4"><button class="btn btn-primary">Open Projects</button></div></div>`);
    }
    $$renderer2.push(`<!--]-->`);
    bind_props($$props, { project, selectedWell });
  });
}
export {
  ProjectWorkspace as P
};
