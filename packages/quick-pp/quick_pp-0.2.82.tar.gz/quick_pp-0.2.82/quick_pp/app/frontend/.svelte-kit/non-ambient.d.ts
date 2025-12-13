
// this file is generated — do not edit it


declare module "svelte/elements" {
	export interface HTMLAttributes<T> {
		'data-sveltekit-keepfocus'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-noscroll'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-preload-code'?:
			| true
			| ''
			| 'eager'
			| 'viewport'
			| 'hover'
			| 'tap'
			| 'off'
			| undefined
			| null;
		'data-sveltekit-preload-data'?: true | '' | 'hover' | 'tap' | 'off' | undefined | null;
		'data-sveltekit-reload'?: true | '' | 'off' | undefined | null;
		'data-sveltekit-replacestate'?: true | '' | 'off' | undefined | null;
	}
}

export {};


declare module "$app/types" {
	export interface AppTypes {
		RouteId(): "/" | "/login" | "/projects" | "/projects/[project_id]" | "/projects/[project_id]/perm-transform" | "/projects/[project_id]/rock-typing" | "/projects/[project_id]/shf" | "/wells" | "/wells/[project_id]" | "/wells/[project_id]/[well_id]" | "/wells/[project_id]/[well_id]/data" | "/wells/[project_id]/[well_id]/litho-poro" | "/wells/[project_id]/[well_id]/perm" | "/wells/[project_id]/[well_id]/ressum" | "/wells/[project_id]/[well_id]/saturation";
		RouteParams(): {
			"/projects/[project_id]": { project_id: string };
			"/projects/[project_id]/perm-transform": { project_id: string };
			"/projects/[project_id]/rock-typing": { project_id: string };
			"/projects/[project_id]/shf": { project_id: string };
			"/wells/[project_id]": { project_id: string };
			"/wells/[project_id]/[well_id]": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/data": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/litho-poro": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/perm": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/ressum": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/saturation": { project_id: string; well_id: string }
		};
		LayoutParams(): {
			"/": { project_id?: string; well_id?: string };
			"/login": Record<string, never>;
			"/projects": { project_id?: string };
			"/projects/[project_id]": { project_id: string };
			"/projects/[project_id]/perm-transform": { project_id: string };
			"/projects/[project_id]/rock-typing": { project_id: string };
			"/projects/[project_id]/shf": { project_id: string };
			"/wells": { project_id?: string; well_id?: string };
			"/wells/[project_id]": { project_id: string; well_id?: string };
			"/wells/[project_id]/[well_id]": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/data": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/litho-poro": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/perm": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/ressum": { project_id: string; well_id: string };
			"/wells/[project_id]/[well_id]/saturation": { project_id: string; well_id: string }
		};
		Pathname(): "/" | "/login" | "/login/" | "/projects" | "/projects/" | `/projects/${string}` & {} | `/projects/${string}/` & {} | `/projects/${string}/perm-transform` & {} | `/projects/${string}/perm-transform/` & {} | `/projects/${string}/rock-typing` & {} | `/projects/${string}/rock-typing/` & {} | `/projects/${string}/shf` & {} | `/projects/${string}/shf/` & {} | "/wells" | "/wells/" | `/wells/${string}` & {} | `/wells/${string}/` & {} | `/wells/${string}/${string}` & {} | `/wells/${string}/${string}/` & {} | `/wells/${string}/${string}/data` & {} | `/wells/${string}/${string}/data/` & {} | `/wells/${string}/${string}/litho-poro` & {} | `/wells/${string}/${string}/litho-poro/` & {} | `/wells/${string}/${string}/perm` & {} | `/wells/${string}/${string}/perm/` & {} | `/wells/${string}/${string}/ressum` & {} | `/wells/${string}/${string}/ressum/` & {} | `/wells/${string}/${string}/saturation` & {} | `/wells/${string}/${string}/saturation/` & {};
		ResolvedPathname(): `${"" | `/${string}`}${ReturnType<AppTypes['Pathname']>}`;
		Asset(): "/robots.txt" | string & {};
	}
}