import "clsx";
import { o as onDestroy } from "../../../chunks/index-server.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let _unsubWorkspace = null;
    let _unsubProjects = null;
    onDestroy(() => {
      try {
        _unsubWorkspace && _unsubWorkspace();
      } catch (e) {
      }
      try {
        _unsubProjects && _unsubProjects();
      } catch (e) {
      }
    });
    {
      $$renderer2.push("<!--[!-->");
      $$renderer2.push(`<div class="p-6"><h2 class="text-lg font-semibold">Projects</h2> `);
      {
        $$renderer2.push("<!--[-->");
        $$renderer2.push(`<div class="mt-4 text-sm"><p>No projects found for your account or workspace.</p> <p class="mt-2">How to proceed:</p> <ul class="list-disc ml-6 mt-2 text-sm"><li>Use the <strong>New Project</strong> button in the left sidebar to create a project.</li> <li>If you already have projects, open the project selector in the sidebar and choose one to activate it.</li></ul> <p class="mt-3 text-muted-foreground">After creating or selecting a project the workspace will open automatically.</p></div>`);
      }
      $$renderer2.push(`<!--]--></div>`);
    }
    $$renderer2.push(`<!--]-->`);
  });
}
export {
  _page as default
};
