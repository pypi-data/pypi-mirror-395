// @ts-nocheck
import type { PageLoad } from './$types';

export const load = ({ params }: Parameters<PageLoad>[0]) => {
  const projectId = params.project_id ?? null;
  return {
    title: 'Well Analysis',
    subtitle: projectId ? `ID: ${projectId}` : undefined,
  };
};
