const load = ({ params }) => {
  const projectId = params.project_id ?? null;
  return {
    title: "Well Analysis",
    subtitle: projectId ? `ID: ${projectId}` : void 0
  };
};
export {
  load
};
