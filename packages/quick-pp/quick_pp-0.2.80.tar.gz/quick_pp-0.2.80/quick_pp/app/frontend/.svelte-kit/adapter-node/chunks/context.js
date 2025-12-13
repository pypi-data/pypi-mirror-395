var is_array = Array.isArray;
var index_of = Array.prototype.indexOf;
var array_from = Array.from;
var define_property = Object.defineProperty;
var get_descriptor = Object.getOwnPropertyDescriptor;
var object_prototype = Object.prototype;
var array_prototype = Array.prototype;
var get_prototype_of = Object.getPrototypeOf;
var is_extensible = Object.isExtensible;
const noop = () => {
};
function run(fn) {
  return fn();
}
function run_all(arr) {
  for (var i = 0; i < arr.length; i++) {
    arr[i]();
  }
}
function deferred() {
  var resolve;
  var reject;
  var promise = new Promise((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}
function fallback(value, fallback2, lazy = false) {
  return value === void 0 ? lazy ? (
    /** @type {() => V} */
    fallback2()
  ) : (
    /** @type {V} */
    fallback2
  ) : value;
}
function lifecycle_outside_component(name) {
  {
    throw new Error(`https://svelte.dev/e/lifecycle_outside_component`);
  }
}
var ssr_context = null;
function set_ssr_context(v) {
  ssr_context = v;
}
function getContext(key) {
  const context_map = get_or_init_context_map();
  const result = (
    /** @type {T} */
    context_map.get(key)
  );
  return result;
}
function setContext(key, context) {
  get_or_init_context_map().set(key, context);
  return context;
}
function hasContext(key) {
  return get_or_init_context_map().has(key);
}
function getAllContexts() {
  return get_or_init_context_map();
}
function get_or_init_context_map(name) {
  if (ssr_context === null) {
    lifecycle_outside_component();
  }
  return ssr_context.c ??= new Map(get_parent_context(ssr_context) || void 0);
}
function push(fn) {
  ssr_context = { p: ssr_context, c: null, r: null };
}
function pop() {
  ssr_context = /** @type {SSRContext} */
  ssr_context.p;
}
function get_parent_context(ssr_context2) {
  let parent = ssr_context2.p;
  while (parent !== null) {
    const context_map = parent.c;
    if (context_map !== null) {
      return context_map;
    }
    parent = parent.p;
  }
  return null;
}
export {
  array_from as a,
  getAllContexts as b,
  run_all as c,
  define_property as d,
  set_ssr_context as e,
  fallback as f,
  getContext as g,
  hasContext as h,
  ssr_context as i,
  pop as j,
  deferred as k,
  array_prototype as l,
  get_descriptor as m,
  noop as n,
  object_prototype as o,
  push as p,
  get_prototype_of as q,
  run as r,
  setContext as s,
  is_array as t,
  is_extensible as u,
  index_of as v
};
