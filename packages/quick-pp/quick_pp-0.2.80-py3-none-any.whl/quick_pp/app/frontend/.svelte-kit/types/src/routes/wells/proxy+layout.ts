// @ts-nocheck
import type { LayoutLoad } from './$types';

export const load = async ({ params }: Parameters<LayoutLoad>[0]) => {
  const projectId = params.project_id ?? null;
  const wellId = params.well_id ? decodeURIComponent(params.well_id) : null;
  return { projectId, wellId };
};
