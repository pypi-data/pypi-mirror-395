
// ---- types & utils ----
export type NodeId = string;
export type PortName = string;
export type PortValue = any;

export type InputSync = 'all' | 'any' | 'driver' | 'timestamp';

export interface Link { from: { node: NodeId, port: PortName }, to: { node: NodeId, port: PortName } }

function uid(prefix = '') { return prefix + Math.random().toString(36).slice(2, 9); }

// ---- Node base ----
export abstract class BaseNode {
    id: NodeId;
    inputs: Record<PortName, PortValue | undefined> = {};
    outputs: Record<PortName, PortValue | undefined> = {};
    inputNewFlag: Record<PortName, boolean> = {};
    inputTimestamps: Record<PortName, number | undefined> = {};
    inputSync: InputSync = 'all';
    driverPort?: PortName; // when inputSync == 'driver'

    constructor(id?: NodeId) {
        this.id = id ?? uid('node_');
    }

    // each node implements this
    abstract process(inputs: Record<PortName, PortValue>): Promise<Record<PortName, PortValue>>;

    // helper: called by engine to set an input
    receiveInput(port: PortName, value: PortValue, ts?: number) {
        this.inputs[port] = value;
        this.inputNewFlag[port] = true;
        if (ts !== undefined) this.inputTimestamps[port] = ts;
    }

    // decide if node can execute given its inputFlags & policy
    canExecute(): boolean {
        const ports = Object.keys(this.inputs);
        if (ports.length === 0) return true; // source-like node
        if (this.inputSync === 'all') {
            return ports.every(p => !!this.inputNewFlag[p]);
        }
        if (this.inputSync === 'any') {
            return ports.some(p => !!this.inputNewFlag[p]);
        }
        if (this.inputSync === 'driver') {
            if (!this.driverPort) return false;
            return !!this.inputNewFlag[this.driverPort];
        }
        if (this.inputSync === 'timestamp') {
            // naive timestamp alignment: all new and max-min <= tolerance
            const vals = ports.map(p => this.inputTimestamps[p] ?? 0);
            if (vals.some(v => v === 0)) return false;
            const tol = 20; // ms tolerance, can be parameterized
            return (Math.max(...vals) - Math.min(...vals)) <= tol;
        }
        return false;
    }

    // clear new flags for ports we've consumed
    clearNewFlags(consumedPorts: PortName[] = []) {
        if (this.inputSync === 'any') {
            // clear only the consumed ports (we'll assume caller passes which)
            consumedPorts.forEach(p => this.inputNewFlag[p] = false);
        } else {
            // clear all by default
            Object.keys(this.inputNewFlag).forEach(p => this.inputNewFlag[p] = false);
        }
    }
}

// ---- Example Nodes ----

// 1) Source node: pushes periodically
export class SourceNode extends BaseNode {
    outName: PortName = 'out';
    intervalMs: number;
    makeValue: () => any;
    timer: any = null;
    engine: Engine | null = null;

    constructor(makeValue: () => any, intervalMs = 100, id?: NodeId) {
        super(id);
        this.intervalMs = intervalMs;
        this.makeValue = makeValue;
        this.outputs[this.outName] = undefined;
    }

    async process(_: Record<string, any>) {
        // produce a value
        const v = this.makeValue();
        this.outputs[this.outName] = v;
        return { [this.outName]: v };
    }

    start(engine: Engine) {
        this.engine = engine;
        this.timer = setInterval(async () => {
            const out = await this.process({});
            // use timestamp for sync policies if needed
            engine.publish(this.id, this.outName, out[this.outName], Date.now());
        }, this.intervalMs);
    }

    stop() {
        if (this.timer) clearInterval(this.timer);
        this.timer = null;
    }
}

// 2) Adder node: waits for all inputs (默认 all)
export class AdderNode extends BaseNode {
    inA = 'a'; inB = 'b'; out = 'sum';
    constructor(id?: NodeId) {
        super(id);
        this.inputs[this.inA] = undefined;
        this.inputs[this.inB] = undefined;
        this.inputNewFlag[this.inA] = false;
        this.inputNewFlag[this.inB] = false;
        this.outputs[this.out] = undefined;
        this.inputSync = 'all';
    }
    async process(inputs: Record<string, any>) {
        const a = inputs[this.inA] ?? 0;
        const b = inputs[this.inB] ?? 0;
        const s = a + b;
        this.outputs[this.out] = s;
        console.log(`[ADD ${this.id}]`, a, b, s);
        return { [this.out]: s };
    }
}

