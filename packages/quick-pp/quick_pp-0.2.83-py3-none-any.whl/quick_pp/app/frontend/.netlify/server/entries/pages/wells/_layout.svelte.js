import { b as slot, c as bind_props } from "../../../chunks/vendor.js";
import "clsx";
import { S as Sidebar_provider, A as App_sidebar, a as Sidebar_inset, b as Site_header } from "../../../chunks/site-header.js";
import "../../../chunks/button.js";
import "../../../chunks/workspace.js";
import "@sveltejs/kit/internal";
import "@sveltejs/kit/internal/server";
function _layout($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let data = $$props["data"];
    Sidebar_provider($$renderer2, {
      style: "--sidebar-width: calc(var(--spacing) * 72); --header-height: calc(var(--spacing) * 12);",
      children: ($$renderer3) => {
        App_sidebar($$renderer3, { variant: "inset" });
        $$renderer3.push(`<!----> `);
        Sidebar_inset($$renderer3, {
          children: ($$renderer4) => {
            Site_header($$renderer4);
            $$renderer4.push(`<!----> <div class="flex flex-1 flex-col"><div class="@container/main flex flex-1 flex-col gap-2"><div class="flex flex-col gap-4 py-4 md:gap-6 md:py-6"><!--[-->`);
            slot($$renderer4, $$props, "default", {});
            $$renderer4.push(`<!--]--></div></div></div>`);
          },
          $$slots: { default: true }
        });
        $$renderer3.push(`<!---->`);
      },
      $$slots: { default: true }
    });
    bind_props($$props, { data });
  });
}
export {
  _layout as default
};
