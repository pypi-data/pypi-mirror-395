import "clsx";
import { a as attr, c as bind_props } from "../../../../../chunks/index2.js";
import { B as Button } from "../../../../../chunks/button.js";
import { D as DepthFilterStatus } from "../../../../../chunks/DepthFilterStatus.js";
import { S as escape_html } from "../../../../../chunks/utils2.js";
import { P as ProjectWorkspace } from "../../../../../chunks/ProjectWorkspace.js";
import { o as onDestroy } from "../../../../../chunks/index-server.js";
import { w as workspace } from "../../../../../chunks/workspace.js";
function WsShf($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    const projectId = null;
    let loading = false;
    let message = null;
    let entryHeight = 0.5;
    async function computeShf() {
      loading = true;
      message = null;
      try {
        await new Promise((r) => setTimeout(r, 600));
        message = "SHF computation finished (preview).";
      } catch (e) {
        message = "Failed to compute SHF.";
      } finally {
        loading = false;
      }
    }
    $$renderer2.push(`<div class="ws-shf"><div class="mb-2"><div class="font-semibold">Saturation Height Function (Multi-Well)</div> <div class="text-sm text-muted-foreground">Estimate SHF parameters across multiple wells for the project.</div></div> `);
    DepthFilterStatus($$renderer2);
    $$renderer2.push(`<!----> <div class="bg-panel rounded p-3"><div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3"><div><label for="entryHeight" class="text-sm">Entry Height (m)</label> <input id="entryHeight" type="number" step="0.01"${attr("value", entryHeight)} class="input mt-1"/></div> <div class="col-span-2 flex items-end">`);
    Button($$renderer2, {
      class: "btn btn-primary",
      onclick: computeShf,
      disabled: loading,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->${escape_html(loading ? "Computing…" : "Compute SHF")}`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    Button($$renderer2, {
      class: "btn ml-2",
      onclick: () => {
      },
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Export SHF`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----></div></div> `);
    if (message) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="text-sm text-muted-foreground mb-3">${escape_html(message)}</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--> <div class="grid grid-cols-1 md:grid-cols-2 gap-3"><div class="bg-surface rounded p-3 min-h-[220px]"><div class="font-medium mb-2">SHF Plot</div> <div class="text-sm text-muted-foreground">Placeholder for SHF curves across wells.</div> <div class="mt-4 h-[140px] bg-white/5 rounded border border-border/30"></div></div> <div class="bg-surface rounded p-3 min-h-[220px]"><div class="font-medium mb-2">Parameter Summary</div> <div class="text-sm text-muted-foreground">Table of derived parameters and fit statistics.</div> <div class="mt-4 h-[140px] bg-white/5 rounded border border-border/30"></div></div></div></div></div>`);
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
          WsShf($$renderer3, { projectId: selectedProject?.project_id ?? null });
          $$renderer3.push(`<!----></div>`);
        }
      }
    });
  });
}
export {
  _page as default
};