// 3) Gain node: any-input policy (parameter + signal)
export class GainNode2 extends BaseNode {
    inSignal = 'sig'; inGain = 'gain'; out = 'out';
    constructor(id?: NodeId) {
        super(id);
        this.inputs[this.inSignal] = undefined;
        this.inputs[this.inGain] = 1;
        this.inputNewFlag[this.inSignal] = false;
        this.inputNewFlag[this.inGain] = false;
        this.outputs[this.out] = undefined;
        this.inputSync = 'any';
    }
    async process(inputs: Record<string, any>) {
        const sig = inputs[this.inSignal] ?? 0;
        const gain = inputs[this.inGain] ?? 1;
        const out = sig * gain;
        this.outputs[this.out] = out;
        return { [this.out]: out };
    }
}

// 4) Sink / Printer
export class PrintNode extends BaseNode {
    in = 'in';
    constructor(id?: NodeId) {
        super(id);
        this.inputs[this.in] = undefined;
        this.inputNewFlag[this.in] = false;
        this.inputSync = 'any';
    }
    async process(inputs: Record<string, any>) {
        console.log(`[PRINT ${this.id}]`, inputs[this.in]);
        return {};
    }
}

// ---- Engine ----
export class Engine {
    nodes: Map<NodeId, BaseNode> = new Map();
    links: Link[] = [];
    // adjacency: from node -> list of outgoing links
    adjacency: Map<NodeId, Link[]> = new Map();

    addNode(n: BaseNode) {
        this.nodes.set(n.id, n);
        this.adjacency.set(n.id, []);
    }

    addLink(link: Link) {
        this.links.push(link);
        if (!this.adjacency.has(link.from.node)) this.adjacency.set(link.from.node, []);
        this.adjacency.get(link.from.node)!.push(link);
    }

    // publish: called when a node produces an output
    async publish(fromNodeId: NodeId, port: PortName, value: any, ts?: number) {
        const outLinks = this.adjacency.get(fromNodeId) || [];
        // for each link forward to destination node's input
        const promises: Promise<any>[] = [];
        for (const lk of outLinks) {
            if (lk.from.port !== port) continue;
            const toNode = this.nodes.get(lk.to.node);
            if (!toNode) continue;
            toNode.receiveInput(lk.to.port, value, ts);
            // if destination can execute, schedule it
            if (toNode.canExecute()) {
                // collect inputs snapshot for processing
                const inputsSnapshot: Record<string, any> = {};
                const consumedPorts: PortName[] = [];
                for (const p of Object.keys(toNode.inputs)) {
                    inputsSnapshot[p] = toNode.inputs[p];
                    if (toNode.inputNewFlag[p]) consumedPorts.push(p);
                }
                // clear flags before async process to avoid reentrancy problems
                toNode.clearNewFlags(consumedPorts);
                const p = (async () => {
                    try {
                        const outs = await toNode.process(inputsSnapshot);
                        // publish its outputs to downstream
                        for (const outPort of Object.keys(outs)) {
                            await this.publish(toNode.id, outPort, outs[outPort], Date.now());
                        }
                    } catch (e) {
                        console.error('Node process error', toNode.id, e);
                    }
                })();
                promises.push(p);
            }
        }
        // we don't await here in push model; but we return a Promise for optional waiting
        if (promises.length) {
            return Promise.all(promises);
        } else {
            return Promise.resolve();
        }
    }

    startAllSources() {
        console.log('startAllSources');
        for (const n of this.nodes.values()) {
            if (n instanceof SourceNode) {
                console.log('start source', n.id);
                n.start(this);
            }
        }
    }

    stopAllSources() {
        for (const n of this.nodes.values()) {
            if (n instanceof SourceNode) n.stop();
        }
    }
}


// 示例代码（已注释，由 Vue 组件使用）
// 如果需要直接运行示例，取消下面的注释
/*
// create engine
const e = new Engine();

// create two sources with different intervals
const s1 = new SourceNode(() => Math.floor(Math.random() * 10), 300, 'srcA');
const s2 = new SourceNode(() => Math.floor(Math.random() * 10), 500, 'srcB');

// adder node expecting both inputs (all)
const add = new AdderNode('adder1');
// print node
const printer = new PrintNode('printer1');

// register
e.addNode(s1); e.addNode(s2); e.addNode(add); e.addNode(printer);

// links: srcA.out -> adder.a ; srcB.out -> adder.b ; adder.sum -> printer.in
e.addLink({ from: { node: 'srcA', port: 'out' }, to: { node: 'adder1', port: 'a' } });
e.addLink({ from: { node: 'srcB', port: 'out' }, to: { node: 'adder1', port: 'b' } });
e.addLink({ from: { node: 'adder1', port: 'sum' }, to: { node: 'printer1', port: 'in' } });

// start
e.startAllSources();

// after some time stop
setTimeout(() => {
    e.stopAllSources();
    console.log('stopped');
}, 5000);
*/
