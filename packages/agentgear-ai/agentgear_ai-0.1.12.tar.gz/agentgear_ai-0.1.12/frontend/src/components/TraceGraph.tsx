import { useMemo } from 'react';
import ReactFlow, {
    Background,
    Controls,
    Edge,
    Node,
    Position,
    useNodesState,
    useEdgesState,
} from 'reactflow';
import dagre from 'dagre';
import 'reactflow/dist/style.css';

type Span = {
    id: string;
    name: string;
    parent_id?: string;
    latency_ms?: number;
    status?: string;
};

const nodeWidth = 250;
const nodeHeight = 80;

const getLayoutedElements = (nodes: Node[], edges: Edge[]) => {
    const dagreGraph = new dagre.graphlib.Graph();
    dagreGraph.setDefaultEdgeLabel(() => ({}));

    dagreGraph.setGraph({ rankdir: 'TB' }); // Top to Bottom flow

    nodes.forEach((node) => {
        dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
    });

    edges.forEach((edge) => {
        dagreGraph.setEdge(edge.source, edge.target);
    });

    dagre.layout(dagreGraph);

    nodes.forEach((node) => {
        const nodeWithPosition = dagreGraph.node(node.id);
        node.targetPosition = Position.Top;
        node.sourcePosition = Position.Bottom;

        // Shift node to center it accurately
        node.position = {
            x: nodeWithPosition.x - nodeWidth / 2,
            y: nodeWithPosition.y - nodeHeight / 2,
        };

        return node;
    });

    return { nodes, edges };
};

export function TraceGraph({ spans }: { spans: Span[] }) {
    const { nodes: initialNodes, edges: initialEdges } = useMemo(() => {
        const nodes: Node[] = spans.map((span) => ({
            id: span.id,
            data: {
                label: (
                    <div className="p-2 border border-slate-200 rounded bg-white shadow-sm text-left">
                        <div className="font-semibold text-sm text-slate-800 truncate" title={span.name}>
                            {span.name}
                        </div>
                        <div className="text-xs text-slate-500 mt-1 flex justify-between">
                            <span>{span.status || 'unknown'}</span>
                            <span>{span.latency_ms ? `${Math.round(span.latency_ms)}ms` : '0ms'}</span>
                        </div>
                    </div>
                )
            },
            position: { x: 0, y: 0 },
            type: 'default', // Using default with custom label JSX
            style: {
                width: nodeWidth,
                border: 'none',
                background: 'transparent',
                padding: 0
            }
        }));

        const edges: Edge[] = spans
            .filter((s) => s.parent_id)
            .map((span) => ({
                id: `e-${span.parent_id}-${span.id}`,
                source: span.parent_id!,
                target: span.id,
                type: 'smoothstep',
                animated: true,
                style: { stroke: '#94a3b8' },
            }));

        return getLayoutedElements(nodes, edges);
    }, [spans]);

    const [nodes, , onNodesChange] = useNodesState(initialNodes);
    const [edges, , onEdgesChange] = useEdgesState(initialEdges);

    if (!spans || spans.length === 0) {
        return <div className="p-8 text-center text-slate-400">No spans to visualize</div>;
    }

    return (
        <div style={{ width: '100%', height: '500px' }} className="border rounded-lg bg-slate-50">
            <ReactFlow
                nodes={nodes}
                edges={edges}
                onNodesChange={onNodesChange}
                onEdgesChange={onEdgesChange}
                fitView
            >
                <Background />
                <Controls />
            </ReactFlow>
        </div>
    );
}
