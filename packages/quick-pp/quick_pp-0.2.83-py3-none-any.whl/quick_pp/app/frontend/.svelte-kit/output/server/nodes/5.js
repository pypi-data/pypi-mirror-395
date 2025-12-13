

export const index = 5;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/login/_page.svelte.js')).default;
export const imports = ["_app/immutable/nodes/5.E92b6ga7.js","_app/immutable/chunks/C3gbSB1S.js","_app/immutable/chunks/BNO5OzLn.js","_app/immutable/chunks/BJMC0GYJ.js","_app/immutable/chunks/pD2rMnZE.js","_app/immutable/chunks/BlDOT_QG.js"];
export const stylesheets = ["_app/immutable/assets/vendor.S5W4ZllZ.css"];
export const fonts = [];
