export function resolveRunId(runIdParam: string | undefined): string | null {
  if (!runIdParam) return null
  if (runIdParam === 'last') {
    return localStorage.getItem('lastRunId')
  }
  return runIdParam
}
