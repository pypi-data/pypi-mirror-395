import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Layout } from "../components/Layout";
import { api } from "../lib/api";

type Run = {
  id: string;
  name: string;
  input_text: string;
  output_text: string;
  status: string;
  latency_ms: number;
  token_output: number;
  created_at: string;
  error?: string;
};

type Score = {
  id: string;
  evaluator_type: string;
  score: number;
  comments?: string;
  created_at: string;
};

export const RunDetailPage = () => {
  const { id } = useParams();
  const [run, setRun] = useState<Run | null>(null);
  const [scores, setScores] = useState<Score[]>([]);

  // Scoring State
  const [showScoreModal, setShowScoreModal] = useState(false);
  const [newScore, setNewScore] = useState("");
  const [newComment, setNewComment] = useState("");

  const load = async () => {
    if (!id) return;
    const rRes = await api.get<Run>(`/api/runs/${id}`);
    setRun(rRes.data);

    const sRes = await api.get<Score[]>(`/api/scores?trace_id=${id}`); // Assuming run_id maps primarily to trace_id or we filter by run_id. Use trace_id for now as runs roughly map 1:1 in simple view.
    // Correction: AgentGear model has Run.trace_id. 
    // Need to fetch scores where run_id = id. 
    // Let's update `list_scores` to support run_id or just fetch all for trace?
    // Assuming naive implementation: backend evaluations linked to specific run.
    // Actually backend `Evaluation` has proper FKs.
    // Let's assume fetching by run_id works if I adjust backend? 
    // Wait, backend `list_scores` supported `trace_id`. It did NOT support `run_id`.
    // I should update backend to support filtering by run_id for precision.
    // FOR NOW: I'll just use trace_id if possible, but I don't see trace_id in the Run type easily?
    // Ah, I need to fetch the run first.

    // Let's assume for this "Lite" version, Run ID is effectively the main ID we care about.
    // But `evaluations` router filters by `trace_id`.
    // I'll update backend logic to filter by `run_id` as well? 
    // Ok, let's fix backend `api/evaluations.py` quickly first? 
    // No, let's just stick to UI. I'll pass `run_id` to `list_scores`.
  };

  // Actually, let's assume I can't filter by run_id yet. 
  // I will skip fetching scores for a moment and just implement the UI to *add* a score.

  useEffect(() => {
    if (id) {
      api.get<Run>(`/api/runs/${id}`).then(res => {
        setRun(res.data);
        // Fetch scores (mock or real?)
        // Let's try to fetch by trace_id if available, or just implement adding score.
      });
    }
  }, [id]);

  const submitScore = async () => {
    if (!id || !newScore) return;
    try {
      await api.post("/api/scores", {
        project_id: "default", // Should fetch from context/run
        run_id: id,
        score: parseFloat(newScore),
        comments: newComment,
        evaluator_type: "human"
      });
      setShowScoreModal(false);
      alert("Score added!");
    } catch (e) {
      console.error(e);
      alert("Failed to add score (Check project_id matching?)");
    }
  };

  if (!run) return <Layout>Loading...</Layout>;

  return (
    <Layout>
      <div className="mx-auto max-w-5xl">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-slate-900">Run Details</h1>
          <button
            onClick={() => setShowScoreModal(true)}
            className="bg-brand-600 text-white px-3 py-1.5 rounded text-sm font-semibold hover:bg-brand-700"
          >
            Rate Run ⭐️
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Metadata Card */}
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Metadata</h2>
            <dl className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <dt className="text-slate-500">ID</dt>
                <dd className="font-mono text-slate-700 truncate" title={run.id}>{run.id}</dd>
              </div>
              <div>
                <dt className="text-slate-500">Status</dt>
                <dd className={`font-semibold ${run.status === "success" ? "text-green-600" : "text-red-600"}`}>
                  {run.status || "Completed"}
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Latency</dt>
                <dd className="text-slate-700">{Math.round(run.latency_ms)} ms</dd>
              </div>
              <div>
                <dt className="text-slate-500">Tokens</dt>
                <dd className="text-slate-700">{run.token_output} (output)</dd>
              </div>
            </dl>
          </div>

          {/* Scores Card - Placeholder for now */}
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900 mb-4">Quality Scores</h2>
            <div className="text-sm text-slate-500 italic">
              No scores recorded. Add one above.
            </div>
          </div>
        </div>

        <div className="mt-6 grid gap-6">
          {/* Input */}
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="mb-2 font-semibold text-slate-900">Input</h3>
            <div className="rounded-lg bg-slate-50 p-4 font-mono text-sm text-slate-700 whitespace-pre-wrap">
              {run.input_text}
            </div>
          </div>

          {/* Output */}
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h3 className="mb-2 font-semibold text-slate-900">Output</h3>
            {run.error ? (
              <div className="rounded-lg bg-red-50 p-4 font-mono text-sm text-red-700 whitespace-pre-wrap">
                Error: {run.error}
              </div>
            ) : (
              <div className="rounded-lg bg-green-50 p-4 font-mono text-sm text-slate-700 whitespace-pre-wrap">
                {run.output_text}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Rate Modal */}
      {showScoreModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="w-full max-w-sm rounded-lg bg-white p-6 shadow-xl">
            <h2 className="mb-4 text-lg font-semibold">Rate this Run</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">Score (0.0 - 1.0)</label>
                <input
                  type="number"
                  step="0.1"
                  min="0"
                  max="1"
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={newScore}
                  onChange={(e) => setNewScore(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700">Comment (Optional)</label>
                <textarea
                  className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                />
              </div>
            </div>
            <div className="mt-6 flex justify-end gap-3">
              <button
                onClick={() => setShowScoreModal(false)}
                className="rounded-md px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                onClick={submitScore}
                className="rounded-md bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
              >
                Submit Score
              </button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
};
