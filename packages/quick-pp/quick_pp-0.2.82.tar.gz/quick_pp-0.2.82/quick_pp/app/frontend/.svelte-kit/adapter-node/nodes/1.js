

export const index = 1;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/error.svelte.js')).default;
export const imports = ["_app/immutable/nodes/1.DN2KB0_o.js","_app/immutable/chunks/BA6D4iam.js","_app/immutable/chunks/BNO5OzLn.js","_app/immutable/chunks/BJMC0GYJ.js"];
export const stylesheets = ["_app/immutable/assets/vendor.S5W4ZllZ.css"];
export const fonts = [];
