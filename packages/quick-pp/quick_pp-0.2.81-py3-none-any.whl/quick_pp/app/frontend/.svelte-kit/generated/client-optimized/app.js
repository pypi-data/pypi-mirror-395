export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13'),
	() => import('./nodes/14'),
	() => import('./nodes/15'),
	() => import('./nodes/16'),
	() => import('./nodes/17'),
	() => import('./nodes/18')
];

export const server_loads = [];

export const dictionary = {
		"/": [4],
		"/login": [5],
		"/projects": [6],
		"/projects/[project_id]": [7,[2]],
		"/projects/[project_id]/perm-transform": [8,[2]],
		"/projects/[project_id]/rock-typing": [9,[2]],
		"/projects/[project_id]/shf": [10,[2]],
		"/wells": [11,[3]],
		"/wells/[project_id]": [12,[3]],
		"/wells/[project_id]/[well_id]": [13,[3]],
		"/wells/[project_id]/[well_id]/data": [14,[3]],
		"/wells/[project_id]/[well_id]/litho-poro": [15,[3]],
		"/wells/[project_id]/[well_id]/perm": [16,[3]],
		"/wells/[project_id]/[well_id]/ressum": [17,[3]],
		"/wells/[project_id]/[well_id]/saturation": [18,[3]]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),
	
	reroute: (() => {}),
	transport: {}
};

export const decoders = Object.fromEntries(Object.entries(hooks.transport).map(([k, v]) => [k, v.decode]));
export const encoders = Object.fromEntries(Object.entries(hooks.transport).map(([k, v]) => [k, v.encode]));

export const hash = false;

export const decode = (type, value) => decoders[type](value);

export { default as root } from '../root.js';