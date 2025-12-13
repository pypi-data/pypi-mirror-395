

export const index = 1;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/error.svelte.js')).default;
export const imports = ["_app/immutable/nodes/1.sF9C5BAx.js","_app/immutable/chunks/3IT1wouH.js","_app/immutable/chunks/BNO5OzLn.js","_app/immutable/chunks/BRMrIf-g.js"];
export const stylesheets = ["_app/immutable/assets/vendor.S5W4ZllZ.css"];
export const fonts = [];
