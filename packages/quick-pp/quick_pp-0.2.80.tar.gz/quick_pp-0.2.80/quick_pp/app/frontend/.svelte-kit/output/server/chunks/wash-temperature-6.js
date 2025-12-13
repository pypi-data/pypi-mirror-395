import { n as sanitize_props, q as rest_props, e as attributes, k as ensure_array_like, l as element, b as slot, c as bind_props, g as spread_props } from "./index2.js";
import { f as fallback } from "./context.js";
const defaultAttributes = {
  outline: {
    xmlns: "http://www.w3.org/2000/svg",
    width: 24,
    height: 24,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    "stroke-width": 2,
    "stroke-linecap": "round",
    "stroke-linejoin": "round"
  },
  filled: {
    xmlns: "http://www.w3.org/2000/svg",
    width: 24,
    height: 24,
    viewBox: "0 0 24 24",
    fill: "currentColor",
    stroke: "none"
  }
};
function Icon($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const $$restProps = rest_props($$sanitized_props, ["type", "name", "color", "size", "stroke", "iconNode"]);
  $$renderer.component(($$renderer2) => {
    let type = $$props["type"];
    let name = $$props["name"];
    let color = fallback($$props["color"], "currentColor");
    let size = fallback($$props["size"], 24);
    let stroke = fallback($$props["stroke"], 2);
    let iconNode = $$props["iconNode"];
    $$renderer2.push(`<svg${attributes(
      {
        ...defaultAttributes[type],
        ...$$restProps,
        width: size,
        height: size,
        class: `tabler-icon tabler-icon-${name} ${$$sanitized_props.class ?? ""}`,
        ...type === "filled" ? { fill: color } : { "stroke-width": stroke, stroke: color }
      },
      void 0,
      void 0,
      void 0,
      3
    )}><!--[-->`);
    const each_array = ensure_array_like(iconNode);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let [tag, attrs] = each_array[$$index];
      element($$renderer2, tag, () => {
        $$renderer2.push(`${attributes({ ...attrs }, void 0, void 0, void 0, 3)}`);
      });
    }
    $$renderer2.push(`<!--]--><!--[-->`);
    slot($$renderer2, $$props, "default", {});
    $$renderer2.push(`<!--]--></svg>`);
    bind_props($$props, { type, name, color, size, stroke, iconNode });
  });
}
function List_details($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const iconNode = [
    ["path", { "d": "M13 5h8" }],
    ["path", { "d": "M13 9h5" }],
    ["path", { "d": "M13 15h8" }],
    ["path", { "d": "M13 19h5" }],
    [
      "path",
      {
        "d": "M3 4m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"
      }
    ],
    [
      "path",
      {
        "d": "M3 14m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z"
      }
    ]
  ];
  Icon($$renderer, spread_props([
    { type: "outline", name: "list-details" },
    $$sanitized_props,
    {
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
function Table($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const iconNode = [
    [
      "path",
      {
        "d": "M3 5a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2v-14z"
      }
    ],
    ["path", { "d": "M3 10h18" }],
    ["path", { "d": "M10 3v18" }]
  ];
  Icon($$renderer, spread_props([
    { type: "outline", name: "table" },
    $$sanitized_props,
    {
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
function Text_wrap_disabled($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const iconNode = [
    ["path", { "d": "M4 6l10 0" }],
    ["path", { "d": "M4 18l10 0" }],
    ["path", { "d": "M4 12h17l-3 -3m0 6l3 -3" }]
  ];
  Icon($$renderer, spread_props([
    { type: "outline", name: "text-wrap-disabled" },
    $$sanitized_props,
    {
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
function Wall($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const iconNode = [
    [
      "path",
      {
        "d": "M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z"
      }
    ],
    ["path", { "d": "M4 8h16" }],
    ["path", { "d": "M20 12h-16" }],
    ["path", { "d": "M4 16h16" }],
    ["path", { "d": "M9 4v4" }],
    ["path", { "d": "M14 8v4" }],
    ["path", { "d": "M8 12v4" }],
    ["path", { "d": "M16 12v4" }],
    ["path", { "d": "M11 16v4" }]
  ];
  Icon($$renderer, spread_props([
    { type: "outline", name: "wall" },
    $$sanitized_props,
    {
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
function Wash_temperature_6($$renderer, $$props) {
  const $$sanitized_props = sanitize_props($$props);
  const iconNode = [
    ["path", { "d": "M9 15h.01" }],
    [
      "path",
      {
        "d": "M3 6l1.721 10.329a2 2 0 0 0 1.973 1.671h10.612a2 2 0 0 0 1.973 -1.671l1.721 -10.329"
      }
    ],
    ["path", { "d": "M12 15h.01" }],
    ["path", { "d": "M15 15h.01" }],
    ["path", { "d": "M15 12h.01" }],
    ["path", { "d": "M12 12h.01" }],
    ["path", { "d": "M9 12h.01" }],
    [
      "path",
      {
        "d": "M3.486 8.965c.168 .02 .34 .033 .514 .035c.79 .009 1.539 -.178 2 -.5c.461 -.32 1.21 -.507 2 -.5c.79 -.007 1.539 .18 2 .5c.461 .322 1.21 .509 2 .5c.79 .009 1.539 -.178 2 -.5c.461 -.32 1.21 -.507 2 -.5c.79 -.007 1.539 .18 2 .5c.461 .322 1.21 .509 2 .5c.17 0 .339 -.014 .503 -.034"
      }
    ]
  ];
  Icon($$renderer, spread_props([
    { type: "outline", name: "wash-temperature-6" },
    $$sanitized_props,
    {
      iconNode,
      children: ($$renderer2) => {
        $$renderer2.push(`<!--[-->`);
        slot($$renderer2, $$props, "default", {});
        $$renderer2.push(`<!--]-->`);
      },
      $$slots: { default: true }
    }
  ]));
}
export {
  Icon as I,
  List_details as L,
  Text_wrap_disabled as T,
  Wall as W,
  Wash_temperature_6 as a,
  Table as b
};
