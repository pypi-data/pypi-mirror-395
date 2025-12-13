import { a as attr, o as attr_style, c as bind_props, j as stringify } from "./index2.js";
import { o as onDestroy } from "./index-server.js";
import { D as DEV } from "./false.js";
import { w as workspace } from "./workspace.js";
import { D as DepthFilterStatus } from "./DepthFilterStatus.js";
import { f as fallback } from "./context.js";
import { S as escape_html } from "./utils2.js";
const browser = DEV;
function WsWellPlot($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = $$props["projectId"];
    let wellName = $$props["wellName"];
    let container = null;
    let minWidth = fallback($$props["minWidth"], "480px");
    let loading = false;
    let error = null;
    let autoRefresh = false;
    let refreshInterval = 5e3;
    let _refreshTimer = null;
    let depthFilter = { enabled: false, minDepth: null, maxDepth: null };
    let zoneFilter = { enabled: false, zones: [] };
    const API_BASE = "http://localhost:6312";
    async function ensurePlotly() {
      throw new Error("Plotly can only be loaded in the browser");
    }
    async function loadAndRender() {
      if (!projectId || !wellName) return;
      loading = true;
      error = null;
      try {
        let url = `${API_BASE}/quick_pp/plotter/projects/${projectId}/wells/${encodeURIComponent(String(wellName))}/log`;
        const params = new URLSearchParams();
        if (depthFilter.enabled) {
          if (depthFilter.minDepth !== null) {
            params.append("min_depth", String(depthFilter.minDepth));
          }
          if (depthFilter.maxDepth !== null) {
            params.append("max_depth", String(depthFilter.maxDepth));
          }
        }
        if (zoneFilter?.enabled && Array.isArray(zoneFilter.zones) && zoneFilter.zones.length > 0) {
          const encoded = zoneFilter.zones.map((z) => String(z)).join(",");
          params.append("zones", encoded);
        }
        if (params.toString()) {
          url += "?" + params.toString();
        }
        const res = await fetch(url);
        if (!res.ok) throw new Error(await res.text());
        const fig = await res.json();
        if (!container) throw new Error("Missing plot container");
        const PlotlyLib = await ensurePlotly();
        if (!PlotlyLib) throw new Error("Failed to load Plotly library");
        const config = { ...fig.config || {}, responsive: true, scrollZoom: true };
        const layout = {
          ...fig.layout || {},
          dragmode: fig.layout?.dragmode ?? "zoom"
        };
        if (PlotlyLib.react) {
          PlotlyLib.react(container, fig.data, layout, config);
        } else {
          PlotlyLib.newPlot(container, fig.data, layout, config);
        }
        if (browser && typeof ResizeObserver !== "undefined") ;
      } catch (err) {
        console.error("Failed to render well plot", err);
        error = String(err?.message ?? err);
      } finally {
        loading = false;
      }
    }
    function scheduleAutoRefresh() {
      try {
        if (_refreshTimer) {
          clearInterval(_refreshTimer);
          _refreshTimer = null;
        }
        if (autoRefresh && typeof window !== "undefined") ;
      } catch (e) {
      }
    }
    const unsubscribeWorkspace = workspace.subscribe((w) => {
      if (w?.depthFilter) {
        const newFilter = { ...w.depthFilter };
        if (JSON.stringify(newFilter) !== JSON.stringify(depthFilter)) {
          depthFilter = newFilter;
        }
      }
      if (w?.zoneFilter) {
        const newZone = { ...w.zoneFilter };
        const prev = zoneFilter && Array.isArray(zoneFilter.zones) ? zoneFilter.zones.join(",") : "";
        const curr = newZone && Array.isArray(newZone.zones) ? newZone.zones.join(",") : "";
        if (newZone.enabled !== zoneFilter.enabled || prev !== curr) {
          zoneFilter = newZone;
        }
      }
    });
    onDestroy(() => {
      try {
        unsubscribeWorkspace();
        if (container && container._plotlyResizeObserver) ;
        if (_refreshTimer) {
          clearInterval(_refreshTimer);
          _refreshTimer = null;
        }
      } catch (e) {
      }
    });
    scheduleAutoRefresh();
    $$renderer2.push(`<div class="ws-well-plot">`);
    DepthFilterStatus($$renderer2);
    $$renderer2.push(`<!----> <div class="mb-2 flex items-center gap-2"><button class="btn px-3 py-1 text-sm bg-gray-800 text-white rounded" aria-label="Refresh plot">Refresh</button> <label class="text-sm flex items-center gap-1"><input type="checkbox"${attr(
      "checked",
      // Subscribe to workspace for depth filter changes
      // Check if filter actually changed to avoid unnecessary re-renders
      // Trigger re-render when depth filter changes
      // zone filter changes should also trigger a re-render
      // compare by enabled + joined zones
      // initial render handled by reactive statement above
      // ignore
      // Listen for updates dispatched from other components (e.g., save actions)
      // Only refresh if the event refers to the same project/well
      // remove listener on destroy
      autoRefresh,
      true
    )}/> Auto-refresh</label> `);
    {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div> `);
    if (loading) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="text-sm">Loading well log…</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      if (error) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="text-sm text-red-500">Error: ${escape_html(error)}</div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--> <div${attr_style(`width:100%; min-width: ${stringify(minWidth)}; height:900px;`)}></div></div>`);
    bind_props($$props, { projectId, wellName, minWidth });
  });
}
export {
  WsWellPlot as W
};
