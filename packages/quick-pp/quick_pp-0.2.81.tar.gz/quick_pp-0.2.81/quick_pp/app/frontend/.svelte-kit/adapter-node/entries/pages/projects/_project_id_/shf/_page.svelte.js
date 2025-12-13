import "clsx";
import { aj as fallback, o as onDestroy, a as attr, c as bind_props, C as attr_class, t as escape_html, i as stringify, F as ensure_array_like } from "../../../../../chunks/vendor.js";
import { B as Button } from "../../../../../chunks/button.js";
import { D as DepthFilterStatus } from "../../../../../chunks/DepthFilterStatus.js";
import { w as workspace, b as applyZoneFilter } from "../../../../../chunks/workspace.js";
import { P as ProjectWorkspace } from "../../../../../chunks/ProjectWorkspace.js";
function WsShf($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = fallback($$props["projectId"], null);
    let loading = false;
    let message = null;
    let dataLoading = false;
    let dataError = null;
    let wellData = null;
    let data = null;
    let fits = null;
    let shfData = null;
    let fwl = 1e4;
    let ift = 30;
    let theta = 30;
    let gw = 1.05;
    let ghc = 0.8;
    let cutoffsInput = "0.1, 1.0, 3.0, 6.0, 8.0";
    let zoneFilter = { enabled: false, zones: [] };
    const unsubscribe = workspace.subscribe((w) => {
      if (w?.zoneFilter && (zoneFilter.enabled !== w.zoneFilter.enabled || JSON.stringify(zoneFilter.zones) !== JSON.stringify(w.zoneFilter.zones))) {
        zoneFilter = { ...w.zoneFilter };
      }
    });
    onDestroy(() => unsubscribe());
    const API_BASE = "http://localhost:6312";
    function getFilteredData() {
      if (!wellData) return null;
      const rows = wellData.phit.map((phit, i) => ({
        phit,
        perm: wellData.perm[i],
        zone: wellData.zones[i],
        rock_flag: wellData.rock_flags[i],
        well_name: wellData.well_names[i],
        depth: wellData.depths[i]
      }));
      const visibleRows = applyZoneFilter(rows, zoneFilter);
      return {
        phit: visibleRows.map((r) => r.phit),
        perm: visibleRows.map((r) => r.perm),
        zones: visibleRows.map((r) => r.zone),
        rock_flags: visibleRows.map((r) => r.rock_flag),
        well_names: visibleRows.map((r) => r.well_name),
        depths: visibleRows.map((r) => r.depth)
      };
    }
    async function loadData() {
      if (!projectId) return;
      dataLoading = true;
      dataError = null;
      try {
        const wellUrl = `${API_BASE}/quick_pp/database/projects/${projectId}/fzi_data`;
        const wellRes = await fetch(wellUrl);
        if (!wellRes.ok) throw new Error(await wellRes.text());
        wellData = await wellRes.json();
        const url = `${API_BASE}/quick_pp/database/projects/${projectId}/j_data?cutoffs=${encodeURIComponent(cutoffsInput)}`;
        const res = await fetch(url);
        if (!res.ok) throw new Error(await res.text());
        data = await res.json();
      } catch (e) {
        dataError = e.message || "Failed to load data";
        data = null;
        fits = null;
      } finally {
        dataLoading = false;
      }
    }
    async function computeFits() {
      if (!data || !projectId) return;
      loading = true;
      message = null;
      try {
        if (!data) return;
        const url = `${API_BASE}/quick_pp/database/projects/${projectId}/compute_j_fits`;
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ data, ift, theta })
        });
        if (!res.ok) throw new Error(await res.text());
        fits = await res.json();
        message = "J fits computed";
      } catch (e) {
        message = `Error: ${e.message}`;
      } finally {
        loading = false;
      }
    }
    async function computeShf() {
      if (!data || !fits || !projectId) return;
      loading = true;
      message = null;
      try {
        const filteredData = getFilteredData();
        if (!filteredData) return;
        const url = `${API_BASE}/quick_pp/database/projects/${projectId}/compute_shf`;
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ data: filteredData, fits, fwl, ift, theta, gw, ghc })
        });
        if (!res.ok) throw new Error(await res.text());
        const result = await res.json();
        shfData = result.shf_data;
        message = "SHF computed";
      } catch (e) {
        message = `Error: ${e.message}`;
      } finally {
        loading = false;
      }
    }
    async function saveShf() {
      if (!shfData || !projectId) return;
      loading = true;
      message = null;
      try {
        const url = `${API_BASE}/quick_pp/database/projects/${projectId}/save_shf`;
        const res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ shf_data: shfData })
        });
        if (!res.ok) throw new Error(await res.text());
        message = "SHF saved";
      } catch (e) {
        message = `Error: ${e.message}`;
      } finally {
        loading = false;
      }
    }
    if (projectId && cutoffsInput) {
      loadData();
    }
    $$renderer2.push(`<div class="ws-shf"><div class="mb-2"><div class="font-semibold">Saturation Height Function (Multi-Well)</div> <div class="text-sm text-muted-foreground">Estimate SHF parameters across multiple wells for the project.</div></div> `);
    DepthFilterStatus($$renderer2);
    $$renderer2.push(`<!----> <div class="bg-panel rounded p-3"><div><label for="cutoffs" class="text-sm">FZI Cutoffs</label> <input id="cutoffs" type="text"${attr("value", cutoffsInput)} class="input mt-1" placeholder="0.1, 1.0, 3.0, 6.0"/></div> <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-3"><div><label for="fwl" class="text-sm">FWL (ft)</label> <input id="fwl" type="number" step="0.1"${attr("value", fwl)} class="input mt-1"/></div> <div><label for="ift" class="text-sm">IFT (dynes/cm)</label> <input id="ift" type="number" step="0.1"${attr("value", ift)} class="input mt-1"/></div> <div><label for="theta" class="text-sm">Theta (deg)</label> <input id="theta" type="number" step="0.1"${attr("value", theta)} class="input mt-1"/></div> <div><label for="gw" class="text-sm">GW (g/cc)</label> <input id="gw" type="number" step="0.01"${attr("value", gw)} class="input mt-1"/></div> <div><label for="ghc" class="text-sm">GHC (g/cc)</label> <input id="ghc" type="number" step="0.01"${attr("value", ghc)} class="input mt-1"/></div> <div class="col-span-2 flex items-end">`);
    Button($$renderer2, {
      class: "btn btn-primary",
      onclick: computeFits,
      disabled: loading || !data,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Compute Fits`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    Button($$renderer2, {
      class: "btn ml-2",
      onclick: computeShf,
      disabled: loading || !fits,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Compute SHF`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    Button($$renderer2, {
      class: "btn ml-2",
      onclick: saveShf,
      disabled: loading || !shfData,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Save SHF`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----></div></div> `);
    if (message) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div${attr_class(`text-sm ${stringify(message.startsWith("Error") ? "text-red-600" : "text-green-600")} mb-3`)}>${escape_html(message)}</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--> `);
    if (fits) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="font-semibold mb-2">Fitted Parameters</div> <div class="text-sm text-muted-foreground mb-3">J curve parameters a and b per rock flag.</div> <div class="bg-surface rounded p-3"><table class="w-full text-sm"><thead><tr><th>Rock Flag</th><th>a</th><th>b</th><th>RMSE</th></tr></thead><tbody><!--[-->`);
      const each_array = ensure_array_like(Object.entries(fits));
      for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
        let [rf, params] = each_array[$$index];
        $$renderer2.push(`<tr><td>${escape_html(rf)}</td><td>${escape_html(params.a)}</td><td>${escape_html(params.b)}</td><td>${escape_html(params.rmse)}</td></tr>`);
      }
      $$renderer2.push(`<!--]--></tbody></table></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--> <div class="grid grid-cols-1 gap-3"><div class="bg-surface rounded p-3 min-h-[220px]"><div class="font-medium mb-2">J Plot</div> <div class="text-sm text-muted-foreground">J vs SW with fitted curves per rock flag.</div> `);
    if (dataLoading) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="text-sm text-blue-600 mb-3">Loading data...</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      if (dataError) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="text-sm text-red-600 mb-3">${escape_html(dataError)}</div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--> <div class="mt-4 h-[300px] bg-white/5 rounded border border-border/30"></div></div> <div class="bg-surface rounded p-3 min-h-[220px]"><div class="font-medium mb-2">SHF Plot</div> <div class="text-sm text-muted-foreground">SHF vs depth.</div> <div class="mt-4 h-[300px] bg-white/5 rounded border border-border/30"></div></div></div></div></div>`);
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
