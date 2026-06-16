import { auth, currentUser } from "@clerk/nextjs/server";
import { AppShell } from "@/components/app-shell";

export default async function ProfilePage() {
  const user = await currentUser();
  const { redirectToSignIn } = await auth();
  if (!user) return redirectToSignIn();
  return <AppShell><main className="mx-auto max-w-3xl p-6"><h1 className="text-3xl font-black">Profile</h1><div className="card mt-6 p-6"><p className="text-sm text-slate-400">Signed in as</p><p className="mt-2 text-xl font-bold">{user.fullName ?? user.username}</p><p className="text-slate-300">{user.primaryEmailAddress?.emailAddress}</p></div></main></AppShell>;
}
