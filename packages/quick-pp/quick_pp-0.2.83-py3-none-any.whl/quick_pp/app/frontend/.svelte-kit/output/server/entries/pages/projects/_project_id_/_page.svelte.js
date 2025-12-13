import { aj as fallback, t as escape_html, F as ensure_array_like, c as bind_props, a as attr, o as onDestroy, ak as attr_style, i as stringify, s as store_get, u as unsubscribe_stores, p as page } from "../../../../chunks/vendor.js";
import "../../../../chunks/workspace.js";
import "@sveltejs/kit/internal";
import "@sveltejs/kit/internal/server";
import { B as Button } from "../../../../chunks/button.js";
/* empty css                        */
function WellSelector($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = $$props["projectId"];
    let selected = fallback($$props["selected"], null);
    let placeholder = fallback($$props["placeholder"], "Select well...");
    const API_BASE = "http://localhost:6312";
    let wells = [];
    let loading = false;
    let error = null;
    async function loadWells() {
      if (!projectId) return;
      loading = true;
      error = null;
      try {
        const res = await fetch(`${API_BASE}/quick_pp/database/projects/${projectId}/wells`);
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        wells = Array.isArray(data) ? data : data.wells ?? [];
      } catch (err) {
        error = String(err?.message ?? err);
      } finally {
        loading = false;
      }
    }
    if (projectId) loadWells();
    $$renderer2.push(`<div>`);
    if (loading) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="text-sm">Loading wells…</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      if (error) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="text-red-600 text-sm">${escape_html(error)}</div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> `);
      $$renderer2.select({ value: selected, class: "input" }, ($$renderer3) => {
        $$renderer3.option({ value: "" }, ($$renderer4) => {
          $$renderer4.push(`${escape_html(placeholder)}`);
        });
        $$renderer3.push(`<!--[-->`);
        const each_array = ensure_array_like(wells);
        for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
          let w = each_array[$$index];
          $$renderer3.option({ value: w.name }, ($$renderer4) => {
            $$renderer4.push(`${escape_html(w.name)}${escape_html(w.uwi ? ` — ${w.uwi}` : "")}`);
          });
        }
        $$renderer3.push(`<!--]-->`);
      });
    }
    $$renderer2.push(`<!--]--></div>`);
    bind_props($$props, { projectId, selected, placeholder });
  });
}
function BulkAncillaryImporter($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = $$props["projectId"];
    let type = fallback($$props["type"], "formation_tops");
    let maxConcurrency = fallback($$props["maxConcurrency"], 4);
    let previews = [];
    let selectedWells = {};
    let processing = false;
    let results = [];
    let fileStatuses = {};
    let fileErrors = {};
    let $$settled = true;
    let $$inner_renderer;
    function $$render_inner($$renderer3) {
      $$renderer3.push(`<div class="bulk-importer"><div class="mb-2"><div class="flex items-center gap-3"><label for="import-type-select" class="block text-sm">Import type</label> `);
      $$renderer3.select({ id: "import-type-select", value: type, class: "input w-48" }, ($$renderer4) => {
        $$renderer4.option({ value: "formation_tops" }, ($$renderer5) => {
          $$renderer5.push(`Formation tops`);
        });
        $$renderer4.option({ value: "fluid_contacts" }, ($$renderer5) => {
          $$renderer5.push(`Fluid contacts`);
        });
        $$renderer4.option({ value: "pressure_tests" }, ($$renderer5) => {
          $$renderer5.push(`Pressure tests`);
        });
        $$renderer4.option({ value: "core_samples" }, ($$renderer5) => {
          $$renderer5.push(`Core samples`);
        });
        $$renderer4.option({ value: "rca" }, ($$renderer5) => {
          $$renderer5.push(`RCA (measurements)`);
        });
        $$renderer4.option({ value: "scal" }, ($$renderer5) => {
          $$renderer5.push(`SCAL (relperm/pc)`);
        });
      });
      $$renderer3.push(` <label for="csv-input" class="block text-sm mb-0"><div class="px-3 py-2 border rounded cursor-pointer bg-white/5">Choose CSV files</div></label> <input id="csv-input" type="file" accept=".csv" multiple class="hidden"/></div> <div class="text-xs text-muted-foreground mt-1"><div>You can select multiple CSVs. Each file can target a well or include a <code>well_name</code> column.</div> <div class="mt-1">Required columns for the selected import type:</div> `);
      if (type === "formation_tops") {
        $$renderer3.push("<!--[-->");
        $$renderer3.push(`<div class="text-xs"><code>name</code>, <code>depth</code></div>`);
      } else {
        $$renderer3.push("<!--[!-->");
        if (type === "fluid_contacts") {
          $$renderer3.push("<!--[-->");
          $$renderer3.push(`<div class="text-xs"><code>name</code>, <code>depth</code></div>`);
        } else {
          $$renderer3.push("<!--[!-->");
          if (type === "pressure_tests") {
            $$renderer3.push("<!--[-->");
            $$renderer3.push(`<div class="text-xs"><code>depth</code>, <code>pressure</code>, <code>pressure_uom</code> (optional)</div>`);
          } else {
            $$renderer3.push("<!--[!-->");
            if (type === "core_samples" || type === "rca") {
              $$renderer3.push("<!--[-->");
              $$renderer3.push(`<div class="text-xs">Required columns: <code>well_name</code>, <code>sample_name</code> (or <code>sample</code>), <code>depth</code>, <code>description</code>, <code>remarks</code>, and measurement columns: <code>cpore</code>, <code>cperm</code></div>`);
            } else {
              $$renderer3.push("<!--[!-->");
              if (type === "scal") {
                $$renderer3.push("<!--[-->");
                $$renderer3.push(`<div class="text-xs">Relperm: <code>rp_sat</code>, <code>rp_kr</code>, <code>rp_phase</code>. Capillary pressure: <code>pc_sat</code>, <code>pc_pressure</code>, <code>pc_type</code>, <code>pc_cycle</code>. Wide format supported: <code>Pc.1</code>, <code>Pc.2</code>, <code>Sw.1</code>, <code>Sw.2</code>, etc.</div>`);
              } else {
                $$renderer3.push("<!--[!-->");
              }
              $$renderer3.push(`<!--]-->`);
            }
            $$renderer3.push(`<!--]-->`);
          }
          $$renderer3.push(`<!--]-->`);
        }
        $$renderer3.push(`<!--]-->`);
      }
      $$renderer3.push(`<!--]--></div></div> `);
      if (previews.length) {
        $$renderer3.push("<!--[-->");
        $$renderer3.push(`<div class="mb-2"><div class="font-semibold">Files preview</div> <!--[-->`);
        const each_array = ensure_array_like(previews);
        for (let $$index_3 = 0, $$length = each_array.length; $$index_3 < $$length; $$index_3++) {
          let p = each_array[$$index_3];
          $$renderer3.push(`<div class="border rounded p-3 my-2 bg-panel"><div class="flex justify-between items-start mb-2"><div><div class="font-medium">${escape_html(p.fileName)}</div> <div class="text-xs text-muted-foreground">Detected: ${escape_html(JSON.stringify(p.detected))}</div></div> <div class="flex items-center gap-2">`);
          if (fileStatuses[p.fileName] === "processing") {
            $$renderer3.push("<!--[-->");
            $$renderer3.push(`<div class="text-sm">Processing…</div>`);
          } else {
            $$renderer3.push("<!--[!-->");
            if (fileStatuses[p.fileName] === "success") {
              $$renderer3.push("<!--[-->");
              $$renderer3.push(`<div class="text-sm text-green-600">✓ Imported</div>`);
            } else {
              $$renderer3.push("<!--[!-->");
              if (fileStatuses[p.fileName] === "error") {
                $$renderer3.push("<!--[-->");
                $$renderer3.push(`<div class="text-sm text-red-600">✕ ${escape_html(fileErrors[p.fileName])}</div>`);
              } else {
                $$renderer3.push("<!--[!-->");
              }
              $$renderer3.push(`<!--]-->`);
            }
            $$renderer3.push(`<!--]-->`);
          }
          $$renderer3.push(`<!--]--> <button class="btn btn-ghost btn-sm">Remove</button></div></div> <div class="mb-2 flex items-center gap-2"><div class="text-sm">Target well:</div> `);
          WellSelector($$renderer3, {
            projectId,
            get selected() {
              return selectedWells[p.fileName];
            },
            set selected($$value) {
              selectedWells[p.fileName] = $$value;
              $$settled = false;
            }
          });
          $$renderer3.push(`<!----></div> <div class="text-sm overflow-auto"><table class="text-sm w-full table-auto border-collapse"><thead><tr>`);
          if (p.previewRows && p.previewRows.length) {
            $$renderer3.push("<!--[-->");
            $$renderer3.push(`<!--[-->`);
            const each_array_1 = ensure_array_like(Object.keys(p.previewRows[0]));
            for (let $$index = 0, $$length2 = each_array_1.length; $$index < $$length2; $$index++) {
              let h = each_array_1[$$index];
              $$renderer3.push(`<th class="text-left pr-3">${escape_html(h)}</th>`);
            }
            $$renderer3.push(`<!--]-->`);
          } else {
            $$renderer3.push("<!--[!-->");
          }
          $$renderer3.push(`<!--]--></tr></thead><tbody><!--[-->`);
          const each_array_2 = ensure_array_like(p.previewRows && p.previewRows.length ? p.previewRows : p.rows.slice(0, 10));
          for (let $$index_2 = 0, $$length2 = each_array_2.length; $$index_2 < $$length2; $$index_2++) {
            let r = each_array_2[$$index_2];
            $$renderer3.push(`<tr><!--[-->`);
            const each_array_3 = ensure_array_like(Object.keys(r));
            for (let $$index_1 = 0, $$length3 = each_array_3.length; $$index_1 < $$length3; $$index_1++) {
              let k = each_array_3[$$index_1];
              $$renderer3.push(`<td class="pr-3">${escape_html(r[k])}</td>`);
            }
            $$renderer3.push(`<!--]--></tr>`);
          }
          $$renderer3.push(`<!--]--></tbody></table></div></div>`);
        }
        $$renderer3.push(`<!--]--></div> `);
        {
          $$renderer3.push("<!--[!-->");
        }
        $$renderer3.push(`<!--]--> <div class="mb-3"><button class="btn btn-primary"${attr("disabled", processing, true)}>${escape_html("Process all")}</button></div> `);
        if (results.length) {
          $$renderer3.push("<!--[-->");
          $$renderer3.push(`<div class="mt-2"><div class="font-semibold">Results</div> <ul><!--[-->`);
          const each_array_4 = ensure_array_like(results);
          for (let $$index_4 = 0, $$length = each_array_4.length; $$index_4 < $$length; $$index_4++) {
            let r = each_array_4[$$index_4];
            $$renderer3.push(`<li>${escape_html(r.file)}: ${escape_html(r.ok ? "OK" : `FAILED (${r.status || ""}) - ${r.error ?? ""}`)}</li>`);
          }
          $$renderer3.push(`<!--]--></ul></div>`);
        } else {
          $$renderer3.push("<!--[!-->");
        }
        $$renderer3.push(`<!--]-->`);
      } else {
        $$renderer3.push("<!--[!-->");
      }
      $$renderer3.push(`<!--]--></div>`);
    }
    do {
      $$settled = true;
      $$inner_renderer = $$renderer2.copy();
      $$render_inner($$inner_renderer);
    } while (!$$settled);
    $$renderer2.subsume($$inner_renderer);
    bind_props($$props, { projectId, type, maxConcurrency });
  });
}
function WsFormationTops($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = $$props["projectId"];
    let wellName = fallback($$props["wellName"], "");
    let showList = fallback($$props["showList"], true);
    function normalizeWellNames() {
      if (!wellName) return null;
      if (Array.isArray(wellName)) return wellName.map(String);
      return [String(wellName)];
    }
    function buildWellNameQs() {
      const names = normalizeWellNames();
      if (!names || names.length === 0) return "";
      return "?" + names.map((n) => `well_name=${encodeURIComponent(String(n))}`).join("&");
    }
    const API_BASE = "http://localhost:6312";
    let tops = [];
    let loading = false;
    let error = null;
    let newTop = { name: "", depth: null };
    let showImporter = false;
    async function loadTops() {
      if (!projectId) return;
      loading = true;
      error = null;
      try {
        const qs = buildWellNameQs();
        const res = await fetch(`${API_BASE}/quick_pp/database/projects/${projectId}/formation_tops${qs}`);
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        tops = data.tops || [];
      } catch (err) {
        error = String(err?.message ?? err);
      } finally {
        loading = false;
      }
    }
    async function addTop() {
      {
        error = "Name and depth are required";
        return;
      }
    }
    async function deleteTop(name) {
      if (!confirm(`Delete top '${name}'?`)) return;
      loading = true;
      error = null;
      try {
        const qs = buildWellNameQs();
        const res = await fetch(`${API_BASE}/quick_pp/database/projects/${projectId}/formation_tops/${encodeURIComponent(name)}${qs}`, { method: "DELETE" });
        if (!res.ok) throw new Error(await res.text());
        await loadTops();
      } catch (err) {
        error = String(err?.message ?? err);
      } finally {
        loading = false;
      }
    }
    if (projectId) {
      loadTops();
    }
    $$renderer2.push(`<div class="formation-tops">`);
    if (loading) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="text-sm">Loading…</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      if (error) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="text-sm text-red-600">${escape_html(error)}</div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> <div class="mb-3 flex items-center gap-2"><input placeholder="Well name"${attr("value", wellName)} class="input w-32"/> <input placeholder="Top name"${attr("value", newTop.name)} class="input w-32"/> <input placeholder="Depth" type="number"${attr("value", newTop.depth)} class="input w-24"/></div> `);
      Button($$renderer2, {
        variant: "default",
        onclick: addTop,
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->Add Top`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----> `);
      Button($$renderer2, {
        variant: "secondary",
        class: "ml-2",
        onclick: () => showImporter = !showImporter,
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->${escape_html(showImporter ? "Hide bulk importer" : "Bulk import")}`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----> `);
      if (showImporter) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="mt-3 mb-3">`);
        BulkAncillaryImporter($$renderer2, { projectId, type: "formation_tops" });
        $$renderer2.push(`<!----></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> `);
      if (showList) {
        $$renderer2.push("<!--[-->");
        if (tops.length === 0) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<div class="text-sm text-muted-foreground">No tops defined for this well.</div>`);
        } else {
          $$renderer2.push("<!--[!-->");
          $$renderer2.push(`<ul class="space-y-1"><!--[-->`);
          const each_array = ensure_array_like(tops);
          for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
            let t = each_array[$$index];
            $$renderer2.push(`<li class="flex justify-between items-center p-2 bg-white/5 rounded"><div>${escape_html(t.well_name)}: ${escape_html(t.name)} — ${escape_html(t.depth)}</div> <div>`);
            Button($$renderer2, {
              variant: "outline",
              onclick: () => deleteTop(t.name),
              children: ($$renderer3) => {
                $$renderer3.push(`<!---->Delete`);
              },
              $$slots: { default: true }
            });
            $$renderer2.push(`<!----></div></li>`);
          }
          $$renderer2.push(`<!--]--></ul>`);
        }
        $$renderer2.push(`<!--]-->`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--></div>`);
    bind_props($$props, { projectId, wellName, showList });
  });
}
function WsFluidContacts($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = $$props["projectId"];
    let wellName = $$props["wellName"];
    let showList = fallback($$props["showList"], true);
    const API_BASE = "http://localhost:6312";
    let contacts = [];
    let loading = false;
    let error = null;
    let newContact = { name: "", depth: null };
    let showImporter = false;
    async function loadContacts() {
      if (!projectId) return;
      loading = true;
      error = null;
      try {
        const qs = wellName ? `?well_name=${encodeURIComponent(String(wellName))}` : "";
        const res = await fetch(`${API_BASE}/quick_pp/database/projects/${projectId}/fluid_contacts${qs}`);
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        contacts = data.fluid_contacts || [];
      } catch (err) {
        error = String(err?.message ?? err);
      } finally {
        loading = false;
      }
    }
    async function addContact() {
      {
        error = "Name and depth required";
        return;
      }
    }
    if (projectId) loadContacts();
    $$renderer2.push(`<div class="fluid-contacts">`);
    if (loading) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="text-sm">Loading…</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      if (error) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="text-sm text-red-600">${escape_html(error)}</div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> <div class="mb-3"><input placeholder="Well name"${attr("value", wellName)} class="input w-32"/> <input placeholder="Contact name"${attr("value", newContact.name)} class="input w-32"/> <input placeholder="Depth" type="number"${attr("value", newContact.depth)} class="input w-24"/></div> `);
      Button($$renderer2, {
        variant: "default",
        onclick: addContact,
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->Add`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----> `);
      Button($$renderer2, {
        variant: "secondary",
        class: "ml-2",
        onclick: () => showImporter = !showImporter,
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->${escape_html(showImporter ? "Hide bulk importer" : "Bulk import")}`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----> `);
      if (showImporter) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="mb-3">`);
        BulkAncillaryImporter($$renderer2, { projectId, type: "fluid_contacts" });
        $$renderer2.push(`<!----></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> `);
      if (showList) {
        $$renderer2.push("<!--[-->");
        if (contacts.length === 0) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<div class="text-sm text-muted">No fluid contacts</div>`);
        } else {
          $$renderer2.push("<!--[!-->");
          $$renderer2.push(`<ul class="space-y-1"><!--[-->`);
          const each_array = ensure_array_like(contacts);
          for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
            let c = each_array[$$index];
            $$renderer2.push(`<li class="flex justify-between items-center p-2 bg-white/5 rounded"><div>${escape_html(c.well_name ?? wellName)}: ${escape_html(c.name)} — ${escape_html(c.depth)}</div></li>`);
          }
          $$renderer2.push(`<!--]--></ul>`);
        }
        $$renderer2.push(`<!--]-->`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--></div>`);
    bind_props($$props, { projectId, wellName, showList });
  });
}
function WsPressureTests($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let projectId = $$props["projectId"];
    let wellName = $$props["wellName"];
    let showList = fallback($$props["showList"], true);
    const API_BASE = "http://localhost:6312";
    let tests = [];
    let loading = false;
    let error = null;
    let newTest = { depth: null, pressure: null, pressure_uom: "psi" };
    let showImporter = false;
    async function loadTests() {
      if (!projectId) return;
      loading = true;
      error = null;
      try {
        const qs = wellName ? `?well_name=${encodeURIComponent(String(wellName))}` : "";
        const res = await fetch(`${API_BASE}/quick_pp/database/projects/${projectId}/pressure_tests${qs}`);
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();
        tests = data.pressure_tests || [];
      } catch (err) {
        error = String(err?.message ?? err);
      } finally {
        loading = false;
      }
    }
    async function addTest() {
      {
        error = "Depth and pressure are required";
        return;
      }
    }
    if (projectId) loadTests();
    $$renderer2.push(`<div class="pressure-tests">`);
    if (loading) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="text-sm">Loading…</div>`);
    } else {
      $$renderer2.push("<!--[!-->");
      if (error) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="text-sm text-red-600">${escape_html(error)}</div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> <div class="mb-3"><input placeholder="Well name"${attr("value", wellName)} class="input w-32"/> <input placeholder="Depth" type="number"${attr("value", newTest.depth)} class="input w-24"/> <input placeholder="Pressure" type="number"${attr("value", newTest.pressure)} class="input w-24"/> `);
      $$renderer2.select({ value: newTest.pressure_uom, class: "input w-24" }, ($$renderer3) => {
        $$renderer3.option({}, ($$renderer4) => {
          $$renderer4.push(`psi`);
        });
        $$renderer3.option({}, ($$renderer4) => {
          $$renderer4.push(`bar`);
        });
      });
      $$renderer2.push(`</div> `);
      Button($$renderer2, {
        variant: "default",
        onclick: addTest,
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->Add`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----> `);
      Button($$renderer2, {
        variant: "secondary",
        class: "ml-2",
        onclick: () => showImporter = !showImporter,
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->${escape_html(showImporter ? "Hide bulk importer" : "Bulk import")}`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----> `);
      if (showImporter) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="mb-3">`);
        BulkAncillaryImporter($$renderer2, { projectId, type: "pressure_tests" });
        $$renderer2.push(`<!----></div>`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> `);
      if (showList) {
        $$renderer2.push("<!--[-->");
        if (tests.length === 0) {
          $$renderer2.push("<!--[-->");
          $$renderer2.push(`<div class="text-sm text-muted">No pressure tests</div>`);
        } else {
          $$renderer2.push("<!--[!-->");
          $$renderer2.push(`<ul class="space-y-1"><!--[-->`);
          const each_array = ensure_array_like(tests);
          for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
            let t = each_array[$$index];
            $$renderer2.push(`<li class="flex justify-between items-center p-2 bg-white/5 rounded"><div>${escape_html(t.well_name)}: ${escape_html(t.depth)} — ${escape_html(t.pressure)} ${escape_html(t.pressure_uom)}</div></li>`);
          }
          $$renderer2.push(`<!--]--></ul>`);
        }
        $$renderer2.push(`<!--]-->`);
      } else {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]-->`);
    }
    $$renderer2.push(`<!--]--></div>`);
    bind_props($$props, { projectId, wellName, showList });
  });
}
function WsCoreSamples($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    const API_BASE = "http://localhost:6312";
    let projectId = $$props["projectId"];
    let wellName = $$props["wellName"];
    let showList = fallback($$props["showList"], true);
    let samples = [];
    let loading = false;
    let form = { sample_name: "", depth: "", description: "" };
    let measurements = [{ property_name: "", value: "", unit: "" }];
    let relperm = [{ saturation: "", kr: "", phase: "water" }];
    let pc = [
      { saturation: "", pressure: "", experiment_type: "", cycle: "" }
    ];
    let showImporter = false;
    async function fetchSamples() {
      loading = true;
      try {
        const qs = wellName ? `?well_name=${encodeURIComponent(String(wellName))}` : "";
        const res = await fetch(`${API_BASE}/quick_pp/database/projects/${projectId}/core_samples${qs}`);
        if (res.ok) {
          const data = await res.json();
          samples = data.core_samples || [];
        } else {
          console.warn("Failed to load core samples", await res.text());
        }
      } catch (e) {
        console.warn("Error fetching core samples", e);
      } finally {
        loading = false;
      }
    }
    function addMeasurement() {
      measurements = [...measurements, { property_name: "", value: "", unit: "" }];
    }
    function removeMeasurement(i) {
      measurements = [...measurements.slice(0, i), ...measurements.slice(i + 1)];
    }
    function addRelperm() {
      relperm = [...relperm, { saturation: "", kr: "", phase: "" }];
    }
    function removeRelperm(i) {
      relperm = [...relperm.slice(0, i), ...relperm.slice(i + 1)];
    }
    function addPc() {
      pc = [
        ...pc,
        { saturation: "", pressure: "", experiment_type: "", cycle: "" }
      ];
    }
    function removePc(i) {
      pc = [...pc.slice(0, i), ...pc.slice(i + 1)];
    }
    async function submitSample() {
      {
        alert("Sample name is required");
        return;
      }
    }
    if (projectId) {
      fetchSamples();
    }
    $$renderer2.push(`<div class="ws-core-samples">`);
    if (
      // basic validation
      showList
    ) {
      $$renderer2.push("<!--[-->");
      if (loading) {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div>Loading...</div>`);
      } else {
        $$renderer2.push("<!--[!-->");
        $$renderer2.push(`<ul class="space-y-2"><!--[-->`);
        const each_array = ensure_array_like(samples);
        for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
          let s = each_array[$$index];
          $$renderer2.push(`<li class="p-2 bg-surface rounded"><div class="font-medium">${escape_html(s.sample_name)}</div> <div class="text-sm">Depth: ${escape_html(s.depth)} ${escape_html(s.description ? `- ${s.description}` : "")}</div></li>`);
        }
        $$renderer2.push(`<!--]--></ul>`);
      }
      $$renderer2.push(`<!--]-->`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--> <div class="mt-4 bg-panel rounded p-3"><div class="font-semibold mb-2">Add / Update Sample</div> <div class="grid grid-cols-1 gap-2"><div class="flex items-center gap-2"><input placeholder="Well name"${attr("value", wellName)} class="input w-32"/> <input placeholder="Sample name"${attr("value", form.sample_name)} class="input w-32"/> <input placeholder="Depth"${attr("value", form.depth)} class="input w-32"/></div> <input placeholder="Description"${attr("value", form.description)} class="input"/> <div><div class="flex items-center justify-between"><span class="text-sm font-medium">Measurements (RCA)</span> `);
    Button($$renderer2, {
      class: "btn btn-sm",
      type: "button",
      onclick: addMeasurement,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Add`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----></div> <div class="space-y-2 mt-2"><!--[-->`);
    const each_array_1 = ensure_array_like(measurements);
    for (let i = 0, $$length = each_array_1.length; i < $$length; i++) {
      let m = each_array_1[i];
      $$renderer2.push(`<div class="grid grid-cols-12 gap-2 items-center"><input class="col-span-5 input" placeholder="Property"${attr("value", m.property_name)}/> <input class="col-span-3 input" placeholder="Value"${attr("value", m.value)}/> <input class="col-span-3 input" placeholder="Unit"${attr("value", m.unit)}/> `);
      Button($$renderer2, {
        variant: "secondary",
        type: "button",
        onclick: () => removeMeasurement(i),
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->✕`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----></div>`);
    }
    $$renderer2.push(`<!--]--></div></div> <div><div class="flex items-center justify-between"><span class="text-sm font-medium">Relative Permeability (relperm)</span> `);
    Button($$renderer2, {
      class: "btn btn-sm",
      type: "button",
      onclick: addRelperm,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Add`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----></div> <div class="space-y-2 mt-2"><!--[-->`);
    const each_array_2 = ensure_array_like(relperm);
    for (let i = 0, $$length = each_array_2.length; i < $$length; i++) {
      let r = each_array_2[i];
      $$renderer2.push(`<div class="grid grid-cols-12 gap-2 items-center"><input class="col-span-4 input" placeholder="Saturation"${attr("value", r.saturation)}/> <input class="col-span-4 input" placeholder="kr"${attr("value", r.kr)}/> <input class="col-span-3 input" placeholder="Phase"${attr("value", r.phase)}/> `);
      Button($$renderer2, {
        variant: "secondary",
        type: "button",
        onclick: () => removeRelperm(i),
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->✕`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----></div>`);
    }
    $$renderer2.push(`<!--]--></div></div> <div><div class="flex items-center justify-between"><span class="text-sm font-medium">Capillary Pressure (pc)</span> `);
    Button($$renderer2, {
      class: "btn btn-sm",
      type: "button",
      onclick: addPc,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Add`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----></div> <div class="space-y-2 mt-2"><!--[-->`);
    const each_array_3 = ensure_array_like(pc);
    for (let i = 0, $$length = each_array_3.length; i < $$length; i++) {
      let p = each_array_3[i];
      $$renderer2.push(`<div class="grid grid-cols-12 gap-2 items-center"><input class="col-span-3 input" placeholder="Saturation"${attr("value", p.saturation)}/> <input class="col-span-3 input" placeholder="Pressure"${attr("value", p.pressure)}/> `);
      $$renderer2.select({ class: "col-span-3 input", value: p.experiment_type }, ($$renderer3) => {
        $$renderer3.option({ value: "", disabled: true, hidden: true }, ($$renderer4) => {
          $$renderer4.push(`Experiment Type`);
        });
        $$renderer3.option({ value: "Porous plate" }, ($$renderer4) => {
          $$renderer4.push(`Porous plate`);
        });
        $$renderer3.option({ value: "Centrifuge" }, ($$renderer4) => {
          $$renderer4.push(`Centrifuge`);
        });
        $$renderer3.option({ value: "Mercury Injection" }, ($$renderer4) => {
          $$renderer4.push(`Mercury Injection`);
        });
      });
      $$renderer2.push(` `);
      $$renderer2.select({ class: "col-span-2 input", value: p.cycle }, ($$renderer3) => {
        $$renderer3.option({ value: "", disabled: true, hidden: true }, ($$renderer4) => {
          $$renderer4.push(`Cycle`);
        });
        $$renderer3.option({ value: "Drainage" }, ($$renderer4) => {
          $$renderer4.push(`Drainage`);
        });
        $$renderer3.option({ value: "Imbibition" }, ($$renderer4) => {
          $$renderer4.push(`Imbibition`);
        });
      });
      $$renderer2.push(` `);
      Button($$renderer2, {
        variant: "secondary",
        type: "button",
        onclick: () => removePc(i),
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->✕`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----></div>`);
    }
    $$renderer2.push(`<!--]--></div></div> <div class="mt-2">`);
    Button($$renderer2, {
      class: "btn btn-primary",
      onclick: submitSample,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->Save Sample`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----></div> <div class="mb-3">`);
    Button($$renderer2, {
      variant: "secondary",
      onclick: () => showImporter = !showImporter,
      children: ($$renderer3) => {
        $$renderer3.push(`<!---->${escape_html(showImporter ? "Hide bulk importer" : "Bulk import")}`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----></div> `);
    if (showImporter) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="mb-3">`);
      BulkAncillaryImporter($$renderer2, { projectId, type: "core_samples" });
      $$renderer2.push(`<!----></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div></div></div>`);
    bind_props($$props, { projectId, wellName, showList });
  });
}
function Ws_project($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let _unsubWorkspace = null;
    let depthUom = "m";
    const depthUomId = `depth-uom-${Math.random().toString(36).slice(2, 9)}`;
    let showTops = false;
    let showContacts = false;
    let showPressure = false;
    let showCore = false;
    let showUpload = false;
    async function uploadLas() {
      return;
    }
    onDestroy(() => {
      try {
        _unsubWorkspace && _unsubWorkspace();
      } catch (e) {
      }
    });
    $$renderer2.push(`<div class="project-workspace p-4"><div class="grid grid-cols-1 md:grid-cols-3 gap-4"><div class="col-span-1"><div class="bg-panel rounded p-4 space-y-4"><div class="font-semibold">Data Inputs</div> <div class="text-sm text-muted-foreground">Add or edit data for wells.</div> <div class="accordion-item bg-surface rounded">`);
    Button($$renderer2, {
      variant: "ghost",
      class: "w-full flex justify-between items-center p-2",
      onclick: () => showUpload = !showUpload,
      "aria-expanded": showUpload,
      children: ($$renderer3) => {
        $$renderer3.push(`<div class="font-medium">Add wells from LAS</div> <div class="text-sm"><svg class="inline-block" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"${attr_style(`transform: rotate(${stringify(showUpload ? 90 : 0)}deg); transition: transform .18s ease;`)}><path d="M8 5l8 7-8 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"></path></svg></div>`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    if (showUpload) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="p-3"><div class="mt-1"><div class="text-sm">Select one or more LAS files to add wells to this project.</div> <div class="mt-2"><label${attr("for", depthUomId)} class="text-sm text-muted-foreground">Depth units</label> `);
      $$renderer2.select(
        {
          id: depthUomId,
          value: depthUom,
          class: "rounded border bg-white/5 text-sm p-1 w-27"
        },
        ($$renderer3) => {
          $$renderer3.option({ value: "m" }, ($$renderer4) => {
            $$renderer4.push(`m (meters)`);
          });
          $$renderer3.option({ value: "ft" }, ($$renderer4) => {
            $$renderer4.push(`ft (feet)`);
          });
        }
      );
      $$renderer2.push(` <div class="flex items-center justify-between border rounded-md p-2 bg-white/5"><div class="text-sm text-muted-foreground">`);
      {
        $$renderer2.push("<!--[!-->");
        $$renderer2.push(`No files chosen`);
      }
      $$renderer2.push(`<!--]--></div> <div class="flex items-center gap-2"><label class="inline-flex items-center px-3 py-1 rounded-md border cursor-pointer text-sm"><input type="file" accept=".las,.LAS" multiple class="hidden"/> Choose</label> `);
      Button($$renderer2, {
        variant: "default",
        onclick: uploadLas,
        disabled: true,
        children: ($$renderer3) => {
          $$renderer3.push(`<!---->Upload`);
        },
        $$slots: { default: true }
      });
      $$renderer2.push(`<!----></div></div> `);
      {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> `);
      {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--> `);
      {
        $$renderer2.push("<!--[!-->");
      }
      $$renderer2.push(`<!--]--></div></div></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div> <div class="accordion-item bg-surface rounded">`);
    Button($$renderer2, {
      variant: "ghost",
      class: "w-full flex justify-between items-center p-2",
      onclick: () => showTops = !showTops,
      "aria-expanded": showTops,
      children: ($$renderer3) => {
        $$renderer3.push(`<div class="font-medium">Formation Tops</div> <div class="text-sm"><svg class="inline-block" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"${attr_style(`transform: rotate(${stringify(showTops ? 90 : 0)}deg); transition: transform .18s ease;`)}><path d="M8 5l8 7-8 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"></path></svg></div>`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    if (showTops) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="p-2">`);
      WsFormationTops($$renderer2, {
        projectId: "",
        wellName: "",
        showList: false
      });
      $$renderer2.push(`<!----></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div> <div class="accordion-item bg-surface rounded">`);
    Button($$renderer2, {
      variant: "ghost",
      class: "w-full flex justify-between items-center p-2",
      onclick: () => showCore = !showCore,
      "aria-expanded": showCore,
      children: ($$renderer3) => {
        $$renderer3.push(`<div class="font-medium">Core Samples (RCA &amp; SCAL)</div> <div class="text-sm"><svg class="inline-block" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"${attr_style(`transform: rotate(${stringify(showCore ? 90 : 0)}deg); transition: transform .18s ease;`)}><path d="M8 5l8 7-8 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"></path></svg></div>`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    if (showCore) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="p-2">`);
      WsCoreSamples($$renderer2, {
        projectId: "",
        wellName: "",
        showList: false
      });
      $$renderer2.push(`<!----></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div> <div class="accordion-item bg-surface rounded">`);
    Button($$renderer2, {
      variant: "ghost",
      class: "w-full flex justify-between items-center p-2",
      onclick: () => showPressure = !showPressure,
      "aria-expanded": showPressure,
      children: ($$renderer3) => {
        $$renderer3.push(`<div class="font-medium">Pressure Tests</div> <div class="text-sm"><svg class="inline-block" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"${attr_style(`transform: rotate(${stringify(showPressure ? 90 : 0)}deg); transition: transform .18s ease;`)}><path d="M8 5l8 7-8 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"></path></svg></div>`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    if (showPressure) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="p-2">`);
      WsPressureTests($$renderer2, {
        projectId: "",
        wellName: "",
        showList: false
      });
      $$renderer2.push(`<!----></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div> <div class="accordion-item bg-surface rounded">`);
    Button($$renderer2, {
      variant: "ghost",
      class: "w-full flex justify-between items-center p-2",
      onclick: () => showContacts = !showContacts,
      "aria-expanded": showContacts,
      children: ($$renderer3) => {
        $$renderer3.push(`<div class="font-medium">Fluid Contacts</div> <div class="text-sm"><svg class="inline-block" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"${attr_style(`transform: rotate(${stringify(showContacts ? 90 : 0)}deg); transition: transform .18s ease;`)}><path d="M8 5l8 7-8 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"></path></svg></div>`);
      },
      $$slots: { default: true }
    });
    $$renderer2.push(`<!----> `);
    if (showContacts) {
      $$renderer2.push("<!--[-->");
      $$renderer2.push(`<div class="p-2">`);
      WsFluidContacts($$renderer2, {
        projectId: "",
        wellName: "",
        showList: false
      });
      $$renderer2.push(`<!----></div>`);
    } else {
      $$renderer2.push("<!--[!-->");
    }
    $$renderer2.push(`<!--]--></div></div></div> <div class="col-span-2"><div class="bg-panel rounded p-4">`);
    {
      $$renderer2.push("<!--[!-->");
      $$renderer2.push(`<div class="text-muted-foreground">Select a project from the sidebar to view details.</div>`);
    }
    $$renderer2.push(`<!--]--></div></div></div></div>`);
  });
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    store_get($$store_subs ??= {}, "$page", page).params.project_id;
    $$renderer2.push(`<div>`);
    Ws_project($$renderer2);
    $$renderer2.push(`<!----></div>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
