import { S as escape_html } from "../../chunks/utils2.js";
import "clsx";
import "../../chunks/state.svelte.js";
import { s as stores } from "../../chunks/client.js";
import { g as getContext } from "../../chunks/context.js";
({
  check: stores.updated.check
});
function context() {
  return getContext("__request__");
}
const page$1 = {
  get error() {
    return context().page.error;
  },
  get status() {
    return context().page.status;
  }
};
const page = page$1;
function Error$1($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    $$renderer2.push(`<h1>${escape_html(page.status)}</h1> <p>${escape_html(page.error?.message)}</p>`);
  });
}
export {
  Error$1 as default
};
