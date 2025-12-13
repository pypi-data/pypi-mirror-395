const load = ({ params }) => {
  const projectId = params.project_id ?? null;
  return {
    title: "Well Analysis",
    subtitle: projectId ? `ID: ${projectId}` : void 0
  };
};

var _page_ts = /*#__PURE__*/Object.freeze({
  __proto__: null,
  load: load
});

const index = 13;
let component_cache;
const component = async () => component_cache ??= (await import('./_page.svelte-D0GBuANB.js')).default;
const universal_id = "src/routes/wells/[project_id]/[well_id]/+page.ts";
const imports = ["_app/immutable/nodes/13.DbAFZZ-o.js","_app/immutable/chunks/BA6D4iam.js","_app/immutable/chunks/BNO5OzLn.js","_app/immutable/chunks/BJMC0GYJ.js","_app/immutable/chunks/Dh51Yzp7.js","_app/immutable/chunks/NApQS6X6.js","_app/immutable/chunks/DM-oo5q7.js","_app/immutable/chunks/PPVm8Dsz.js","_app/immutable/chunks/C4A3Hpap.js"];
const stylesheets = ["_app/immutable/assets/vendor.S5W4ZllZ.css","_app/immutable/assets/DepthFilterStatus.CMzVkwfb.css"];
const fonts = [];

export { component, fonts, imports, index, stylesheets, _page_ts as universal, universal_id };
//# sourceMappingURL=13-DVTbv_E_.js.map
