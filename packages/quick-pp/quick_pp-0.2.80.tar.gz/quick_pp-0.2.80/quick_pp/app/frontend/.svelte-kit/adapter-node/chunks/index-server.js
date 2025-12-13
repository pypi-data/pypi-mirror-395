import { i as ssr_context } from "./context.js";
import { l as lifecycle_function_unavailable } from "./errors.js";
import "clsx";
function onDestroy(fn) {
  /** @type {SSRContext} */
  ssr_context.r.on_destroy(fn);
}
function mount() {
  lifecycle_function_unavailable("mount");
}
function unmount() {
  lifecycle_function_unavailable("unmount");
}
async function tick() {
}
export {
  mount as m,
  onDestroy as o,
  tick as t,
  unmount as u
};
