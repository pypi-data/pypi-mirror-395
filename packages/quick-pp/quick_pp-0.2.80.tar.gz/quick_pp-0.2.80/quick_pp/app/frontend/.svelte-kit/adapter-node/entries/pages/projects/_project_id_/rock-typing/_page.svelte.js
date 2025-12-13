import "clsx";
import { a as attr, c as bind_props } from "../../../../../chunks/index2.js";
import "../../../../../chunks/button.js";
import { D as DepthFilterStatus } from "../../../../../chunks/DepthFilterStatus.js";
import { o as onDestroy } from "../../../../../chunks/index-server.js";
import { w as workspace } from "../../../../../chunks/workspace.js";
import { f as fallback } from "../../../../../chunks/context.js";
import { P as ProjectWorkspace } from "../../../../../chunks/ProjectWorkspace.js";
function WsRockTyping($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = fallback($$props["projectId"], null);
    const unsubscribe = workspace.subscribe((w) => {
      if (w?.zoneFilter) {
        ({ ...w.zoneFilter });
      }
    });
    onDestroy(() => unsubscribe());
    let cutoffsInput = "0.1, 1.0, 3.0, 6.0";
    $$renderer2.push(`<div class="ws-rock-typing"><div class="mb-2"><div class="font-semibold">Rock Typing (Multi-Well)</div> <div class="text-sm text-muted-foreground">Cluster wells into rock types across the project.</div></div> `);
    DepthFilterStatus($$renderer2);
    $$renderer2.push(`<!----> <div class="bg-panel rounded p-3 mb-3"><div class="flex-1"><label for="cutoffs" class="block text-sm font-medium mb-1">FZI Cutoffs (comma-separated)</label> <input id="cutoffs" type="text"${attr("value", cutoffsInput)} class="w-full px-3 py-2 border border-border rounded-md bg-background text-foreground" placeholder="e.g., 0.5,1.0,2.0"/></div> <div class="font-semibold mb-2">FZI Log-Log Plot</div> <div class="text-sm text-muted-foreground mb-3">Plot Flow Zone Indicator (FZI) from porosity and permeability data across all wells.</div> `);
    {
      $$renderer2.push("<!--[!-->");
      {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--> <div class="bg-surface rounded p-3 min-h-[400px]"><div class="w-full max-w-[600px] h-[500px] mx-auto"></div></div> <div class="font-semibold mb-2">Pore-Perm Crossplot</div> <div class="text-sm text-muted-foreground mb-3">Plot porosity vs permeability with FZI cutoff lines and rock type coloring.</div> <div class="bg-surface rounded p-3 min-h-[400px]"><div class="w-full max-w-[600px] h-[500px] mx-auto"></div></div></div></div>`);
    bind_props($$props, { projectId });
  });
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let selectedProject = null;
    const unsubscribe = workspace.subscribe((w) => {
      selectedProject = w?.project ?? null;
    });
    onDestroy(() => unsubscribe());
    ProjectWorkspace($$renderer2, {
      project: selectedProject,
      $$slots: {
        left: ($$renderer3) => {
          $$renderer3.push(`<div slot="left">`);
          WsRockTyping($$renderer3, { projectId: selectedProject?.project_id ?? null });
          $$renderer3.push(`<!----></div>`);
        }
      }
    });
  });
}
export {
  _page as default
};
