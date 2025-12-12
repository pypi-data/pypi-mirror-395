import { ReactNode } from "react";

export const TokenModal = ({
  token,
  onClose
}: {
  token: string | null;
  onClose: () => void;
}) => {
  if (!token) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-lg">
        <h2 className="text-lg font-semibold text-slate-900">Your API Token</h2>
        <p className="mt-2 text-sm text-slate-600">
          Copy this token now. It will not be shown again.
        </p>
        <div className="mt-4 rounded border border-slate-200 bg-slate-50 p-3 font-mono text-sm">
          {token}
        </div>
        <div className="mt-4 flex justify-end gap-2">
          <button
            className="rounded bg-brand-600 px-3 py-2 text-sm font-medium text-white hover:bg-brand-700"
            onClick={() => {
              navigator.clipboard.writeText(token);
            }}
          >
            Copy
          </button>
          <button
            className="rounded border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
            onClick={onClose}
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};
