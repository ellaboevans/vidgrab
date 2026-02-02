/**
 * Hook to control coming soon mode visibility
 * Set NEXT_PUBLIC_COMING_SOON=true in .env to enable
 */
export function useComingSoon(): boolean {
  return process.env.NEXT_PUBLIC_COMING_SOON === "true";
}
