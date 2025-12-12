import { useState } from "react";
import { Layout } from "../components/Layout";

export const GuidePage = () => {
    const [activeSection, setActiveSection] = useState("quick-start");

    const sections = [
        { id: "quick-start", label: "Quick Start" },
        { id: "concepts", label: "Core Concepts" },
        { id: "sdk", label: "Python SDK" },
        { id: "features", label: "Dashboard Features" }
    ];

    const scrollToSection = (id: string) => {
        setActiveSection(id);
        const element = document.getElementById(id);
        if (element) element.scrollIntoView({ behavior: "smooth" });
    };

    return (
        <Layout>
            <div className="mx-auto max-w-6xl">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-slate-900">Documentation</h1>
                    <p className="mt-2 text-lg text-slate-600">
                        Complete guide to integrating and using AgentGear for LLM observability and engineering.
                    </p>
                </div>

                <div className="flex gap-8 items-start">
                    {/* Sticky Table of Contents */}
                    <nav className="w-64 sticky top-6 hidden lg:block space-y-1">
                        {sections.map(section => (
                            <button
                                key={section.id}
                                onClick={() => scrollToSection(section.id)}
                                className={`block w-full text-left px-4 py-2 text-sm font-medium rounded-lg transition-colors ${activeSection === section.id
                                        ? "bg-brand-50 text-brand-700"
                                        : "text-slate-600 hover:bg-slate-50"
                                    }`}
                            >
                                {section.label}
                            </button>
                        ))}
                    </nav>

                    <div className="flex-1 space-y-16">
                        {/* Quick Start */}
                        <section id="quick-start" className="scroll-mt-8">
                            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-100 text-brand-600 text-sm">1</span>
                                Quick Start
                            </h2>
                            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                                <p className="text-slate-600 mb-6">
                                    Get up and running in less than 5 minutes.
                                </p>

                                <div className="space-y-6">
                                    <div>
                                        <h3 className="text-sm font-bold uppercase text-slate-500 mb-2">1. Install SDK</h3>
                                        <div className="rounded-lg bg-slate-900 p-4">
                                            <code className="text-sm text-green-400 font-mono">pip install agentgear-ai</code>
                                        </div>
                                    </div>

                                    <div>
                                        <h3 className="text-sm font-bold uppercase text-slate-500 mb-2">2. Initialize Client</h3>
                                        <div className="rounded-lg bg-slate-900 p-4 relative group">
                                            <pre className="text-sm text-slate-300 font-mono overflow-x-auto">
                                                {`from agentgear import AgentGearClient, observe

# Initialize the client
client = AgentGearClient(
    base_url="http://localhost:8000",  # Your server URL
    project_id="<YOUR_PROJECT_ID>",    # Found in Dashboard > Projects
    api_key="<YOUR_API_KEY>"           # Found in Dashboard > API Management
)`}
                                            </pre>
                                        </div>
                                    </div>

                                    <div>
                                        <h3 className="text-sm font-bold uppercase text-slate-500 mb-2">3. Instrument Code</h3>
                                        <div className="rounded-lg bg-slate-900 p-4">
                                            <pre className="text-sm text-slate-300 font-mono overflow-x-auto">
                                                {`@observe(client)
def chat_with_user(message):
    # Your LLM logic here (OpenAI, Anthropic, etc.)
    response = openai.ChatCompletion.create(...)
    return response.choices[0].message.content`}
                                            </pre>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* Core Concepts */}
                        <section id="concepts" className="scroll-mt-8">
                            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-blue-600 text-sm">2</span>
                                Core Concepts
                            </h2>
                            <div className="grid gap-6 md:grid-cols-2">
                                <ConceptCard
                                    icon="📦"
                                    title="Projects"
                                    desc="Isolate environments (Dev, Staging, Prod) or distinct applications. Each project has unique API keys and data separation."
                                />
                                <ConceptCard
                                    icon="📝"
                                    title="Prompt Registry"
                                    desc="Decouple prompt text from code. Create, version, and manage prompts in the UI. Fetch them dynamically via SDK."
                                />
                                <ConceptCard
                                    icon="🔍"
                                    title="Traces & Spans"
                                    desc="Visualize the full lifecycle of a request. A 'Trace' is the full request, composed of nested 'Spans' (indvidual steps)."
                                />
                                <ConceptCard
                                    icon="🧪"
                                    title="Playground"
                                    desc="Test prompts directly in the browser. Iterate on prompt engineering without running any code locally."
                                />
                            </div>
                        </section>

                        {/* SDK Reference */}
                        <section id="sdk" className="scroll-mt-8">
                            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-purple-100 text-purple-600 text-sm">3</span>
                                SDK Reference
                            </h2>
                            <div className="space-y-6">
                                <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                                    <h3 className="font-semibold text-slate-900 mb-3">Fetching Prompts</h3>
                                    <p className="text-sm text-slate-600 mb-4">
                                        Dynamically load prompt templates from the registry. This allows you to update prompts in real-time without redeploying.
                                    </p>
                                    <div className="rounded-lg bg-slate-900 p-4">
                                        <pre className="text-sm text-slate-300 font-mono overflow-x-auto">
                                            {`# Fetch the latest version of a prompt
prompt = client.prompts.get("customer-service-agent")

# Use the content
print(prompt.content) 

# With versioning (optional)
v2 = client.prompts.get("customer-service-agent", version=2)`}
                                        </pre>
                                    </div>
                                </div>

                                <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
                                    <h3 className="font-semibold text-slate-900 mb-3">Manual Tracing</h3>
                                    <p className="text-sm text-slate-600 mb-4">
                                        For fine-grained control, manually create traces and spans.
                                    </p>
                                    <div className="rounded-lg bg-slate-900 p-4">
                                        <pre className="text-sm text-slate-300 font-mono overflow-x-auto">
                                            {`with client.trace(name="complex-workflow") as trace:
    
    with trace.span(name="retrieve-context") as span:
        # Context retrieval logic
        span.set_attribute("doc_count", 5)
    
    with trace.span(name="llm-generation"):
        # LLM call
        pass`}
                                        </pre>
                                    </div>
                                </div>
                            </div>
                        </section>

                        {/* Features */}
                        <section id="features" className="scroll-mt-8">
                            <h2 className="text-2xl font-bold text-slate-900 mb-6 flex items-center gap-2">
                                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-pink-100 text-pink-600 text-sm">4</span>
                                Advanced Features
                            </h2>
                            <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-xl p-8 text-white">
                                <div className="grid lg:grid-cols-2 gap-8 items-center">
                                    <div>
                                        <h3 className="text-xl font-bold mb-2">Interactive Playground</h3>
                                        <p className="text-slate-300 mb-6">
                                            Debug and refine your prompts instantly. The Playground allows you to select models, inject variables, and view outputs + latency in real-time.
                                        </p>
                                        <ul className="space-y-2 text-sm text-slate-300">
                                            <li className="flex items-center gap-2">✅ Supports OpenAI, Anthropic, etc.</li>
                                            <li className="flex items-center gap-2">✅ Variable interpolation</li>
                                            <li className="flex items-center gap-2">✅ Save as new version</li>
                                        </ul>
                                    </div>
                                    <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
                                        <div className="flex gap-2 mb-2">
                                            <div className="h-3 w-3 rounded-full bg-red-400"></div>
                                            <div className="h-3 w-3 rounded-full bg-yellow-400"></div>
                                            <div className="h-3 w-3 rounded-full bg-green-400"></div>
                                        </div>
                                        <div className="space-y-2 font-mono text-xs text-slate-400">
                                            <div className="text-green-400">Running prompt: "summarize_email"...</div>
                                            <div>Inputs: {`{ "email": "..." }`}</div>
                                            <div className="pl-2 border-l-2 border-slate-600">
                                                Output: "Here is the summary of the email..."
                                            </div>
                                            <div className="text-slate-500">Latency: 450ms</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>

                    </div>
                </div>
            </div>
        </Layout>
    );
};

const ConceptCard = ({ icon, title, desc }: { icon: string, title: string, desc: string }) => (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
        <div className="mb-3 text-3xl">{icon}</div>
        <h3 className="font-semibold text-slate-900 text-lg">{title}</h3>
        <p className="mt-2 text-sm text-slate-600 leading-relaxed">
            {desc}
        </p>
    </div>
);
